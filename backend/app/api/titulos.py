from typing import Optional, List
import time
from datetime import datetime, timedelta
from itertools import combinations
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from pydantic import BaseModel, Field
from ..core.database import get_connection
import logging

logger = logging.getLogger("bimer.titulos")

router = APIRouter(tags=["Títulos & Contas a Pagar"])

class ImpostoItem(BaseModel):
    tipo: str
    aliquota: Optional[float] = 0.0
    valor: float
    dt_venc_imp: Optional[str] = None
    historico: Optional[str] = None

class DocumentoEntrada(BaseModel):
    tipo_doc: str = Field(..., description="NFSE, NFE, RECIBO, CONTRATO, FATURA, DESPESA_INTERNA")
    numero_doc: str
    favorecido: str
    cnpj: str
    data_emissao: str
    data_entrada: Optional[str] = None
    vencimento: str
    valor_bruto: float
    historico: Optional[str] = ""
    descricao: Optional[str] = ""
    ccusto: Optional[str] = "Geral"
    solicitante: Optional[str] = ""
    contrato: Optional[str] = ""
    forma_pgto: Optional[str] = "PIX"
    dados_banco: Optional[str] = ""
    linha_dig: Optional[str] = ""
    cod_operacao: Optional[str] = "1.933 - Aquisição de serviço tributado pelo ISSQN"
    cnae: Optional[str] = ""
    item_lc116: Optional[str] = ""
    impostos: Optional[List[ImpostoItem]] = []

class ConciliacaoGrupoRequest(BaseModel):
    titulo_ids: List[int] = Field(..., description="IDs dos títulos no banco a vincular")
    extrato_fitid: Optional[str] = ""
    extrato_valor: float = Field(..., description="Valor do débito no extrato bancário")
    extrato_data: Optional[str] = ""
    extrato_memo: Optional[str] = ""
    tipo_diferenca: Optional[str] = Field(None, description="JUROS, MULTA, DESCONTO, ARREDONDAMENTO")
    operador: Optional[str] = "Sistema"

@router.get("")
@router.get("/titulos")
def listar_titulos(
    status: Optional[str] = None,
    filtro_data: Optional[str] = None,
    busca: Optional[str] = None
):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, numero_tx, numero_nf, fornecedor, cnpj, dt_emissao, dt_vencimento,
                   valor_bruto, valor_liquido, status, categoria, filial, responsavel,
                   descricao, forma_pgto, cod_barras, pix_chave, observacao,
                   conciliada, dt_pagamento, cod_operacao, cnae, item_lc116,
                   valor_pago, juros_multa, desconto, grupo_conciliacao
            FROM notas
            WHERE (is_previsao = 0 OR is_previsao IS NULL)
        """)
        rows_notas = cur.fetchall()

        cur.execute("SELECT id, nota_id, tipo, aliquota, valor, dt_venc_imp, status, numero_doc FROM nota_impostos")
        rows_impostos = cur.fetchall()
        
        impostos_por_nota = {}
        for imp in rows_impostos:
            nid = imp["nota_id"]
            if nid not in impostos_por_nota:
                impostos_por_nota[nid] = []
            impostos_por_nota[nid].append(dict(imp))

        conn.close()

        hoje_date = datetime.now().date()
        semana_date = hoje_date + timedelta(days=7)
        mes_atual_str = datetime.now().strftime("%Y-%m")

        titulos = []

        for n in rows_notas:
            nota_dict = dict(n)
            n_id = nota_dict["id"]
            n_venc = (nota_dict["dt_vencimento"] or "").strip()
            if n_venc and "/" in n_venc:
                parts = n_venc.split("/")
                if len(parts) == 3 and len(parts[2]) == 4:
                    n_venc = f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
            n_conciliada = bool(nota_dict.get("conciliada"))
            is_pago = (nota_dict.get("status") in ("PAGO", "CONCILIADO")) or n_conciliada
            n_status = "CONCILIADO" if is_pago else "PENDENTE"
            n_situacao = "BAIXADO" if is_pago else "ABERTO"

            titulos.append({
                "id": f"NOTA_{n_id}",
                "db_id": n_id,
                "origem": "NOTA",
                "tipo": "FORNECEDOR",
                "tipo_doc": nota_dict.get("categoria") or "NFSE",
                "numero_doc": nota_dict.get("numero_nf") or nota_dict.get("numero_tx"),
                "cod_operacao": nota_dict.get("cod_operacao") or "1.933 - Aquisição de serviço tributado pelo ISSQN",
                "cnae": nota_dict.get("cnae") or "",
                "item_lc116": nota_dict.get("item_lc116") or "",
                "favorecido": nota_dict.get("fornecedor"),
                "cnpj": nota_dict.get("cnpj"),
                "vencimento": n_venc,
                "valor": nota_dict.get("valor_liquido") or nota_dict.get("valor_bruto") or 0.0,
                "valor_bruto": nota_dict.get("valor_bruto") or 0.0,
                "historico": nota_dict.get("observacao") or "",
                "descricao": nota_dict.get("descricao") or "",
                "ccusto": nota_dict.get("filial") or "",
                "solicitante": nota_dict.get("responsavel") or "",
                "forma_pgto": nota_dict.get("forma_pgto") or "PIX",
                "linha_dig": nota_dict.get("cod_barras") or "",
                "status": n_status,
                "situacao": n_situacao,
                "conciliada": n_conciliada,
                "data_baixa": nota_dict.get("dt_pagamento"),
                "loteId": nota_dict.get("numero_tx"),
                "valor_pago": nota_dict.get("valor_pago"),
                "juros_multa": nota_dict.get("juros_multa") or 0,
                "desconto": nota_dict.get("desconto") or 0,
                "grupo_conciliacao": nota_dict.get("grupo_conciliacao"),
            })

            for imp in impostos_por_nota.get(n_id, []):
                venc_imp = imp.get("dt_venc_imp") or n_venc
                tipo_imp = imp.get("tipo", "IMPOSTO")
                titulos.append({
                    "id": f"IMP_{imp['id']}",
                    "db_id": imp["id"],
                    "nota_pai_id": n_id,
                    "origem": "IMPOSTO",
                    "tipo": f"IMPOSTO_{tipo_imp}",
                    "tipo_doc": "GUIA_TRIBUTO",
                    "numero_doc": nota_dict.get("numero_nf") or nota_dict.get("numero_tx"),
                    "favorecido": f"Guia de Retenção - {tipo_imp} ({nota_dict.get('fornecedor')})",
                    "cnpj": nota_dict.get("cnpj"),
                    "vencimento": venc_imp,
                    "valor": imp.get("valor", 0.0),
                    "valor_bruto": nota_dict.get("valor_bruto") or 0.0,
                    "historico": f"Vlr. ref. retenção de {tipo_imp} s/ doc {nota_dict.get('numero_nf')} de {nota_dict.get('fornecedor')}",
                    "descricao": f"Retenção Tributária {tipo_imp}",
                    "ccusto": nota_dict.get("filial") or "",
                    "solicitante": nota_dict.get("responsavel") or "",
                    "forma_pgto": "BOLETO",
                    "status": "CONCILIADO" if imp.get("status") == "PAGO" else "PENDENTE",
                    "loteId": nota_dict.get("numero_tx")
                })

        if status:
            titulos = [t for t in titulos if t["status"].upper() == status.upper()]

        if filtro_data:
            resultado_filtrado = []
            for t in titulos:
                v = t.get("vencimento")
                if not v:
                    continue
                try:
                    if "/" in v:
                        v_date = datetime.strptime(v, "%d/%m/%Y").date()
                    else:
                        v_date = datetime.strptime(v[:10], "%Y-%m-%d").date()

                    if filtro_data == "vencidos" and v_date < hoje_date and t["status"] == "PENDENTE":
                        resultado_filtrado.append(t)
                    elif filtro_data == "hoje" and v_date == hoje_date:
                        resultado_filtrado.append(t)
                    elif filtro_data == "semana" and hoje_date <= v_date <= semana_date:
                        resultado_filtrado.append(t)
                    elif filtro_data == "mes" and v_date.strftime("%Y-%m") == mes_atual_str:
                        resultado_filtrado.append(t)
                except Exception:
                    pass
            titulos = resultado_filtrado

        if busca:
            b_low = busca.lower()
            titulos = [t for t in titulos if b_low in str(t["favorecido"]).lower() or b_low in str(t["numero_doc"]).lower()]

        titulos.sort(key=lambda x: x.get("vencimento") or "9999-99-99")
        return {"success": True, "total": len(titulos), "titulos": titulos}

    except Exception as e:
        return {"success": False, "error": str(e), "titulos": []}

@router.get("/dashboard")
def dashboard_kpis():
    try:
        conn = get_connection()
        cur = conn.cursor()
        hoje = datetime.now().date()
        hoje_str = hoje.strftime("%Y-%m-%d")
        semana_str = (hoje + timedelta(days=7)).strftime("%Y-%m-%d")
        mes_ini = hoje.strftime("%Y-%m-01")
        mes_fim = hoje.strftime("%Y-%m-30")

        # Buscar todos os titulos nao-previsao
        cur.execute("""
            SELECT id, fornecedor, dt_vencimento, valor_bruto, valor_liquido,
                   status, conciliada, dt_pagamento
            FROM notas
            WHERE (is_previsao = 0 OR is_previsao IS NULL)
        """)
        rows = cur.fetchall()
        conn.close()

        total_aberto = 0.0
        total_vencido = 0.0
        total_hoje = 0.0
        total_semana = 0.0
        total_mes = 0.0
        total_baixado_mes = 0.0
        qtd_aberto = 0
        qtd_vencido = 0
        qtd_hoje = 0
        qtd_baixado = 0

        venc_map = {}  # data -> {total, qtd}
        forn_map = {}  # fornecedor -> {total, qtd}

        for r in rows:
            rd = dict(r)
            valor = rd.get("valor_liquido") or rd.get("valor_bruto") or 0.0
            venc = (rd.get("dt_vencimento") or "").strip()[:10]
            is_pago = rd.get("status") in ("PAGO", "CONCILIADO") or bool(rd.get("conciliada"))
            fornecedor = rd.get("fornecedor") or "Sem nome"

            # Normalizar data
            if venc and "/" in venc:
                parts = venc.split("/")
                if len(parts) == 3 and len(parts[2]) == 4:
                    venc = f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"

            # Top fornecedores (apenas abertos)
            if not is_pago:
                if fornecedor not in forn_map:
                    forn_map[fornecedor] = {"total": 0.0, "qtd": 0}
                forn_map[fornecedor]["total"] += valor
                forn_map[fornecedor]["qtd"] += 1

            if is_pago:
                qtd_baixado += 1
                # Baixado no mes
                dt_pgto = (rd.get("dt_pagamento") or venc or "")[:10]
                if dt_pgto >= mes_ini and dt_pgto <= mes_fim:
                    total_baixado_mes += valor
                continue

            # Titulo aberto
            qtd_aberto += 1
            total_aberto += valor

            if not venc:
                continue

            # Vencimentos por dia (proximos 14 dias)
            if venc >= hoje_str and venc <= (hoje + timedelta(days=14)).strftime("%Y-%m-%d"):
                if venc not in venc_map:
                    venc_map[venc] = {"total": 0.0, "qtd": 0}
                venc_map[venc]["total"] += valor
                venc_map[venc]["qtd"] += 1

            if venc < hoje_str:
                total_vencido += valor
                qtd_vencido += 1
            elif venc == hoje_str:
                total_hoje += valor
                qtd_hoje += 1

            if venc >= hoje_str and venc <= semana_str:
                total_semana += valor

            if venc >= mes_ini and venc <= mes_fim:
                total_mes += valor

        # Montar vencimentos 14 dias ordenados
        venc_14dias = []
        for i in range(15):
            d = (hoje + timedelta(days=i)).strftime("%Y-%m-%d")
            entry = venc_map.get(d, {"total": 0.0, "qtd": 0})
            venc_14dias.append({"data": d, "total": round(entry["total"], 2), "qtd": entry["qtd"]})

        # Top 10 fornecedores por valor
        top_forn = sorted(forn_map.items(), key=lambda x: x[1]["total"], reverse=True)[:10]
        top_fornecedores = [{"nome": k, "total": round(v["total"], 2), "qtd": v["qtd"]} for k, v in top_forn]

        return {
            "success": True,
            "kpis": {
                "total_aberto": round(total_aberto, 2),
                "total_vencido": round(total_vencido, 2),
                "total_vence_hoje": round(total_hoje, 2),
                "total_semana": round(total_semana, 2),
                "total_mes": round(total_mes, 2),
                "total_baixado_mes": round(total_baixado_mes, 2),
                "qtd_aberto": qtd_aberto,
                "qtd_vencido": qtd_vencido,
                "qtd_vence_hoje": qtd_hoje,
                "qtd_baixado": qtd_baixado
            },
            "vencimentos_14dias": venc_14dias,
            "top_fornecedores": top_fornecedores
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/gravar-documento")
@router.post("/titulos/gravar-documento")
def gravar_documento(doc: DocumentoEntrada):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM notas WHERE cnpj = ? AND numero_nf = ?",
            (doc.cnpj.strip(), doc.numero_doc.strip())
        )
        if cur.fetchone():
            conn.close()
            raise HTTPException(
                status_code=400,
                detail=f"Bloqueio de Duplicidade: O documento nº {doc.numero_doc} para o CNPJ {doc.cnpj} já está cadastrado."
            )

        tot_ret = sum(i.valor for i in doc.impostos)
        valor_liquido = max(0.0, round(doc.valor_bruto - tot_ret, 2))
        lote_id = f"TX_{int(time.time() * 100)}"

        cur.execute("""
            INSERT INTO notas (
                numero_tx, tipo, fornecedor, cnpj, dt_emissao, dt_vencimento,
                valor_bruto, valor_liquido, status, categoria, observacao,
                responsavel, descricao, filial, forma_pgto, cod_barras,
                pix_chave, numero_nf, cod_operacao, cnae, item_lc116, is_previsao, conciliada
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
        """, (
            lote_id,
            "FORNECEDOR" if doc.tipo_doc == "NFSE" else "DESPESA_GERAL",
            doc.favorecido.strip(),
            doc.cnpj.strip(),
            doc.data_emissao,
            doc.vencimento,
            doc.valor_bruto,
            valor_liquido,
            "PENDENTE",
            doc.tipo_doc,
            doc.historico,
            doc.solicitante,
            doc.descricao,
            doc.ccusto,
            doc.forma_pgto,
            doc.linha_dig,
            doc.dados_banco,
            doc.numero_doc.strip(),
            doc.cod_operacao or "1.933 - Aquisição de serviço tributado pelo ISSQN",
            doc.cnae or "",
            doc.item_lc116 or ""
        ))
        nota_id = cur.lastrowid

        for imp in doc.impostos:
            if imp.valor > 0:
                cur.execute("""
                    INSERT INTO nota_impostos (
                        nota_id, tipo, aliquota, valor, dt_venc_imp, status, numero_doc
                    ) VALUES (?, ?, ?, ?, ?, 'PENDENTE', ?)
                """, (
                    nota_id,
                    imp.tipo.upper(),
                    imp.aliquota,
                    imp.valor,
                    imp.dt_venc_imp or doc.vencimento,
                    doc.numero_doc.strip()
                ))

        # Auto-salvar/atualizar cadastro de fornecedor
        try:
            f_cnpj = doc.cnpj.strip() if doc.cnpj else ""
            f_razao = doc.favorecido.strip() if doc.favorecido else ""
            if f_razao:
                f_exist = None
                if f_cnpj:
                    cur.execute("SELECT id FROM fornecedores WHERE cnpj_cpf = ?", (f_cnpj,))
                    f_exist = cur.fetchone()
                if not f_exist:
                    cur.execute("SELECT id FROM fornecedores WHERE razao_social = ? COLLATE NOCASE", (f_razao,))
                    f_exist = cur.fetchone()

                if f_exist:
                    cur.execute("""
                        UPDATE fornecedores SET
                            razao_social = COALESCE(NULLIF(?, ''), razao_social),
                            cnpj_cpf = CASE WHEN (cnpj_cpf IS NULL OR cnpj_cpf = '') AND ? != '' THEN ? ELSE cnpj_cpf END,
                            categoria = COALESCE(NULLIF(?, ''), categoria),
                            ccusto = COALESCE(NULLIF(?, ''), ccusto),
                            responsavel = COALESCE(NULLIF(?, ''), responsavel),
                            forma_pgto = COALESCE(NULLIF(?, ''), forma_pgto),
                            dados_banco = COALESCE(NULLIF(?, ''), dados_banco),
                            cod_operacao = COALESCE(NULLIF(?, ''), cod_operacao),
                            cnae = COALESCE(NULLIF(?, ''), cnae),
                            item_lc116 = COALESCE(NULLIF(?, ''), item_lc116),
                            atualizado_em = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (
                        f_razao,
                        f_cnpj, f_cnpj,
                        doc.tipo_doc or "",
                        doc.ccusto or "",
                        doc.solicitante or "",
                        doc.forma_pgto or "",
                        doc.dados_banco or "",
                        doc.cod_operacao or "",
                        doc.cnae or "",
                        doc.item_lc116 or "",
                        f_exist["id"]
                    ))
                else:
                    cur.execute("""
                        INSERT INTO fornecedores (
                            razao_social, nome_fantasia, cnpj_cpf, tipo, categoria,
                            ccusto, responsavel, forma_pgto, dados_banco,
                            cod_operacao, cnae, item_lc116
                        ) VALUES (?, ?, ?, 'FORNECEDOR', ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f_razao,
                        f_razao,
                        f_cnpj if f_cnpj else None,
                        doc.tipo_doc or "",
                        doc.ccusto or "",
                        doc.solicitante or "",
                        doc.forma_pgto or "",
                        doc.dados_banco or "",
                        doc.cod_operacao or "",
                        doc.cnae or "",
                        doc.item_lc116 or ""
                    ))
        except Exception as e_forn:
            logger.warning("Erro ao auto-salvar fornecedor: %s", e_forn)

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": "Documento e retenções tributárias gravadas com sucesso no SQLite!",
            "nota_id": nota_id,
            "lote_tx": lote_id,
            "valor_liquido": valor_liquido,
            "impostos_gravados": len(doc.impostos)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/{identificador}/baixa")
@router.post("/titulos/{identificador}/baixa")
def alternar_baixa(identificador: str, forcar_baixa: Optional[bool] = Query(False)):
    try:
        conn = get_connection()
        cur = conn.cursor()
        hoje_str = datetime.now().strftime("%Y-%m-%d")

        if identificador.startswith("IMP_"):
            imp_id = int(identificador.replace("IMP_", ""))
            cur.execute("SELECT status FROM nota_impostos WHERE id = ?", (imp_id,))
            row = cur.fetchone()
            if not row:
                conn.close()
                raise HTTPException(status_code=404, detail="Imposto não localizado.")
            novo_status = "PAGO" if forcar_baixa else ("PENDENTE" if row["status"] == "PAGO" else "PAGO")
            cur.execute("UPDATE nota_impostos SET status = ? WHERE id = ?", (novo_status, imp_id))
        else:
            clean_id = identificador.replace("NOTA_", "").strip()
            row = None
            nota_id = None
            if clean_id.isdigit():
                nota_id = int(clean_id)
                cur.execute("SELECT id, status FROM notas WHERE id = ?", (nota_id,))
                row = cur.fetchone()
            
            if not row:
                cur.execute("SELECT id, status FROM notas WHERE numero_nf = ? OR numero_tx = ?", (identificador, identificador))
                row = cur.fetchone()
                if row:
                    nota_id = row["id"]

            if not row:
                conn.close()
                raise HTTPException(status_code=404, detail="Título não localizado.")

            novo_status = "CONCILIADO" if forcar_baixa else ("PENDENTE" if row["status"] in ("PAGO", "CONCILIADO") else "CONCILIADO")
            cur.execute("""
                UPDATE notas
                SET status = ?, conciliada = ?, dt_pagamento = ?
                WHERE id = ?
            """, (novo_status, 1 if novo_status == "CONCILIADO" else 0, hoje_str if novo_status == "CONCILIADO" else None, nota_id))

        conn.commit()
        conn.close()
        return {"success": True, "novo_status": novo_status}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{identificador}")
@router.delete("/titulos/{identificador}")
def excluir_titulo(identificador: str):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if identificador.startswith("IMP_"):
            imp_id = int(identificador.replace("IMP_", ""))
            cur.execute("DELETE FROM nota_impostos WHERE id = ?", (imp_id,))
        else:
            nota_id = int(identificador.replace("NOTA_", ""))
            cur.execute("DELETE FROM nota_impostos WHERE nota_id = ?", (nota_id,))
            cur.execute("DELETE FROM notas WHERE id = ?", (nota_id,))

        conn.commit()
        conn.close()
        return {"success": True, "message": "Título excluído com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TituloEdicao(BaseModel):
    numero_doc: Optional[str] = None
    favorecido: Optional[str] = None
    cnpj: Optional[str] = None
    cod_operacao: Optional[str] = None
    cnae: Optional[str] = None
    item_lc116: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    historico: Optional[str] = None
    ccusto: Optional[str] = None
    solicitante: Optional[str] = None
    vencimento: Optional[str] = None
    data_emissao: Optional[str] = None
    valor: Optional[float] = None
    forma_pgto: Optional[str] = None
    linha_dig: Optional[str] = None
    dados_banco: Optional[str] = None

@router.put("/{identificador}")
@router.put("/titulos/{identificador}")
@router.post("/{identificador}/editar")
@router.post("/titulos/{identificador}/editar")
def editar_titulo(identificador: str, dados: TituloEdicao):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if identificador.startswith("IMP_"):
            imp_id = int(identificador.replace("IMP_", ""))
            cur.execute("SELECT * FROM nota_impostos WHERE id = ?", (imp_id,))
            row = cur.fetchone()
            if not row:
                conn.close()
                raise HTTPException(status_code=404, detail="Imposto não localizado.")

            cur.execute("""
                UPDATE nota_impostos
                SET valor = COALESCE(?, valor),
                    dt_venc_imp = COALESCE(?, dt_venc_imp),
                    numero_doc = COALESCE(?, numero_doc)
                WHERE id = ?
            """, (dados.valor, dados.vencimento, dados.numero_doc, imp_id))
        else:
            clean_id = identificador.replace("NOTA_", "").strip()
            nota_id = None
            if clean_id.isdigit():
                nota_id = int(clean_id)
            else:
                cur.execute("SELECT id FROM notas WHERE numero_nf = ? OR numero_tx = ?", (identificador, identificador))
                r = cur.fetchone()
                if r:
                    nota_id = r["id"]

            if not nota_id:
                conn.close()
                raise HTTPException(status_code=404, detail="Título não localizado.")

            cur.execute("""
                UPDATE notas
                SET fornecedor = COALESCE(?, fornecedor),
                    cnpj = COALESCE(?, cnpj),
                    numero_nf = COALESCE(?, numero_nf),
                    dt_vencimento = COALESCE(?, dt_vencimento),
                    dt_emissao = COALESCE(?, dt_emissao),
                    valor_bruto = COALESCE(?, valor_bruto),
                    valor_liquido = COALESCE(?, valor_liquido),
                    categoria = COALESCE(?, categoria),
                    descricao = COALESCE(?, descricao),
                    observacao = COALESCE(?, observacao),
                    filial = COALESCE(?, filial),
                    responsavel = COALESCE(?, responsavel),
                    forma_pgto = COALESCE(?, forma_pgto),
                    cod_barras = COALESCE(?, cod_barras),
                    cod_operacao = COALESCE(?, cod_operacao),
                    cnae = COALESCE(?, cnae),
                    item_lc116 = COALESCE(?, item_lc116)
                WHERE id = ?
            """, (
                dados.favorecido.strip() if dados.favorecido else None,
                dados.cnpj.strip() if dados.cnpj else None,
                dados.numero_doc.strip() if dados.numero_doc else None,
                dados.vencimento if dados.vencimento else None,
                dados.data_emissao if dados.data_emissao else None,
                dados.valor if dados.valor is not None else None,
                dados.valor if dados.valor is not None else None,
                dados.categoria if dados.categoria else None,
                dados.descricao if dados.descricao else None,
                dados.historico if dados.historico else None,
                dados.ccusto if dados.ccusto else None,
                dados.solicitante if dados.solicitante else None,
                dados.forma_pgto if dados.forma_pgto else None,
                dados.linha_dig if dados.linha_dig else None,
                dados.cod_operacao if dados.cod_operacao else None,
                dados.cnae if dados.cnae else None,
                dados.item_lc116 if dados.item_lc116 else None,
                nota_id
            ))

            # Sincronizar dados do fornecedor se alterados
            if dados.favorecido:
                try:
                    f_cnpj = dados.cnpj.strip() if dados.cnpj else ""
                    f_razao = dados.favorecido.strip()
                    f_exist = None
                    if f_cnpj:
                        cur.execute("SELECT id FROM fornecedores WHERE cnpj_cpf = ?", (f_cnpj,))
                        f_exist = cur.fetchone()
                    if not f_exist:
                        cur.execute("SELECT id FROM fornecedores WHERE razao_social = ? COLLATE NOCASE", (f_razao,))
                        f_exist = cur.fetchone()

                    if f_exist:
                        cur.execute("""
                            UPDATE fornecedores SET
                                razao_social = COALESCE(NULLIF(?, ''), razao_social),
                                cnpj_cpf = CASE WHEN (cnpj_cpf IS NULL OR cnpj_cpf = '') AND ? != '' THEN ? ELSE cnpj_cpf END,
                                categoria = COALESCE(NULLIF(?, ''), categoria),
                                ccusto = COALESCE(NULLIF(?, ''), ccusto),
                                responsavel = COALESCE(NULLIF(?, ''), responsavel),
                                forma_pgto = COALESCE(NULLIF(?, ''), forma_pgto),
                                cod_operacao = COALESCE(NULLIF(?, ''), cod_operacao),
                                cnae = COALESCE(NULLIF(?, ''), cnae),
                                item_lc116 = COALESCE(NULLIF(?, ''), item_lc116),
                                atualizado_em = CURRENT_TIMESTAMP
                            WHERE id = ?
                        """, (
                            f_razao,
                            f_cnpj, f_cnpj,
                            dados.categoria or "",
                            dados.ccusto or "",
                            dados.solicitante or "",
                            dados.forma_pgto or "",
                            dados.cod_operacao or "",
                            dados.cnae or "",
                            dados.item_lc116 or "",
                            f_exist["id"]
                        ))
                    else:
                        cur.execute("""
                            INSERT INTO fornecedores (
                                razao_social, nome_fantasia, cnpj_cpf, tipo, categoria,
                                ccusto, responsavel, forma_pgto, cod_operacao, cnae, item_lc116
                            ) VALUES (?, ?, ?, 'FORNECEDOR', ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            f_razao,
                            f_razao,
                            f_cnpj if f_cnpj else None,
                            dados.categoria or "",
                            dados.ccusto or "",
                            dados.solicitante or "",
                            dados.forma_pgto or "",
                            dados.cod_operacao or "",
                            dados.cnae or "",
                            dados.item_lc116 or ""
                        ))
                except Exception as e_forn:
                    logger.warning("Erro ao auto-salvar fornecedor: %s", e_forn)

        conn.commit()
        conn.close()
        return {"success": True, "message": "Título atualizado com sucesso!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ==============================================================================
# NOVAS ROTAS INTEGRADAS: REMESSA ITAÚ SISPAG, CONCILIAÇÃO OFX E WHATSAPP
# ==============================================================================
from fastapi import Response, UploadFile, File
import requests
from ..core.itau_sispag import gerar_cnab240_sispag_itau

@router.get("/exportar-lote-itau")
@router.post("/exportar-lote-itau")
def exportar_lote_itau(
    data_pagamento: Optional[str] = Query(None, description="Data de pagamento (YYYY-MM-DD)"),
    filial: Optional[str] = Query(None)
):
    """
    Gera arquivo de remessa CNAB 240 / SISPAG Itaú contendo todos os títulos
    em aberto com linha digitável/código de barras para a data especificada.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id, numero_tx, numero_nf, fornecedor, cnpj, dt_emissao, dt_vencimento,
                   valor_bruto, valor_liquido, status, categoria, filial, forma_pgto,
                   cod_barras, pix_chave
            FROM notas
            WHERE (is_previsao = 0 OR is_previsao IS NULL)
              AND (status = 'PENDENTE' OR status = 'EM ABERTO' OR status IS NULL OR status = '' OR status = 'ABERTO')
        """
        params = []
        if data_pagamento:
            query += " AND (dt_vencimento LIKE ? OR dt_vencimento = ?)"
            params.extend([f"{data_pagamento}%", data_pagamento])
        if filial:
            query += " AND filial = ?"
            params.append(filial)
            
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        conn.close()
        
        titulos = [dict(r) for r in rows]
        if not titulos:
            # Se não achou na data exata, busca todos os abertos
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, numero_tx, numero_nf, fornecedor, cnpj, dt_emissao, dt_vencimento,
                       valor_bruto, valor_liquido, status, categoria, filial, forma_pgto,
                       cod_barras, pix_chave
                FROM notas
                WHERE (is_previsao = 0 OR is_previsao IS NULL)
                  AND (status = 'PENDENTE' OR status = 'EM ABERTO' OR status IS NULL OR status = '' OR status = 'ABERTO')
                LIMIT 50
            """)
            titulos = [dict(r) for r in cur.fetchall()]
            conn.close()
            
        if not titulos:
            raise HTTPException(status_code=404, detail="Nenhum título em aberto encontrado para gerar o lote.")
            
        dt_pgto = data_pagamento or datetime.now().strftime("%Y-%m-%d")
        remessa_conteudo = gerar_cnab240_sispag_itau(titulos, data_pagamento=dt_pgto)
        
        nome_arquivo = f"LOTE_ITAU_{dt_pgto.replace('-', '')}.REM"
        return Response(
            content=remessa_conteudo,
            media_type="text/plain",
            headers={
                "Content-Disposition": f'attachment; filename="{nome_arquivo}"',
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erro ao gerar lote Itaú: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conciliar-ofx")
async def conciliar_extrato_ofx(arquivo: UploadFile = File(...)):
    """
    Recebe um arquivo OFX do Itaú, extrai os débitos de pagamentos
    e dá baixa automática nos títulos correspondentes.
    Estratégias de match (em ordem):
      1. Valor exato (±R$ 0,05)
      2. Soma de 2-3 títulos pendentes
      3. Tolerância de juros (até 5%)
    """
    try:
        import ofxparse
        import io
        conteudo = await arquivo.read()
        ofx = ofxparse.OfxParser.parse(io.BytesIO(conteudo))
        
        debitos_encontrados = []
        for account in ofx.accounts:
            for tx in account.statement.transactions:
                if tx.amount < 0:
                    debitos_encontrados.append({
                        "data": tx.date.strftime("%Y-%m-%d"),
                        "valor": abs(float(tx.amount)),
                        "descricao": tx.memo or "",
                        "checknum": tx.checknum or tx.id or "",
                        "fitid": tx.id or ""
                    })
                    
        conn = get_connection()
        cur = conn.cursor()
        
        titulos_baixados = []
        titulos_baixados_soma = []
        titulos_baixados_juros = []
        nao_localizados = []
        hoje_str = datetime.now().strftime("%Y-%m-%d")

        # Carrega todos os títulos pendentes uma vez
        cur.execute("""
            SELECT id, fornecedor, dt_vencimento, valor_liquido, valor_bruto, numero_nf
            FROM notas
            WHERE (status = 'PENDENTE' OR status = 'EM ABERTO' OR status IS NULL OR status = '' OR status = 'ABERTO')
              AND (is_previsao = 0 OR is_previsao IS NULL)
        """)
        pendentes = [dict(r) for r in cur.fetchall()]
        ids_usados = set()
        
        for deb in debitos_encontrados:
            val = deb["valor"]
            dt = deb["data"]
            matched = False
            
            # === ESTRATÉGIA 1: Match exato por valor (±R$ 0,05) ===
            for p in pendentes:
                if p["id"] in ids_usados:
                    continue
                v_liq = p.get("valor_liquido") or 0
                v_bru = p.get("valor_bruto") or 0
                if abs(round(v_liq, 2) - round(val, 2)) < 0.06 or abs(round(v_bru, 2) - round(val, 2)) < 0.06:
                    tit_id = p["id"]
                    cur.execute("""
                        UPDATE notas
                        SET status = 'PAGO', conciliada = 1, dt_pagamento = ?, valor_pago = ?
                        WHERE id = ?
                    """, (dt, val, tit_id))
                    ids_usados.add(tit_id)
                    titulos_baixados.append({
                        "id": tit_id, "fornecedor": p["fornecedor"],
                        "numero_nf": p["numero_nf"], "valor": val,
                        "dt_pagamento": dt, "descricao_banco": deb["descricao"],
                        "match_tipo": "EXATO"
                    })
                    matched = True
                    break
            
            if matched:
                continue
            
            # === ESTRATÉGIA 2: Match por soma de 2-3 títulos ===
            disponiveis = [p for p in pendentes if p["id"] not in ids_usados]
            found_combo = False
            for n in (2, 3):
                if found_combo or len(disponiveis) < n:
                    break
                for combo in combinations(disponiveis, n):
                    soma = sum((c.get("valor_liquido") or c.get("valor_bruto") or 0) for c in combo)
                    if abs(round(soma, 2) - round(val, 2)) < 0.11:
                        grupo_id = f"GRP_{int(time.time() * 1000)}_{deb.get('fitid', '')}"
                        combo_ids = [c["id"] for c in combo]
                        for c in combo:
                            cur.execute("""
                                UPDATE notas
                                SET status = 'PAGO', conciliada = 1, dt_pagamento = ?,
                                    valor_pago = ?, grupo_conciliacao = ?
                                WHERE id = ?
                            """, (dt, val, grupo_id, c["id"]))
                            ids_usados.add(c["id"])
                        # Registrar grupo
                        cur.execute("""
                            INSERT INTO conciliacao_grupos
                                (id, extrato_fitid, extrato_valor, extrato_data, extrato_memo,
                                 soma_titulos, diferenca, tipo_diferenca, qtd_titulos, operador)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (grupo_id, deb.get("fitid", ""), val, dt,
                              deb["descricao"], round(soma, 2),
                              round(val - soma, 2), None, n, "Sistema (Auto OFX)"))
                        titulos_baixados_soma.append({
                            "grupo_id": grupo_id, "titulo_ids": combo_ids,
                            "soma_titulos": round(soma, 2), "valor_extrato": val,
                            "dt_pagamento": dt, "descricao_banco": deb["descricao"],
                            "match_tipo": "SOMA"
                        })
                        found_combo = True
                        break
            
            if found_combo:
                continue
            
            # === ESTRATÉGIA 3: Match com tolerância de juros (até 5%) ===
            for p in pendentes:
                if p["id"] in ids_usados:
                    continue
                v_ref = p.get("valor_liquido") or p.get("valor_bruto") or 0
                if v_ref <= 0:
                    continue
                diff = val - v_ref
                pct = abs(diff / v_ref) * 100
                if 0.06 < abs(diff) and pct <= 5.0:
                    tit_id = p["id"]
                    tipo_dif = "JUROS" if diff > 0 else "DESCONTO"
                    cur.execute("""
                        UPDATE notas
                        SET status = 'PAGO', conciliada = 1, dt_pagamento = ?,
                            valor_pago = ?, juros_multa = ?, desconto = ?
                        WHERE id = ?
                    """, (dt, val,
                          round(diff, 2) if diff > 0 else 0,
                          round(abs(diff), 2) if diff < 0 else 0,
                          tit_id))
                    ids_usados.add(tit_id)
                    titulos_baixados_juros.append({
                        "id": tit_id, "fornecedor": p["fornecedor"],
                        "numero_nf": p["numero_nf"],
                        "valor_titulo": v_ref, "valor_pago": val,
                        "diferenca": round(diff, 2),
                        "tipo_diferenca": tipo_dif,
                        "percentual": round(pct, 2),
                        "dt_pagamento": dt, "descricao_banco": deb["descricao"],
                        "match_tipo": "JUROS_TOLERANCIA"
                    })
                    matched = True
                    break
            
            if not matched:
                nao_localizados.append(deb)
                
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "total_debitos_ofx": len(debitos_encontrados),
            "total_conciliados_exato": len(titulos_baixados),
            "total_conciliados_soma": len(titulos_baixados_soma),
            "total_conciliados_juros": len(titulos_baixados_juros),
            "total_conciliados": len(titulos_baixados) + len(titulos_baixados_soma) + len(titulos_baixados_juros),
            "titulos_baixados": titulos_baixados,
            "titulos_baixados_soma": titulos_baixados_soma,
            "titulos_baixados_juros": titulos_baixados_juros,
            "nao_localizados": nao_localizados
        }
    except Exception as e:
        logger.exception("Erro ao conciliar OFX: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== NOVAS ROTAS: CONCILIAÇÃO AVANÇADA ====================

@router.get("/titulos-pendentes-para-conciliacao")
def listar_pendentes_conciliacao(
    valor_aprox: Optional[float] = Query(None, description="Valor aproximado para filtrar"),
    fornecedor: Optional[str] = Query(None, description="Filtro por nome de fornecedor"),
    tolerancia_pct: Optional[float] = Query(50.0, description="Tolerância % para filtro por valor")
):
    """
    Retorna títulos pendentes para uso no modal de vinculação manual
    da conciliação bancária. Suporta filtros por valor aproximado e fornecedor.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, fornecedor, cnpj, dt_vencimento, valor_liquido, valor_bruto,
                   numero_nf, descricao, categoria, forma_pgto
            FROM notas
            WHERE (status = 'PENDENTE' OR status = 'EM ABERTO' OR status IS NULL
                   OR status = '' OR status = 'ABERTO')
              AND (is_previsao = 0 OR is_previsao IS NULL)
            ORDER BY dt_vencimento ASC
        """)
        rows = cur.fetchall()
        conn.close()

        resultados = []
        for r in rows:
            rd = dict(r)
            v = rd.get("valor_liquido") or rd.get("valor_bruto") or 0

            # Filtro por valor aproximado
            if valor_aprox is not None and valor_aprox > 0 and v > 0:
                diff_pct = abs(v - valor_aprox) / valor_aprox * 100
                if diff_pct > tolerancia_pct:
                    continue

            # Filtro por fornecedor
            if fornecedor:
                nome = (rd.get("fornecedor") or "").lower()
                if fornecedor.lower() not in nome:
                    continue

            resultados.append({
                "id": rd["id"],
                "fornecedor": rd.get("fornecedor"),
                "cnpj": rd.get("cnpj"),
                "vencimento": rd.get("dt_vencimento"),
                "valor": v,
                "valor_bruto": rd.get("valor_bruto") or 0,
                "numero_nf": rd.get("numero_nf"),
                "descricao": rd.get("descricao"),
                "categoria": rd.get("categoria"),
            })

        return {"success": True, "total": len(resultados), "titulos": resultados}
    except Exception as e:
        logger.exception("Erro ao listar pendentes para conciliação: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conciliar-grupo")
def conciliar_grupo(req: ConciliacaoGrupoRequest):
    """
    Vincula N títulos do sistema a 1 débito do extrato bancário.
    Registra o agrupamento, calcula diferença (juros/multa/desconto),
    e dá baixa em todos os títulos vinculados.
    """
    try:
        if not req.titulo_ids:
            raise HTTPException(status_code=400, detail="Nenhum título informado")

        conn = get_connection()
        cur = conn.cursor()
        hoje_str = datetime.now().strftime("%Y-%m-%d")
        dt_pgto = req.extrato_data or hoje_str

        # Buscar títulos e calcular soma
        placeholders = ",".join(["?" for _ in req.titulo_ids])
        cur.execute(f"""
            SELECT id, fornecedor, valor_liquido, valor_bruto, numero_nf
            FROM notas WHERE id IN ({placeholders})
        """, tuple(req.titulo_ids))
        titulos_encontrados = [dict(r) for r in cur.fetchall()]

        if len(titulos_encontrados) != len(req.titulo_ids):
            ids_encontrados = {t["id"] for t in titulos_encontrados}
            ids_faltando = [i for i in req.titulo_ids if i not in ids_encontrados]
            raise HTTPException(status_code=404,
                detail=f"Títulos não encontrados: {ids_faltando}")

        soma = sum((t.get("valor_liquido") or t.get("valor_bruto") or 0) for t in titulos_encontrados)
        diferenca = round(req.extrato_valor - soma, 2)

        # Determinar tipo da diferença automaticamente se não informado
        tipo_dif = req.tipo_diferenca
        if tipo_dif is None and abs(diferenca) > 0.05:
            tipo_dif = "JUROS" if diferenca > 0 else "DESCONTO"

        # Gerar ID do grupo
        grupo_id = f"GRP_{int(time.time() * 1000)}"

        # Registrar grupo de conciliação
        cur.execute("""
            INSERT INTO conciliacao_grupos
                (id, extrato_fitid, extrato_valor, extrato_data, extrato_memo,
                 soma_titulos, diferenca, tipo_diferenca, qtd_titulos, operador)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (grupo_id, req.extrato_fitid, req.extrato_valor, dt_pgto,
              req.extrato_memo, round(soma, 2), diferenca, tipo_dif,
              len(req.titulo_ids), req.operador))

        # Dar baixa em cada título
        juros_val = round(diferenca, 2) if diferenca > 0 else 0
        desc_val = round(abs(diferenca), 2) if diferenca < 0 else 0

        titulos_result = []
        for t in titulos_encontrados:
            cur.execute("""
                UPDATE notas
                SET status = 'PAGO', conciliada = 1, dt_pagamento = ?,
                    valor_pago = ?, juros_multa = ?, desconto = ?,
                    grupo_conciliacao = ?
                WHERE id = ?
            """, (dt_pgto, req.extrato_valor, juros_val, desc_val,
                  grupo_id, t["id"]))
            titulos_result.append({
                "id": t["id"],
                "fornecedor": t["fornecedor"],
                "numero_nf": t["numero_nf"],
                "valor_titulo": t.get("valor_liquido") or t.get("valor_bruto") or 0
            })

        conn.commit()
        conn.close()

        logger.info("Conciliação em grupo: %s — %d títulos, extrato R$ %.2f, soma R$ %.2f, dif R$ %.2f (%s)",
                     grupo_id, len(req.titulo_ids), req.extrato_valor, soma, diferenca, tipo_dif or "SEM_DIF")

        return {
            "success": True,
            "grupo_id": grupo_id,
            "qtd_titulos": len(req.titulo_ids),
            "soma_titulos": round(soma, 2),
            "valor_extrato": req.extrato_valor,
            "diferenca": diferenca,
            "tipo_diferenca": tipo_dif,
            "titulos": titulos_result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erro ao conciliar grupo: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/disparar-whatsapp-diretoria")
def disparar_whatsapp_diretoria(
    numero: Optional[str] = Query("557191045869", description="Número com DDI+DDD"),
    data_pagamento: Optional[str] = Query(None)
):
    """
    Gera o resumo consolidado de títulos a pagar e envia via WhatsApp.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        hoje_str = data_pagamento or datetime.now().strftime("%Y-%m-%d")
        
        cur.execute("""
            SELECT id, fornecedor, dt_vencimento, valor_liquido, valor_bruto, forma_pgto
            FROM notas
            WHERE (is_previsao = 0 OR is_previsao IS NULL)
              AND (status = 'PENDENTE' OR status = 'EM ABERTO' OR status IS NULL OR status = '' OR status = 'ABERTO')
              AND (dt_vencimento LIKE ? OR dt_vencimento = ?)
        """, (f"{hoje_str}%", hoje_str))
        
        rows = cur.fetchall()
        conn.close()
        
        titulos = [dict(r) for r in rows]
        total_despesas = sum(float(t.get("valor_liquido") or t.get("valor_bruto") or 0.0) for t in titulos)
        
        msg = (
            f"📊 *BOAH FINANCEIRO - AUTORIZAÇÃO DE PAGAMENTOS*\n"
            f"📅 *Data:* {hoje_str}\n\n"
            f"📉 *Total a Pagar:* R$ {total_despesas:,.2f}\n"
            f"📑 *Quantidade de Títulos:* {len(titulos)}\n\n"
            f"✅ Acesse o Bimer Cloud para conferência e aprovação:\n"
            f"https://bimer-cloud-app.vercel.app/\n"
        )
        
        resp = requests.post("http://localhost:3333/send-text", json={
            "number": numero,
            "message": msg
        }, timeout=10)
        
        return {
            "success": True,
            "mensagem_enviada": msg,
            "whatsapp_status": resp.json() if resp.status_code == 200 else resp.text
        }
    except Exception as e:
        logger.exception("Erro ao disparar WhatsApp: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
