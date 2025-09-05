import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.title = "Lista 1"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.font = ['popins', 'times new roman', 'arial']
    page.add(ft.Text("Bem-vindo ao IFNMG Diamantina!", size = 20, weight = ft.FontWeight.BOLD,),
             ft.Text('Você está aprendendo a usar o Flet para criar interfaces gráficas com Python.'),
             ft.Text('Este é um componente de Texto (ft.Text).'))

    
    

    page.update()

ft.app(main)
