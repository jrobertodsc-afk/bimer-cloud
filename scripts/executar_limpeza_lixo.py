import os
import sys
import shutil
import sqlite3
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv("backend/.env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_LOCAL = os.path.join(BASE_DIR, "database", "bimer.db")
DB_BACKEND = os.path.join(BASE_DIR, "backend", "bimer.db")

# 1. Backups locais dos arquivos SQLite
for db_file in [DB_LOCAL, DB_BACKEND]:
    if os.path.exists(db_file):
        bkp = db_file + ".backup_seguranca_antes_limpar_lixo"
        shutil.copy2(db_file, bkp)
        print(f"✅ Backup local criado: {bkp}")

# 2. Conectar ao Turso
url = os.getenv("TURSO_DATABASE_URL", "").replace("libsql://", "https://") + "/v2/pipeline"
token = os.getenv("TURSO_AUTH_TOKEN", "")

if not url or not token:
    print("❌ Credenciais do Turso não encontradas!")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
session = requests.Session()

def exec_turso(stmts):
    payload = {"requests": [{"type": "execute", "stmt": s} for s in stmts]}
    res = session.post(url, headers=headers, json=payload, timeout=30)
    if res.status_code != 200:
        raise RuntimeError(f"Erro Turso {res.status_code}: {res.text}")
    data = res.json()
    for item in data.get("results", []):
        if item.get("type") == "error":
            raise RuntimeError(f"Erro SQL Turso: {item}")
    return data

print("\n🚀 1. Criando tabelas de backup no Turso...")
exec_turso([
    {"sql": "DROP TABLE IF EXISTS notas_backup_antes_limpeza;"},
    {"sql": "CREATE TABLE notas_backup_antes_limpeza AS SELECT * FROM notas;"},
    {"sql": "DROP TABLE IF EXISTS nota_impostos_backup_antes_limpeza;"},
    {"sql": "CREATE TABLE nota_impostos_backup_antes_limpeza AS SELECT * FROM nota_impostos;"}
])
print("  ✅ Tabelas de backup no Turso criadas com sucesso!")

print("\n🚀 2. Excluindo lançamentos lixo no Turso (filhos primeiro, depois notas)...")
res_del_notas = exec_turso([
    {"sql": "DELETE FROM nota_impostos WHERE nota_id NOT IN (SELECT id FROM notas WHERE dt_vencimento IN ('2026-09-10', '10/09/2026'));"},
    {"sql": "DELETE FROM notas WHERE dt_vencimento NOT IN ('2026-09-10', '10/09/2026');"},
    {"sql": "SELECT COUNT(*) FROM notas;"},
    {"sql": "SELECT id, numero_nf, fornecedor, dt_vencimento, valor_bruto FROM notas ORDER BY id ASC;"}
])

results = res_del_notas["results"]
total_mantido = results[2]["response"]["result"]["rows"][0][0]["value"]
rows_mantidos = results[3]["response"]["result"]["rows"]

print(f"\n🎉 Concluído no Turso: {total_mantido} títulos reais mantidos vencendo hoje:")
for r in rows_mantidos:
    vals = [c.get("value") for c in r]
    print(f"  ID {vals[0]}: NF {vals[1]} | {vals[2]} | Venc: {vals[3]} | R$ {vals[4]}")

# 3. Sincronizar o banco local SQLite com os dados limpos do Turso
print("\n🚀 3. Sincronizando SQLite local com os títulos limpos do Turso...")

# Buscar todas as notas mantidas completas do Turso
res_all_notas = exec_turso([{"sql": "SELECT * FROM notas;"}])
cols_notas = [c["name"] for c in res_all_notas["results"][0]["response"]["result"]["cols"]]
rows_notas_raw = res_all_notas["results"][0]["response"]["result"]["rows"]

for db_file in [DB_LOCAL, DB_BACKEND]:
    if not os.path.exists(db_file):
        continue
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    # Limpar notas e reinserir os mantidos
    cur.execute("DELETE FROM nota_impostos;")
    cur.execute("DELETE FROM notas;")
    
    col_str = ", ".join(cols_notas)
    ph_str = ", ".join(["?" for _ in cols_notas])
    
    for r in rows_notas_raw:
        vals = [c.get("value") for c in r]
        parsed_vals = []
        for v in vals:
            if isinstance(v, bool):
                parsed_vals.append(1 if v else 0)
            else:
                parsed_vals.append(v)
        cur.execute(f"INSERT OR REPLACE INTO notas ({col_str}) VALUES ({ph_str})", parsed_vals)
        
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM notas;")
    cnt_local = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM fornecedores;")
    cnt_forn = cur.fetchone()[0]
    conn.close()
    print(f"  ✅ {os.path.basename(db_file)}: {cnt_local} títulos mantidos | {cnt_forn} fornecedores preservados.")

print("\n" + "="*60)
print("🎉 LIMPEZA CONCLUÍDA COM SUCESSO ABSOLUTO!")
print("="*60)
