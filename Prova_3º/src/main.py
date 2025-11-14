# main.py
import flet as ft
from calc_TBM import tmb_homem, tmb_mulher
from base_config import Config, apply_config, create_sidebar


def main(page: ft.Page):
    # --- Configuração inicial ---
    config = Config()
    apply_config(page, config)
    page.title = "Calculadora de Gasto Calórico (TMB)"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # --- Funções auxiliares ---
    def restart_app(e):
        genero_group.value = None
        idade_field.value = ""
        peso_field.value = ""
        altura_field.value = ""
        resultado_text.value = ""
        page.update()

    def toggle_theme(e):
        config.theme = "Dark" if config.theme == "Light" else "Light"
        theme_button.text = f"Tema: {config.theme}"
        apply_config(page, config)
        page.update()

    # --- Barra lateral ---
    sidebar, theme_button = create_sidebar(restart_app, toggle_theme, config)
    sidebar.bgcolor = ft.Colors.BLUE_GREY_800

    # --- Campos de entrada ---
    genero_group = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="Masculino", label="Masculino", fill_color=ft.Colors.LIGHT_BLUE_200),
                ft.Radio(value="Feminino", label="Feminino", fill_color=ft.Colors.PINK_200),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    idade_field = ft.TextField(
        label="Idade (anos)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        width=250
    )
    peso_field = ft.TextField(
        label="Peso (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        width=250
    )
    altura_field = ft.TextField(
        label="Altura (cm)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        width=250
    )

    resultado_text = ft.Text("", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.LIGHT_GREEN_300)

    # --- Função principal ---
    def calcular_tmb(e):
        if not genero_group.value or not idade_field.value or not peso_field.value or not altura_field.value:
            page.open(ft.SnackBar(ft.Text("Por favor, preencha todos os campos.")))
            return

        try:
            idade = int(idade_field.value)
            peso = float(peso_field.value)
            altura = float(altura_field.value)
        except ValueError:
            page.open(ft.SnackBar(ft.Text("Digite apenas números válidos nos campos!")))
            return

        if genero_group.value == "Masculino":
            resultado = tmb_homem(peso, altura, idade)
        elif genero_group.value == "Feminino":
            resultado = tmb_mulher(peso, altura, idade)
        else:
            page.open(ft.SnackBar(ft.Text("Selecione um gênero antes de calcular.")))
            return

        resultado_text.value = f"{resultado:.2f} kcal/dia"
        page.update()

    calcular_btn = ft.FilledButton(
        text="CALCULAR",
        on_click=calcular_tmb,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.LIGHT_BLUE_400,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
    )

    # --- Card de entrada ---
    card_inputs = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Preencha seus dados:", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    genero_group,
                    idade_field,
                    peso_field,
                    altura_field,
                    calcular_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=30,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=15,
            width=350,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK38)
        )
    )

    # --- Card de resultado ---
    card_resultado = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔥 Sua Taxa Metabólica Basal é:", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    resultado_text,
                    ft.Text("Este é seu gasto calórico em repouso.", size=13, color=ft.Colors.GREY_300),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=25,
            bgcolor=ft.Colors.BLUE_GREY_800,
            border_radius=15,
            width=350,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.BLACK38)
        )
    )

    # --- Layout geral ---
    page.appbar = ft.AppBar(
        title=ft.Text("Calculadora TMB", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.BLUE_GREY_800,
        center_title=True
    )

    layout = ft.Column(
        [
            ft.Row([card_inputs, card_resultado],
                   alignment=ft.MainAxisAlignment.CENTER,
                   spacing=40),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    page.add(layout)


ft.app(target=main)
