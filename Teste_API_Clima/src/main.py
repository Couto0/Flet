import flet as ft
from teste_api import busca_clima


def main(page: ft.Page):
    # Configurações da página
    page.title = "Consulta Clima"
    page.scroll = "adaptive"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.theme_mode = "light"

    page.appbar = ft.AppBar(
        title=ft.Text("Consulta Clima", size=20, weight="bold", color="white"),
        bgcolor=ft.Colors.BLUE_600,
        center_title=True,
    )

    mensagem = ft.Text(
        "Aguardando a consulta de uma cidade...",
        size=14,
        color=ft.Colors.RED_600,
    )

    loader = ft.ProgressRing(visible=False, color=ft.Colors.BLUE)

    cidade_input = ft.TextField(
        label="Digite o nome da cidade",
        border=ft.InputBorder.OUTLINE,
        autofocus=True,
    )

    # Container que receberá o resultado
    resultado_coluna = ft.Column(spacing=10)

    card_resultado = ft.Card(
        visible=False,
        elevation=8,
        color=ft.Colors.WHITE,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Resultado da Consulta",
                        size=18,
                        weight="bold",
                        color=ft.Colors.BLUE_800,
                    ),
                    ft.Divider(),
                    resultado_coluna,
                ],
                tight=True,
            ),
            padding=15,
            width=400,
        ),
    )

    # Função de busca
    def buscar_clima(e):
        cidade = cidade_input.value.strip()
        if not cidade:
            mensagem.value = "Por favor, insira uma cidade válida."
            mensagem.color = ft.Colors.RED_600
            page.update()
            return

        loader.visible = True
        card_resultado.visible = False
        mensagem.value = ""
        page.update()

        clima_info = busca_clima(cidade)

        loader.visible = False
        if clima_info:
            resultado_coluna.controls = [
                ft.Row(
                    [ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.BLUE), ft.Text(f"Cidade: {clima_info['cidade']}")]
                ),
                ft.Row(
                    [ft.Icon(ft.Icons.WB_CLOUDY, color=ft.Colors.BLUE), ft.Text(f"Clima: {clima_info['descricao']}")]
                ),
                ft.Row(
                    [ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.RED), ft.Text(f"Temperatura: {clima_info['temperatura']}°C")]
                ),
                ft.Row(
                    [ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE), ft.Text(f"Umidade: {clima_info['umidade']}%")]
                ),
            ]
            card_resultado.visible = True
            mensagem.value = "Consulta realizada com sucesso!"
            mensagem.color = ft.Colors.GREEN_600
        else:
            mensagem.value = "Erro ao consultar o clima. Tente novamente."
            mensagem.color = ft.Colors.RED_600

        page.update()

    botao_buscar = ft.ElevatedButton(
        "Buscar Clima", on_click=buscar_clima, icon=ft.Icons.SEARCH
    )

    page.add(
        ft.Column(
            [
                mensagem,
                cidade_input,
                botao_buscar,
                loader,
                card_resultado,
            ],
            horizontal_alignment="center",
            tight=True,
            spacing=15,
        )
    )


ft.app(main)
