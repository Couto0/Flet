import flet as ft
from custom_controls import Tarefa
from db_tarefas import DB_Tarefas

db = DB_Tarefas()
db.criar_tabela_tarefas()

def main(page: ft.Page):
    page.title = "MINHA LISTA DE TAREFAS - SPA"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def carregar_tarefas():
        lista_tarefas.controls.clear()
        tarefas = db.listar_tarefas()
        for tarefa in tarefas:
            lista_tarefas.controls.append(
                Tarefa(tarefa[0], tarefa[1], tarefa[2], tarefa[3], alterar_tarefa, db)
            )
        page.update()

    def adicionar_tarefa(e):
        try:
            id = db.adicionar_tarefa(tf_nova_tarefa.value, dd_categoria.value)
            lista_tarefas.controls.append(
                Tarefa(id, tf_nova_tarefa.value, False, dd_categoria.value, alterar_tarefa, db)
            )
            tf_nova_tarefa.value = ''
            dd_categoria.value = "Geral"
            tf_nova_tarefa.focus()
            quantidade_tarefas_restantes()
            page.update()
        except e:
            print(f'Erro em inserção de tarefa: {e}')

    def todas_tarefas(e):
        for tarefa in lista_tarefas.controls:
            tarefa.visible = True
        page.update()

    def tarefas_concluidas(e):
        for tarefa in lista_tarefas.controls:
            tarefa.visible = tarefa.checkbox.value
        page.update()

    def tarefas_pendentes(e):
        for tarefa in lista_tarefas.controls:
            tarefa.visible = not tarefa.checkbox.value
        page.update()

    def quantidade_tarefas_restantes():
        total = db.contar_tarefas_pendentes()
        txt_total_tarefas.value = f"{total} Tarefas Restantes"
        page.update()

    def alterar_tarefa(e):
        quantidade_tarefas_restantes()
        page.update()

    # Campos de entrada
    tf_nova_tarefa = ft.TextField(label="Nova Tarefa", width=300, expand=True, on_submit=adicionar_tarefa)

    dd_categoria = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("Geral"),
            ft.dropdown.Option("Trabalho"),
            ft.dropdown.Option("Estudos"),
            ft.dropdown.Option("Pessoal")
        ],
        value="Geral",
        width=150
    )

    btn_adicionar = ft.IconButton(icon=ft.Icons.ADD, on_click=adicionar_tarefa)
    lista_tarefas = ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)
    btn_todas_tarefas = ft.ElevatedButton(text="Todas as Tarefas", on_click=todas_tarefas)
    btn_tarefas_concluidas = ft.ElevatedButton(text="Tarefas Concluídas", on_click=tarefas_concluidas)
    btn_tarefas_pendentes = ft.ElevatedButton(text="Tarefas Pendentes", on_click=tarefas_pendentes)
    txt_total_tarefas = ft.Text(value="0 Tarefas Restantes", size=20)

    # Layout
    page.add(
        ft.Text("MINHA LISTA DE TAREFAS", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([tf_nova_tarefa, dd_categoria, btn_adicionar]),
        ft.Divider(),
        lista_tarefas,
        ft.Divider(),
        ft.Row([btn_todas_tarefas, btn_tarefas_concluidas, btn_tarefas_pendentes],
               alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        txt_total_tarefas
    )

    carregar_tarefas()
    quantidade_tarefas_restantes()

ft.app(main)
