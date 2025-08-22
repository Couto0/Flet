import flet as ft

def main(page: ft.Page):
    page.title = "Tela de Cadastro"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#f2f2f2"

    avatar = ft.CircleAvatar(
    foreground_image_src="https://cdn-icons-png.flaticon.com/512/149/149071.png",
    radius=40,)

    nome = ft.TextField(label="Name", width=300, prefix_icon=ft.Icons.PERSON)
    email = ft.TextField(label="Email", width=300, prefix_icon=ft.Icons.EMAIL)
    senha = ft.TextField(label="Password", password=True, can_reveal_password=True,
                         width=300, prefix_icon=ft.Icons.LOCK)

    botao = ft.ElevatedButton(
        "Sign up",
        width=300,
        bgcolor="#4a6cf7",
        color="white",
    )

    login_text = ft.TextButton(
        "Already have an account?",
        on_click=lambda e: page.snack_bar.open(ft.SnackBar(ft.Text("Ir para login")))
    )

    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Create Account", size=22, weight="bold"),
                    ft.Text("Enter your details below & free sign up", size=14, color="grey"),
                    avatar,
                    nome,
                    email,
                    senha,
                    botao,
                    login_text,
                ],
                horizontal_alignment="center",
                spacing=15,
            ),
            padding=20,
            width=350,
        )
    )

    page.add(card)

ft.app(target=main)