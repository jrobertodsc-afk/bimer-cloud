import sqlite3
import os
import base64
import requests
from .config import DATABASE_PATH, TURSO_DATABASE_URL, TURSO_AUTH_TOKEN

def _to_turso_arg(v):
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

def _from_turso_val(val_dict):
    if not isinstance(val_dict, dict):
        return val_dict
    t = val_dict.get("type")
    if t == "null":
        return None
    elif t == "integer":
        return int(val_dict.get("value", 0))
    elif t == "float":
        return float(val_dict.get("value", 0.0))
    elif t == "text":
        return val_dict.get("value", "")
    elif t == "blob":
        return base64.b64decode(val_dict.get("base64", ""))
    return val_dict.get("value")

def normalize_turso_url(url: str) -> str:
    url = url.strip()
    if url.startswith("libsql://"):
        url = "https://" + url[len("libsql://"):]
    if not url.endswith("/v2/pipeline"):
        url = url.rstrip("/") + "/v2/pipeline"
    return url

class TursoRow(dict):
    """Permite acesso tanto por nome de coluna (dict / row['col']) quanto por índice (row[0])"""
    def __init__(self, cols, vals):
        super().__init__(zip(cols, vals))
        self._vals = list(vals)
        self._keys = list(cols)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._vals[item]
        return super().__getitem__(item)

    def keys(self):
        return self._keys

    def values(self):
        return self._vals

class TursoCursor:
    def __init__(self, session, endpoint, headers):
        self.session = session
        self.endpoint = endpoint
        self.headers = headers
        self.description = None
        self.lastrowid = None
        self.rowcount = 0
        self._rows = []
        self._idx = 0

    def execute(self, sql, params=()):
        args = [_to_turso_arg(p) for p in params] if params else []
        payload = {
            "requests": [
                {
                    "type": "execute",
                    "stmt": {
                        "sql": sql,
                        "args": args
                    }
                },
                {"type": "close"}
            ]
        }
        res = self.session.post(self.endpoint, headers=self.headers, json=payload, timeout=30)
        if res.status_code != 200:
            raise sqlite3.OperationalError(f"Erro Turso {res.status_code}: {res.text}")
        data = res.json()
        results = data.get("results", [])
        if not results:
            return self
        first = results[0]
        if first.get("type") == "error":
            err_msg = first.get("error", {}).get("message", "Erro SQL desconhecido")
            raise sqlite3.OperationalError(err_msg)

        exec_res = first.get("response", {}).get("result", {})
        cols = [c["name"] for c in exec_res.get("cols", [])]
        self.description = [(c, None, None, None, None, None, None) for c in cols]
        
        last_id = exec_res.get("last_insert_rowid")
        self.lastrowid = int(last_id) if last_id is not None else None
        self.rowcount = exec_res.get("affected_row_count", 0)

        raw_rows = exec_res.get("rows", [])
        parsed_rows = []
        for r in raw_rows:
            vals = [_from_turso_val(v) for v in r]
            parsed_rows.append(TursoRow(cols, vals))

        self._rows = parsed_rows
        self._idx = 0
        return self

    def executemany(self, sql, seq_of_params):
        stmts = []
        for params in seq_of_params:
            stmts.append({
                "type": "execute",
                "stmt": {
                    "sql": sql,
                    "args": [_to_turso_arg(p) for p in params] if params else []
                }
            })
        if not stmts:
            return self
        stmts.append({"type": "close"})
        res = self.session.post(self.endpoint, headers=self.headers, json={"requests": stmts}, timeout=60)
        if res.status_code != 200:
            raise sqlite3.OperationalError(f"Erro Turso executemany {res.status_code}: {res.text}")
        return self

    def fetchone(self):
        if self._idx < len(self._rows):
            r = self._rows[self._idx]
            self._idx += 1
            return r
        return None

    def fetchall(self):
        r = self._rows[self._idx:]
        self._idx = len(self._rows)
        return r

    def fetchmany(self, size=None):
        if size is None:
            size = 1
        end = self._idx + size
        r = self._rows[self._idx:end]
        self._idx = min(end, len(self._rows))
        return r

class TursoConnectionWrapper:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token
        self.session = requests.Session()
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def cursor(self):
        return TursoCursor(self.session, self.endpoint, self.headers)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        self.session.close()

def get_connection():
    if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
        endpoint = normalize_turso_url(TURSO_DATABASE_URL)
        return TursoConnectionWrapper(endpoint, TURSO_AUTH_TOKEN)

    db_file = DATABASE_PATH
    os.makedirs(os.path.dirname(os.path.abspath(db_file)), exist_ok=True)
    conn = sqlite3.connect(db_file, check_same_thread=False, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_tx TEXT,
        tipo TEXT,
        fornecedor TEXT,
        cnpj TEXT,
        dt_emissao TEXT,
        dt_vencimento TEXT,
        dt_pagamento TEXT,
        valor_bruto REAL,
        valor_liquido REAL,
        status TEXT DEFAULT 'PENDENTE',
        categoria TEXT,
        observacao TEXT,
        responsavel TEXT,
        descricao TEXT,
        filial TEXT,
        forma_pgto TEXT,
        cod_barras TEXT,
        pix_chave TEXT,
        numero_nf TEXT,
        is_previsao INTEGER DEFAULT 0,
        conciliada INTEGER DEFAULT 0
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS nota_impostos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nota_id INTEGER,
        tipo TEXT,
        aliquota REAL,
        valor REAL,
        dt_venc_imp TEXT,
        status TEXT DEFAULT 'PENDENTE',
        numero_doc TEXT,
        FOREIGN KEY (nota_id) REFERENCES notas(id) ON DELETE CASCADE
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS adiantamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fornecedor TEXT,
        data TEXT,
        valor REAL,
        status TEXT DEFAULT 'ABERTO',
        observacao TEXT,
        ccusto TEXT,
        forma TEXT,
        motivo TEXT,
        data_fechamento TEXT
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS adiantamento_comprovantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        adiantamento_id INTEGER,
        data TEXT,
        tipo_doc TEXT,
        descricao TEXT,
        valor REAL,
        data_criacao TEXT,
        FOREIGN KEY (adiantamento_id) REFERENCES adiantamentos(id) ON DELETE CASCADE
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT DEFAULT '',
        acao TEXT DEFAULT '',
        entidade TEXT DEFAULT '',
        entidade_id TEXT DEFAULT '',
        descricao TEXT DEFAULT '',
        valor REAL DEFAULT 0,
        ip TEXT DEFAULT '',
        created_at TEXT DEFAULT (datetime('now'))
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        perfil TEXT NOT NULL DEFAULT 'MASTER',
        ativo INTEGER DEFAULT 1,
        ultimo_login TEXT,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

init_db()