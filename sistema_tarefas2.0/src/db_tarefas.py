import sqlite3

# banco de dados local sqlite para manter tarefas em CRUD
class DB_Tarefas():
    def __init__(self, DB_NAME='tarefas.db'):
        self.DB_NAME = DB_NAME

    def conectar(self):
        return sqlite3.connect(self.DB_NAME)

    def criar_tabela_tarefas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT,
                concluida BOOL DEFAULT false,
                categoria TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def adicionar_tarefa(self, descricao="", categoria="Geral"):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tarefas (descricao, categoria) VALUES (?, ?)",
            (descricao, categoria)
        )
        new_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def listar_tarefas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descricao, concluida, categoria FROM tarefas")
        tarefas = cursor.fetchall()
        cursor.close()
        conn.close()
        return tarefas

    def atualizar_tarefa(self, id, descricao, concluida, categoria):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tarefas SET descricao=?, concluida=?, categoria=? WHERE id=?",
            (descricao, concluida, categoria, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def concluir_tarefa(self, id, concluida):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tarefas SET concluida=? WHERE id=?",
            (concluida, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def remover_tarefa(self, id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id=?", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    def contar_tarefas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tarefas")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def contar_tarefas_concluidas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tarefas WHERE concluida=true")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total

    def contar_tarefas_pendentes(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tarefas WHERE concluida=false")
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return total