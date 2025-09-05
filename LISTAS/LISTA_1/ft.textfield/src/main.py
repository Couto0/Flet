import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.title = "Nivel_2"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.font = ['popins', 'times new roman', 'arial']
    a = ft.TextField(label="Nome", width=300, border_color=ft.Colors.GREEN_50, text_size=20,),
    page.add(a,
             ft.ElevatedButton(text = 'MOSTRAR', on_click = lambda e:'txt'),
             ft.Text(value = {a}, size = 20, weight = ft.FontWeight.BOLD,))

    
    

    page.update()

ft.app(main)
