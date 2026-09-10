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

url = os.getenv("TURSO_DATABASE_URL", "").replace("libsql://", "https://") + "/v2/pipeline"
token = os.getenv("TURSO_AUTH_TOKEN", "")

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

print("\n🚀 Sincronizando SQLite local com os títulos limpos do Turso...")

res_all_notas = exec_turso([{"sql": "SELECT * FROM notas;"}])
cols_notas = [c["name"] for c in res_all_notas["results"][0]["response"]["result"]["cols"]]
rows_notas_raw = res_all_notas["results"][0]["response"]["result"]["rows"]

for db_file in [DB_LOCAL, DB_BACKEND]:
    if not os.path.exists(db_file):
        continue
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    # Garantir colunas no SQLite local
    for col in ["cod_operacao", "cnae", "item_lc116", "is_previsao", "conciliada"]:
        try:
            cur.execute(f"ALTER TABLE notas ADD COLUMN {col} TEXT;")
            conn.commit()
        except Exception:
            pass

    cur.execute("PRAGMA table_info(notas);")
    cols_existentes = [r[1] for r in cur.fetchall()]
    cols_comuns = [c for c in cols_notas if c in cols_existentes]
    
    cur.execute("DELETE FROM nota_impostos;")
    cur.execute("DELETE FROM notas;")
    
    col_str = ", ".join(cols_comuns)
    ph_str = ", ".join(["?" for _ in cols_comuns])
    
    for r in rows_notas_raw:
        vals_dict = {cols_notas[i]: r[i].get("value") for i in range(len(cols_notas))}
        row_vals = [vals_dict.get(c) for c in cols_comuns]
        parsed_vals = []
        for v in row_vals:
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
