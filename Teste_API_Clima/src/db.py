# db.py
import sqlite3
from datetime import datetime

DB_FILE = "clima.db"

def criar_tabelas():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # tabela de histórico
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clima (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cidade TEXT NOT NULL,
            descricao TEXT,
            temperatura REAL,
            umidade INTEGER,
            data_hora TEXT
        )
    """)

    # tabela de cidades monitoradas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


# -------- Histórico --------
def salvar_clima(cidade, descricao, temperatura, umidade):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clima (cidade, descricao, temperatura, umidade, data_hora) VALUES (?, ?, ?, ?, ?)",
        (cidade, descricao, temperatura, umidade, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()

def listar_climas(limit: int | None = None):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    sql = "SELECT cidade, descricao, temperatura, umidade, data_hora FROM clima ORDER BY id DESC"
    if limit:
        sql += f" LIMIT {int(limit)}"
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# -------- Cidades monitoradas --------
def salvar_cidade(nome: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO cidades (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def remover_cidade(nome: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM cidades WHERE nome=?", (nome,))
    conn.commit()
    conn.close()

def listar_cidades():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT nome FROM cidades")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows