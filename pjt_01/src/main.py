import flet as ft 

def main(page: ft.Page):
    page.title = 'Minha primeira pagina flet'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Column(
            controls=[
                ft.Text('Bem vindo ao IFNMG Diamantina',size=20),
                ft.Text('Bem vindo ao IFNMG Diamantina',size=20),
                ft.Text('Bem vindo ao IFNMG Diamantina',size=20),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            height=600,
        )
    )

    page.update()

ft.app(main)