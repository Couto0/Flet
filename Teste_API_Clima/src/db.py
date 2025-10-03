# db.py
import sqlite3
from datetime import datetime

DB_FILE = "clima.db"

def criar_tabela():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
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
    conn.commit()
    conn.close()

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