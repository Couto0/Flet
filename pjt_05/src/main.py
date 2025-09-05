import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    conteiner = ft.Container(
        content=ft.Text("Meu Container", size=20, weight="bold", theme_style= ft.TextThemeStyle.HEADLINE_MEDIUM),
        padding=20,
        margin = 30, 
        bgcolor=ft.Colors.GREY_100, 
        width=300, height=100, 
        alignment=ft.alignment.center, 
        border_radius=30,
        border=ft.border.all(3, ft.Colors.BLACK),

    )
    page.add(conteiner)
    

ft.app(main)
