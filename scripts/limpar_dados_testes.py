import os
import sys
import shutil
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.core.database import get_connection

# 1. Backup local
src_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "bimer.db"))
if os.path.exists(src_db):
    shutil.copy2(src_db, src_db + ".backup_testes")
    print(f"?? Backup local criado: {src_db}.backup_testes")

# 2. Limpar Turso
conn = get_connection()
cur = conn.cursor()
tabelas = ['nota_impostos', 'adiantamento_comprovantes', 'adiantamentos', 'notas', 'audit_log']
for t in tabelas:
    cur.execute(f"DELETE FROM {t}")
    print(f"??? Turso: Registros apagados da tabela [{t}]")

try:
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('notas', 'nota_impostos', 'adiantamentos', 'adiantamento_comprovantes', 'audit_log')")
    print("?? Turso: Contadores de ID resetados para 1.")
except Exception as e:
    print("Aviso sequence Turso:", e)

# 3. Limpar bancos locais para manter consistencia
for local_rel in ["database/bimer.db", "backend/bimer.db"]:
    lp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", local_rel))
    if os.path.exists(lp):
        c_loc = sqlite3.connect(lp)
        for t in tabelas:
            c_loc.execute(f"DELETE FROM {t}")
        try:
            c_loc.execute("DELETE FROM sqlite_sequence WHERE name IN ('notas', 'nota_impostos', 'adiantamentos', 'adiantamento_comprovantes', 'audit_log')")
        except Exception:
            pass
        c_loc.commit()
        c_loc.close()
        print(f"??? Local [{local_rel}]: limpo com sucesso.")

conn.close()
print("\n?? Sistema 100% zerado e pronto para alimentacao real!")
