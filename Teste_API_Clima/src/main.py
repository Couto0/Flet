import flet as ft
import asyncio
from datetime import datetime
from teste_api import busca_clima
from db import criar_tabelas, salvar_clima, listar_climas, salvar_cidade, remover_cidade, listar_cidades

UPDATE_INTERVAL = 300  # segundos (5 min)

async def main(page: ft.Page):
    criar_tabelas()

    page.title = "Consulta Clima"
    page.scroll = "adaptive"
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.theme_mode = "light"

    page.appbar = ft.AppBar(
        title=ft.Text("Consulta Clima", size=20, weight="bold", color="white"),
        bgcolor=ft.Colors.BLUE_600,
        center_title=True,
    )

    mensagem = ft.Text("Aguardando consulta...", size=14, color=ft.Colors.RED_600)
    loader = ft.ProgressRing(visible=False)

    cidade_input = ft.TextField(label="Digite o nome da cidade", expand=True, autofocus = True, on_submit=lambda e: adicionar_cidade(e))

    # cidades monitoradas ficam no banco
    cidades: list[str] = listar_cidades()
    cidades_column = ft.Column()
    resultado_cards: dict[str, ft.Card] = {}  # cidade -> card

    resultado_coluna = ft.Column(spacing=10)

    # ---------------- FUNÇÕES ----------------
    def rebuild_cidades():
        cidades_column.controls.clear()
        for nome in cidades:
            def remover(e, nome=nome):
                if nome in cidades:
                    cidades.remove(nome)
                    remover_cidade(nome)
                    rebuild_cidades()
                    if nome in resultado_cards:
                        resultado_coluna.controls.remove(resultado_cards[nome])
                        del resultado_cards[nome]
                    page.update()

            def atual_one(e, nome=nome):
                page.run_task(atualizar_cidade, nome)

            cidades_column.controls.append(
                ft.Row(
                    [
                        ft.Text(nome),
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.Icons.REFRESH, tooltip="Atualizar agora", on_click=atual_one),
                                ft.IconButton(icon=ft.Icons.DELETE, on_click=remover),
                            ]
                        ),
                    ],
                    alignment="spaceBetween",
                )
            )

    def adicionar_cidade(e):
        nome = cidade_input.value.strip()
        if not nome:
            mensagem.value = "Insira uma cidade válida."
            mensagem.color = ft.Colors.RED_600
            page.update()
            return
        if nome in cidades:
            mensagem.value = f"{nome} já está na lista."
            mensagem.color = ft.Colors.ORANGE_700
            page.update()
            return

        cidades.append(nome)
        salvar_cidade(nome)
        cidade_input.value = ""
        rebuild_cidades()
        page.update()

    async def atualizar_cidade(nome: str):
        loader.visible = True
        page.update()
        clima_info = await asyncio.to_thread(busca_clima, nome)

        if clima_info:
            await asyncio.to_thread(
                salvar_clima,
                clima_info["cidade"],
                clima_info["descricao"],
                clima_info["temperatura"],
                clima_info["umidade"],
            )

            novo_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.BLUE), ft.Text(clima_info["cidade"], weight="bold")]),
                            ft.Row([ft.Icon(ft.Icons.WB_CLOUDY), ft.Text(clima_info["descricao"].capitalize())]),
                            ft.Row([ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.RED), ft.Text(f"{clima_info['temperatura']}°C")]),
                            ft.Row([ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE), ft.Text(f"{clima_info['umidade']}%")]),
                        ],
                        spacing=6,
                    ),
                    padding=10,
                )
            )

            # substitui card antigo se já existir
            if nome in resultado_cards:
                idx = resultado_coluna.controls.index(resultado_cards[nome])
                resultado_coluna.controls[idx] = novo_card
            else:
                resultado_coluna.controls.append(novo_card)

            resultado_cards[nome] = novo_card

        else:
            mensagem.value = f"Erro ao consultar {nome}"
            mensagem.color = ft.Colors.RED_600

        loader.visible = False
        mensagem.value = f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        mensagem.color = ft.Colors.GREEN_600
        page.update()

    async def atualizar_todas_cidades():
        for nome in cidades:
            await atualizar_cidade(nome)

    async def periodic():
        while True:
            if cidades:
                await atualizar_todas_cidades()
            await asyncio.sleep(UPDATE_INTERVAL)

    def mostrar_historico(e):
        async def _show():
            rows = await asyncio.to_thread(listar_climas)
            content_column = ft.Column(spacing=6)
            content_column.controls.append(ft.Text("Histórico (mais recente primeiro):", weight="bold"))
            for r in rows[:50]:
                cidade, descricao, temperatura, umidade, data_hora = r
                content_column.controls.append(
                    ft.Row([ft.Text(data_hora, size=12), ft.Text(cidade), ft.Text(f"{temperatura}°C"), ft.Text(f"{umidade}%"), ft.Text(descricao)])
                )

            def fechar(evt):
                dlg.open = False
                page.update()

            dlg = ft.AlertDialog(
                title=ft.Text("Histórico"),
                content=ft.Container(content=content_column, width=700, height=400),
                actions=[ft.TextButton("Fechar", on_click=fechar)],
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

        page.run_task(_show)

    # ---------------- LAYOUT ----------------
    botao_add = ft.IconButton(icon=ft.Icons.ADD, tooltip="Adicionar cidade", on_click=adicionar_cidade)
    botao_atualizar = ft.ElevatedButton("Atualizar agora", on_click=lambda e: page.run_task(atualizar_todas_cidades))
    botao_historico = ft.ElevatedButton("Histórico", on_click=mostrar_historico)

    rebuild_cidades()

    page.add(
        ft.Column(
            [
                mensagem,
                ft.Row([cidade_input, botao_add]),
                ft.Text("Cidades monitoradas:", weight="bold"),
                cidades_column,
                ft.Row([botao_atualizar, botao_historico], spacing=10),
                loader,
                ft.Divider(),
                resultado_coluna,
            ],
            scroll="adaptive",
            expand=True,
            tight=True,
        )
    )

    page.run_task(periodic)


if __name__ == "__main__":
    ft.app(target=main)
