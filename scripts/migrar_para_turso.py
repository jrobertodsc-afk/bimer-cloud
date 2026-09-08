import os
import sys
import sqlite3
import base64
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_LOCAL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "bimer.db"))
if not os.path.exists(DB_LOCAL):
    alt_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "bimer.db"))
    if os.path.exists(alt_db):
        DB_LOCAL = alt_db

def to_turso_arg(v):
    if v is None:
        return {"type": "null"}
    elif isinstance(v, bool):
        return {"type": "integer", "value": "1" if v else "0"}
    elif isinstance(v, int):
        return {"type": "integer", "value": str(v)}
    elif isinstance(v, float):
        return {"type": "float", "value": v}
    elif isinstance(v, (bytes, bytearray)):
        return {"type": "blob", "base64": base64.b64encode(v).decode("ascii")}
    else:
        return {"type": "text", "value": str(v)}

def normalize_turso_url(url: str) -> str:
    url = url.strip()
    if url.startswith("libsql://"):
        url = "https://" + url[len("libsql://"):]
    if not url.endswith("/v2/pipeline"):
        url = url.rstrip("/") + "/v2/pipeline"
    return url

def migrar(turso_url: str, turso_token: str):
    print("=" * 65)
    print("  🚀 MIGRAÇÃO BIMER CLOUD: SQLITE LOCAL ➔ TURSO (LIBSQL)")
    print("=" * 65)
    
    if not os.path.exists(DB_LOCAL):
        print(f"❌ Banco local não encontrado em: {DB_LOCAL}")
        return
        
    endpoint = normalize_turso_url(turso_url)
    print(f"📦 Lendo banco de dados local: {DB_LOCAL}")
    conn_local = sqlite3.connect(DB_LOCAL)
    conn_local.row_factory = sqlite3.Row
    cur_local = conn_local.cursor()
    
    print(f"🌐 Conectando ao Turso: {endpoint}")
    session = requests.Session()
    headers = {
        "Authorization": f"Bearer {turso_token.strip()}",
        "Content-Type": "application/json"
    }

    def exec_batch(stmts):
        payload = {"requests": [{"type": "execute", "stmt": s} for s in stmts]}
        res = session.post(endpoint, headers=headers, json=payload, timeout=30)
        if res.status_code != 200:
            raise RuntimeError(f"Turso HTTP {res.status_code}: {res.text}")
        data = res.json()
        for item in data.get("results", []):
            if item.get("type") == "error":
                raise RuntimeError(f"Erro SQL no Turso: {item}")
        return data
    
    tabelas = ["notas", "nota_impostos", "adiantamentos", "adiantamento_comprovantes", "audit_log", "usuarios"]
    
    for tab in tabelas:
        print(f"\n⚙️ Processando tabela [{tab}]...")
        
        cur_local.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (tab,))
        row_sql = cur_local.fetchone()
        if not row_sql or not row_sql["sql"]:
            print(f"  ⚠️ Tabela {tab} não existe no SQLite local, pulando.")
            continue
            
        ddl = row_sql["sql"]
        if "IF NOT EXISTS" not in ddl.upper():
            ddl = ddl.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)
            
        exec_batch([{"sql": ddl}])
        print(f"  ✅ Tabela criada/verificada no Turso")
        
        if tab == "nota_impostos":
            cur_local.execute("SELECT * FROM nota_impostos WHERE nota_id IN (SELECT id FROM notas)")
        else:
            cur_local.execute(f"SELECT * FROM {tab}")
        rows = cur_local.fetchall()
        total_rows = len(rows)
        print(f"  📊 Total de registros a migrar: {total_rows}")
        
        if total_rows == 0:
            continue
            
        colunas = [col[0] for col in cur_local.description]
        cols_str = ", ".join(colunas)
        placeholders = ", ".join(["?" for _ in colunas])
        insert_sql = f"INSERT OR REPLACE INTO {tab} ({cols_str}) VALUES ({placeholders})"
        
        stmts = []
        inseridos = 0
        for r in rows:
            stmts.append({
                "sql": insert_sql,
                "args": [to_turso_arg(v) for v in r]
            })
            inseridos += 1
            if len(stmts) >= 50 or inseridos == total_rows:
                exec_batch(stmts)
                print(f"    -> {inseridos}/{total_rows} registros inseridos...")
                stmts = []
                
        # Conferência
        res_count = exec_batch([{"sql": f"SELECT COUNT(*) FROM {tab}"}])
        count_turso = res_count["results"][0]["response"]["result"]["rows"][0][0]["value"]
        print(f"  🎉 Concluído: {count_turso} registros verificados no Turso!")
        
    conn_local.close()
    print("\n" + "=" * 65)
    print("  ✅ MIGRAÇÃO PARA O TURSO FINALIZADA COM 100% DE SUCESSO!")
    print("=" * 65)

if __name__ == "__main__":
    url = os.getenv("TURSO_DATABASE_URL") or (sys.argv[1] if len(sys.argv) > 1 else "")
    token = os.getenv("TURSO_AUTH_TOKEN") or (sys.argv[2] if len(sys.argv) > 2 else "")
    
    if not url or not token:
        print("Uso:")
        print("  python migrar_para_turso.py <TURSO_DATABASE_URL> <TURSO_AUTH_TOKEN>")
        print("Ou defina as variáveis de ambiente TURSO_DATABASE_URL e TURSO_AUTH_TOKEN.")
        sys.exit(1)
        
    migrar(url, token)

