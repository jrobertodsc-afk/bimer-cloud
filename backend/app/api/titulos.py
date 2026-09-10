from typing import Optional, List
import time
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from ..core.database import get_connection

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

        try:
            cur.execute("ALTER TABLE notas ADD COLUMN cod_operacao TEXT")
            conn.commit()
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE notas ADD COLUMN cnae TEXT")
            conn.commit()
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE notas ADD COLUMN item_lc116 TEXT")
            conn.commit()
        except Exception:
            pass

        cur.execute("""
            SELECT id, numero_tx, numero_nf, fornecedor, cnpj, dt_emissao, dt_vencimento,
                   valor_bruto, valor_liquido, status, categoria, filial, responsavel,
                   descricao, forma_pgto, cod_barras, pix_chave, observacao,
                   conciliada, dt_pagamento, cod_operacao, cnae, item_lc116
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
            n_venc = nota_dict["dt_vencimento"] or ""
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
                "loteId": nota_dict.get("numero_tx")
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

        try:
            cur.execute("ALTER TABLE notas ADD COLUMN cnae TEXT")
            conn.commit()
        except Exception:
            pass
        try:
            cur.execute("ALTER TABLE notas ADD COLUMN item_lc116 TEXT")
            conn.commit()
        except Exception:
            pass

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

        # Garantir colunas
        for col in ["cod_operacao", "cnae", "item_lc116"]:
            try:
                cur.execute(f"ALTER TABLE notas ADD COLUMN {col} TEXT")
                conn.commit()
            except Exception:
                pass

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

        conn.commit()
        conn.close()
        return {"success": True, "message": "Título atualizado com sucesso!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))