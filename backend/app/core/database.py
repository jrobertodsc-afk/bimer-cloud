import sqlite3
import os
from .config import DATABASE_PATH

def get_connection():
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
    
    conn.commit()
    conn.close()

init_db()