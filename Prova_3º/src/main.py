# main.py
import flet as ft
from calc_TBM import tmb_homem, tmb_mulher
from base_config import Config, apply_config, create_sidebar


def main(page: ft.Page):
    # --- Configuração inicial ---
    config = Config()
    cores = apply_config(page, config)
    page.title = "Calculadora de Gasto Calórico (TMB)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # --- Cria o SnackBar padrão para exibir mensagens (criado apenas uma vez) ---
    snack = ft.SnackBar(
        content=ft.Text("", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.RED_400,
        duration=3000  # 3 segundos
    )
    page.snack_bar = snack  # associa a instância à página

    # --- Funções auxiliares ---
    def restart_app(e):
        """Limpa todos os campos e resultado."""
        genero_group.value = None
        idade_field.value = ""
        peso_field.value = ""
        altura_field.value = ""
        resultado_text.value = ""
        page.update()

    def toggle_theme(e):
        """Alterna entre tema claro e escuro."""
        config.theme = "Dark" if config.theme == "Light" else "Light"
        theme_button.text = f"Tema: {config.theme}"
        apply_config(page, config)
        page.update()

    # --- Barra lateral (importada de base_config) ---
    sidebar, theme_button = create_sidebar(restart_app, toggle_theme, config)
    sidebar.bgcolor = cores["sidebar_color"]

    # --- Campos de entrada ---
    genero_group = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="Masculino", label="Masculino"),
                ft.Radio(value="Feminino", label="Feminino"),
            ]
        )
    )

    idade_field = ft.TextField(label="Idade (anos)", keyboard_type=ft.KeyboardType.NUMBER)
    peso_field = ft.TextField(label="Peso (kg)", keyboard_type=ft.KeyboardType.NUMBER)
    altura_field = ft.TextField(label="Altura (cm)", keyboard_type=ft.KeyboardType.NUMBER)

    resultado_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)

    # --- Função principal de cálculo ---
    def calcular_tmb(e):
        """Valida dados, calcula a TMB e exibe o resultado."""

        # 1. Verifica se algum campo está vazio
        if not genero_group.value or not idade_field.value or not peso_field.value or not altura_field.value:
            snack.content.value = "Por favor, preencha todos os campos."
            snack.open = True
            page.update()
            return

        # 2. Valida se os valores são numéricos
        try:
            idade = int(idade_field.value)
            peso = float(peso_field.value)
            altura = float(altura_field.value)
        except ValueError:
            snack.content.value = "Digite apenas números válidos nos campos!"
            snack.open = True
            page.update()
            return

        # 3. Cálculo da TMB com base no gênero
        if genero_group.value == "Masculino":
            resultado = tmb_homem(peso, altura, idade)
        elif genero_group.value == "Feminino":
            resultado = tmb_mulher(peso, altura, idade)
        else:
            # (caso improvável, pois já checamos acima)
            snack.content.value = "Selecione um gênero antes de calcular."
            snack.open = True
            page.update()
            return

        # 4. Exibição do resultado
        resultado_text.value = f"Sua Taxa Metabólica Basal é: {resultado:.2f} kcal/dia"
        page.update()

    calcular_btn = ft.FilledButton(text="CALCULAR", on_click=calcular_tmb)

    # --- Card de resultado ---
    card_resultado = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("🔥 Sua Taxa Metabólica Basal é:", size=16, weight=ft.FontWeight.BOLD),
                    resultado_text,
                    ft.Text("Este é seu gasto calórico em repouso.", size=12),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        )
    )

    # --- Layout principal da aplicação ---
    page.appbar = ft.AppBar(title=ft.Text("Calculadora TMB"), bgcolor=ft.Colors.BLUE_GREY_700, color=ft.Colors.WHITE)

    layout = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Preencha os dados abaixo:", size=16),
                        genero_group,
                        idade_field,
                        peso_field,
                        altura_field,
                        calcular_btn,
                        card_resultado,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    expand=True,
                ),
                expand=True,
                padding=20,
            ),
        ],
        expand=True,
    )

    page.add(layout)


ft.app(target=main)
