import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.title = "Lista 1"
    
    

    page.update()
ft.app(main)
