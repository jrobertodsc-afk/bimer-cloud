import sqlite3
import os
import sys

def backfill_fornecedores():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_paths = [
        os.path.join(base_dir, "database", "bimer.db"),
        os.path.join(base_dir, "backend", "bimer.db")
    ]
    robo_db_path = r"C:\Users\Roberto\Documents\antigravity\excited-bardeen\ROBO\robo_boah.db"

    ddl = """
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        razao_social TEXT NOT NULL,
        nome_fantasia TEXT,
        cnpj_cpf TEXT UNIQUE,
        tipo TEXT DEFAULT 'FORNECEDOR',
        categoria TEXT,
        ccusto TEXT,
        responsavel TEXT,
        forma_pgto TEXT,
        pix_chave TEXT,
        dados_banco TEXT,
        cod_operacao TEXT,
        cnae TEXT,
        item_lc116 TEXT,
        ativo INTEGER DEFAULT 1,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """

    # 1. Carregar fornecedores do robo_boah.db se existir
    fornecedores_robo = []
    if os.path.exists(robo_db_path):
        try:
            conn_robo = sqlite3.connect(robo_db_path)
            conn_robo.row_factory = sqlite3.Row
            cur_robo = conn_robo.cursor()
            cur_robo.execute("SELECT * FROM fornecedores")
            fornecedores_robo = [dict(r) for r in cur_robo.fetchall()]
            conn_robo.close()
            print(f"Carregados {len(fornecedores_robo)} fornecedores de robo_boah.db")
        except Exception as e:
            print(f"Erro ao ler robo_boah.db: {e}")

    for db_path in db_paths:
        if not os.path.exists(db_path):
            continue
        print(f"\nProcessando banco: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.executescript(ddl)
        conn.commit()

        inseridos_robo = 0
        for f in fornecedores_robo:
            razao = (f.get("razao_social") or "").strip()
            cnpj = (f.get("cnpj_cpf") or "").strip()
            if not razao and not cnpj:
                continue
            
            nome_fantasia = (f.get("nome_fantasia") or "").strip()
            tipo = f.get("tipo") or "FORNECEDOR"
            categoria = f.get("categoria") or ""
            responsavel = f.get("responsavel") or ""
            ccusto = f.get("filial_padrao") or f.get("empresa") or ""
            ativo = f.get("ativo", 1)

            try:
                cur.execute("""
                    INSERT INTO fornecedores (
                        razao_social, nome_fantasia, cnpj_cpf, tipo, categoria, ccusto, responsavel, ativo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(cnpj_cpf) DO UPDATE SET
                        razao_social = excluded.razao_social,
                        nome_fantasia = COALESCE(NULLIF(excluded.nome_fantasia, ''), fornecedores.nome_fantasia),
                        categoria = COALESCE(NULLIF(excluded.categoria, ''), fornecedores.categoria),
                        ccusto = COALESCE(NULLIF(excluded.ccusto, ''), fornecedores.ccusto),
                        responsavel = COALESCE(NULLIF(excluded.responsavel, ''), fornecedores.responsavel)
                """, (razao, nome_fantasia, cnpj if cnpj else None, tipo, categoria, ccusto, responsavel, ativo))
                inseridos_robo += 1
            except Exception as e:
                print(f"Erro ao inserir do robo {razao}: {e}")

        conn.commit()
        print(f"  {inseridos_robo} registros importados/atualizados do robo_boah.db")

        # 2. Carregar e mesclar fornecedores da tabela notas
        cur.execute("""
            SELECT fornecedor, cnpj, categoria, filial, responsavel, forma_pgto, pix_chave,
                   banco_dest, agencia_dest, conta_dest
            FROM notas
            WHERE fornecedor IS NOT NULL AND TRIM(fornecedor) != ''
            ORDER BY id DESC
        """)
        notas = [dict(r) for r in cur.fetchall()]
        print(f"  Analisando {len(notas)} lancamentos de notas...")

        inseridos_notas = 0
        atualizados_notas = 0
        for n in notas:
            razao = (n.get("fornecedor") or "").strip()
            cnpj = (n.get("cnpj") or "").strip()
            if not razao:
                continue

            categoria = n.get("categoria") or ""
            ccusto = n.get("filial") or ""
            responsavel = n.get("responsavel") or ""
            forma_pgto = n.get("forma_pgto") or ""
            pix_chave = n.get("pix_chave") or ""

            banco_info = ""
            if n.get("banco_dest") or n.get("agencia_dest") or n.get("conta_dest"):
                banco_info = f"Bco: {n.get('banco_dest') or ''} Ag: {n.get('agencia_dest') or ''} CC: {n.get('conta_dest') or ''}".strip()

            cur.execute("SELECT id, razao_social, cnpj_cpf, categoria, ccusto, forma_pgto, pix_chave FROM fornecedores WHERE (cnpj_cpf IS NOT NULL AND cnpj_cpf != '' AND cnpj_cpf = ?) OR (razao_social = ? COLLATE NOCASE)", (cnpj, razao))
            existente = cur.fetchone()

            if existente:
                cur.execute("""
                    UPDATE fornecedores SET
                        categoria = CASE WHEN categoria IS NULL OR categoria = '' THEN ? ELSE categoria END,
                        ccusto = CASE WHEN ccusto IS NULL OR ccusto = '' THEN ? ELSE ccusto END,
                        responsavel = CASE WHEN responsavel IS NULL OR responsavel = '' THEN ? ELSE responsavel END,
                        forma_pgto = CASE WHEN forma_pgto IS NULL OR forma_pgto = '' THEN ? ELSE forma_pgto END,
                        pix_chave = CASE WHEN pix_chave IS NULL OR pix_chave = '' THEN ? ELSE pix_chave END,
                        dados_banco = CASE WHEN dados_banco IS NULL OR dados_banco = '' THEN ? ELSE dados_banco END,
                        cnpj_cpf = CASE WHEN (cnpj_cpf IS NULL OR cnpj_cpf = '') AND ? != '' THEN ? ELSE cnpj_cpf END,
                        atualizado_em = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (categoria, ccusto, responsavel, forma_pgto, pix_chave, banco_info, cnpj, cnpj, existente["id"]))
                atualizados_notas += 1
            else:
                cur.execute("""
                    INSERT INTO fornecedores (
                        razao_social, nome_fantasia, cnpj_cpf, tipo, categoria, ccusto, responsavel, forma_pgto, pix_chave, dados_banco
                    ) VALUES (?, ?, ?, 'FORNECEDOR', ?, ?, ?, ?, ?, ?)
                """, (razao, razao, cnpj if cnpj else None, categoria, ccusto, responsavel, forma_pgto, pix_chave, banco_info))
                inseridos_notas += 1

        conn.commit()
        print(f"  Notas processadas: {inseridos_notas} novos fornecedores inseridos, {atualizados_notas} enriquecidos.")

        cur.execute("SELECT COUNT(*) as total FROM fornecedores")
        total = cur.fetchone()["total"]
        print(f"  Total final de fornecedores cadastrados em {os.path.basename(db_path)}: {total}")
        conn.close()

if __name__ == "__main__":
    backfill_fornecedores()
