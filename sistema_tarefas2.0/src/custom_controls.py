import flet as ft
from db_tarefas import DB_Tarefas

class Tarefa(ft.Row):
    def __init__(self, id, descricao, concluida, categoria, on_change_tarefa, db):
        super().__init__()
        self.id = id
        self.checkbox = ft.Checkbox(on_change=self.concluir_tarefa)
        if concluida == 1 or concluida == True:
            self.checkbox.value = True
        self.descricao = ft.Text(f"{descricao} ({categoria})", expand=True)
        self.botao_remover = ft.IconButton(icon=ft.Icons.DELETE, on_click=self.remover_tarefa)
        self.on_change_tarefa = on_change_tarefa
        self.db = db
        self.controls = [self.checkbox, self.descricao, self.botao_remover]

    def concluir_tarefa(self, e):
        try:
            self.db.concluir_tarefa(self.id, self.checkbox.value)
            self.on_change_tarefa(e)
        except e:
            print(f'Erro em conclusão de tarefa: {e}')

    def remover_tarefa(self, e):
        try:
            self.db.remover_tarefa(self.id)
            self.parent.controls.remove(self)
            self.on_change_tarefa(e)
        except e:
            print(f'Erro em remoção de tarefa: {e}')