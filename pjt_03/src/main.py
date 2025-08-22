import flet as ft

def main(page: ft.Page):
    page.title = 'APP CONTADOR'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
    page.padding = 50

    txt_contador = ft.Text('O', size=50, weight=ft.FontWeight.BOLD)
    btn_menos = ft.ElevatedButton('-')
    btn_mais = ft.ElevatedButton('+')
    btn_zerar = ft.ElevatedButton('Zerar')

    page.add(
        txt_contador,
        ft.Row(
            controls=[
                btn_menos,
                btn_mais
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        ),
        btn_zerar,
    )

ft.app(main)
