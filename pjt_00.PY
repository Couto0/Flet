import flet as ft

def main(page: ft.Page):
    page.title = 'Exemplo 00'

    texto = ft.Text('Hello World!')

    page.add(texto)

ft.app(main)