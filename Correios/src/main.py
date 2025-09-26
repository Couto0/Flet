import flet as ft
import requests as req


def buscar_cep(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = req.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "erro" not in data:
                return data
        return None
    except Exception as e:
        print("Erro na requisição:", e)
        return None


def main(page: ft.Page):
    # Configurações da página
    page.title = "Consulta CEP"
    page.scroll = "adaptive"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.theme_mode = "light"

    # Barra de título
    page.appbar = ft.AppBar(
        title=ft.Text("Consulta CEP", size=20, weight="bold", color="white"),
        bgcolor=ft.Colors.BLUE_600,
        center_title=True,
    )

    # Mensagem inicial / erro
    mensagem = ft.Text("Aguardando a consulta de um CEP...", size=14, color=ft.Colors.RED_600)

    # Loader
    loader = ft.ProgressRing(visible=False, color=ft.Colors.BLUE)

    # Campos do resultado
    logradouro = ft.TextField(label="Logradouro", read_only=True, border=ft.InputBorder.UNDERLINE)
    bairro = ft.TextField(label="Bairro", read_only=True, border=ft.InputBorder.UNDERLINE)
    cidade = ft.TextField(label="Cidade", read_only=True, border=ft.InputBorder.UNDERLINE)
    estado = ft.TextField(label="Estado", read_only=True, border=ft.InputBorder.UNDERLINE)
    ddd = ft.TextField(label="DDD", read_only=True, border=ft.InputBorder.UNDERLINE)

    # Card do resultado
    card_resultado = ft.Card(
        visible=False,
        elevation=8,
        color=ft.Colors.WHITE,
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Resultado da Consulta", size=18, weight="bold", color=ft.Colors.BLUE_800),
                    ft.Divider(),
                    logradouro,
                    bairro,
                    cidade,
                    estado,
                    ddd,
                ],
                spacing=10,
                tight=True,
            ),
            padding=20,
            border_radius=15,
        ),
    )

    # Campo de busca
    cep_input = ft.TextField(
        label="Digite o CEP",
        width=220,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=8,
        border_radius=12,
        border_color=ft.Colors.BLUE_400,
    )

    # Função chamada ao clicar em buscar
    def on_buscar(e):
        mensagem.value = ""
        loader.visible = True
        card_resultado.visible = False
        page.update()

        cep = cep_input.value.strip()
        if not cep.isdigit() or len(cep) != 8:
            mensagem.value = "CEP inválido! Digite 8 números."
            loader.visible = False
            page.update()
            return

        dados = buscar_cep(cep)
        loader.visible = False
        if dados:
            logradouro.value = dados.get("logradouro", "")
            bairro.value = dados.get("bairro", "")
            cidade.value = dados.get("localidade", "")
            estado.value = dados.get("uf", "")
            ddd.value = dados.get("ddd", "")
            card_resultado.visible = True
            mensagem.value = ""
        else:
            card_resultado.visible = False
            mensagem.value = "CEP não encontrado."

        page.update()

    # Botões extras
    def on_limpar(e):
        cep_input.value = ""
        mensagem.value = "Aguardando a consulta de um CEP..."
        card_resultado.visible = False
        page.update()

    def on_copiar(e):
        endereco = f"{logradouro.value}, {bairro.value}, {cidade.value}-{estado.value} (DDD: {ddd.value})"
        page.set_clipboard(endereco)
        mensagem.value = "Endereço copiado!"
        page.update()

    button_buscar = ft.FilledButton(
        text="Buscar",
        icon=ft.Icons.SEARCH,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=on_buscar,
    )

    button_limpar = ft.OutlinedButton(
        text="Limpar",
        icon=ft.Icons.CLEAR,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=on_limpar,
    )

    button_copiar = ft.OutlinedButton(
        text="Copiar Endereço",
        icon=ft.Icons.COPY,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=on_copiar,
    )

    # Layout final
    page.add(
        ft.Column(
            [
                ft.Row([cep_input, button_buscar, loader], alignment="center", spacing=10),
                ft.Container(mensagem, margin=10),
                card_resultado,
                ft.Row([button_limpar, button_copiar], alignment="center", spacing=10),
            ],
            horizontal_alignment="center",
            spacing=20,
        )
    )


ft.app(main)