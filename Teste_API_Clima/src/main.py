# main.py
import flet as ft
import asyncio
from datetime import datetime
from teste_api import busca_clima
from db import criar_tabela, salvar_clima, listar_climas

# intervalo de atualização automática (em segundos)
UPDATE_INTERVAL = 300  # 5 minutos (mude se quiser)

async def main(page: ft.Page):
    criar_tabela()

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

    cidade_input = ft.TextField(label="Digite o nome da cidade", expand=True, autofocus = True, on_submit = lambda e: adicionar_cidade(e))
    cidades: list[str] = []                      # lista de nomes de cidade
    cidades_column = ft.Column()
    resultado_coluna = ft.Column(spacing=10)

    # --- helpers UI ---
    def rebuild_cidades():
        cidades_column.controls.clear()
        for nome in cidades:
            def remover(e, nome=nome):
                try:
                    cidades.remove(nome)
                except ValueError:
                    pass
                rebuild_cidades()
                page.update()

            # botão atualizar uma cidade (dispara task segura)
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
        cidade_input.value = ""
        rebuild_cidades()
        page.update()

    # atualiza uma única cidade (executa I/O em thread seguro)
    async def atualizar_cidade(nome: str):
        loader.visible = True
        page.update()
        try:
            clima_info = await asyncio.to_thread(busca_clima, nome)
        except Exception as ex:
            clima_info = None
            print("Erro na requisição:", ex)

        if clima_info:
            # salva no DB (rodando em thread para não bloquear)
            try:
                await asyncio.to_thread(
                    salvar_clima,
                    clima_info["cidade"],
                    clima_info["descricao"],
                    clima_info["temperatura"],
                    clima_info["umidade"],
                )
            except Exception as ex:
                print("Erro ao salvar no DB:", ex)

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.BLUE), ft.Text(clima_info["cidade"], weight="bold")]),
                            ft.Row([ft.Icon(ft.Icons.WB_CLOUDY), ft.Text(clima_info["descricao"].capitalize())]),
                            ft.Row([ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.RED), ft.Text(f"{clima_info['temperatura']}°C")]),
                            ft.Row([ft.Icon(ft.Icons.WATER_DROP), ft.Text(f"{clima_info['umidade']}%")]),
                        ],
                        spacing=6,
                    ),
                    padding=10,
                ),
            )
            # insere no topo dos resultados
            resultado_coluna.controls.insert(0, card)
        else:
            resultado_coluna.controls.insert(0, ft.Text(f"{nome}: erro ao consultar"))

        loader.visible = False
        mensagem.value = f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        mensagem.color = ft.Colors.GREEN_600
        page.update()

    # atualiza todas as cidades (usado por botão e por loop periódico)
    async def atualizar_todas_cidades():
        if not cidades:
            mensagem.value = "Nenhuma cidade para atualizar."
            mensagem.color = ft.Colors.RED_600
            page.update()
            return

        loader.visible = True
        mensagem.value = "Atualizando todas as cidades..."
        resultado_coluna.controls.clear()
        page.update()

        for nome in list(cidades):
            try:
                clima_info = await asyncio.to_thread(busca_clima, nome)
            except Exception as ex:
                clima_info = None
                print("Erro na requisição:", ex)

            if clima_info:
                # salva no DB sem bloquear
                try:
                    await asyncio.to_thread(
                        salvar_clima,
                        clima_info["cidade"],
                        clima_info["descricao"],
                        clima_info["temperatura"],
                        clima_info["umidade"],
                    )
                except Exception as ex:
                    print("Erro ao salvar no DB:", ex)

                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row([ft.Icon(ft.Icons.LOCATION_CITY, color=ft.Colors.BLUE), ft.Text(clima_info["cidade"], weight="bold")]),
                                ft.Row([ft.Icon(ft.Icons.WB_CLOUDY), ft.Text(clima_info["descricao"].capitalize())]),
                                ft.Row([ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.RED), ft.Text(f"{clima_info['temperatura']}°C")]),
                                ft.Row([ft.Icon(ft.Icons.WATER_DROP), ft.Text(f"{clima_info['umidade']}%")]),
                            ],
                            spacing=6,
                        ),
                        padding=10,
                    ),
                )
                resultado_coluna.controls.append(card)
            else:
                resultado_coluna.controls.append(ft.Text(f"{nome}: erro ao consultar"))

            # atualiza UI após cada cidade (mais responsivo)
            page.update()

        loader.visible = False
        mensagem.value = f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        mensagem.color = ft.Colors.GREEN_600
        page.update()

    # loop periódico (executado em background pelo page.run_task)
    async def periodic():
        while True:
            await atualizar_todas_cidades()
            await asyncio.sleep(UPDATE_INTERVAL)

    # mostra histórico do DB em um diálogo
    def mostrar_historico(e):
        async def _show():
            rows = await asyncio.to_thread(listar_climas)  # lista do DB
            content_column = ft.Column(spacing=6)
            content_column.controls.append(ft.Text("Histórico (mais recente primeiro):", weight="bold"))
            # limita para não lotar a UI
            for r in rows[:100]:
                cidade, descricao, temperatura, umidade, data_hora = r
                content_column.controls.append(
                    ft.Row(
                        [
                            ft.Text(data_hora, size=12),
                            ft.Text(cidade, weight="bold"),
                            ft.Text(f"{temperatura}°C"),
                            ft.Text(f"{umidade}%"),
                            ft.Text(descricao),
                        ],
                        spacing=10,
                    )
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

    # --- botões / layout ---
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

    # inicia o loop periódico em background (sem bloquear a UI)
    page.run_task(periodic)


if __name__ == "__main__":
    ft.app(target=main)
