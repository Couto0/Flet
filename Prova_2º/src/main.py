# main.py
import flet as ft
from logic import validar_peso, calcular_consumo


def main(page: ft.Page):

    page.title = "Calculadora de Consumo de Água"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"
    page.padding = 20

    # Snackbar de erro
    snackbar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.RED_300)

    def show_error(msg):
        snackbar.content.value = msg
        snackbar.open = True
        page.update()

    # Campo de peso
    peso_field = ft.TextField(
        label="Peso Corporal",
        hint_text="Digite seu peso",
        width=250,
        suffix_text="kg",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # Grupo de atividade
    atividade_group = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value = 1.00, label = "Sedentário"),
                ft.Radio(value = 1.05, label = "levemente ativo"),
                ft.Radio(value = 1.10, label = "Moderadamente Ativo"),
                ft.Radio(value = 1.15, label = "Muito Ativo"),
                ft.Radio(value = 1.20, label = "Extremamente Ativo"),
            ]
        )
    )

    # Resultado
    resultado_texto = ft.Text("", size=20, weight="bold", text_align="center")

    resultado_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.WATER_DROP, size=40),
                    resultado_texto,
                ],
                horizontal_alignment="center",
            ),
            padding=20,
            width=300,
        ),
        elevation=5,
    )

    # Botão calcular
    def calcular_click(e):
        peso, erro = validar_peso(peso_field.value)

        if erro:
            show_error(erro)
            return

        if not atividade_group.value:
            show_error("Selecione o nível de atividade física.")
            return

        multiplicador = float(atividade_group.value)
        total = calcular_consumo(peso, multiplicador)

        resultado_texto.value = f"Consumo ideal: {total:.0f} ml por dia"
        page.update()

    calcular_btn = ft.FilledButton("Calcular", on_click=calcular_click, width=200)

    # Layout Final
    page.add(
        ft.AppBar(
            title=ft.Text("Calculadora de Consumo de Água Diária"),
            bgcolor=ft.Colors.BLUE_400,
        ),
        snackbar,
        ft.Container(
            content=ft.Column(
                [
                    peso_field,
                    ft.Text("Nível de Atividade Física", size=16, weight="bold"),
                    atividade_group,
                    calcular_btn,
                    ft.Divider(),
                    resultado_card,
                ],
                spacing=20,
            ),
            width=350,
        ),
    )


ft.app(main)
