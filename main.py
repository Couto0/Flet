import flet as ft

def main(page: ft.Page):
    snack = ft.SnackBar(
        content=ft.Text("Mensagem de teste!", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.RED_400,
        duration=3000
    )
    page.snack_bar = snack

    def show_snack(e):
        snack.content.value = "O SnackBar apareceu 👀"
        snack.open = True
        page.update()

    page.add(ft.ElevatedButton("Mostrar SnackBar", on_click=show_snack))

ft.app(target=main)