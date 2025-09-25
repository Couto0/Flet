import flet as ft

def main(page: ft.Page):
    page.title = "Calculadora de Custo de Viagem"
    page.scroll = "adaptive"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.bgcolor = "blue50"   # cor de fundo ciano clara
    page.theme_mode = "sistem"

    # ---------- CAMPOS DE ENTRADA ----------
    distancia = ft.TextField(
        label="Distância",
        suffix_text="km",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        border_radius=10,
        bgcolor = "WHITE" 
    )
    consumo = ft.TextField(
        label="Consumo",
        suffix_text="km/L",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        border_radius=10,
        bgcolor = "WHITE" 
    )
    preco_comb = ft.TextField(
        label="Preço Comb.",
        suffix_text="R$/L",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        border_radius=10,
        bgcolor = "WHITE" 
    )
    pedagios = ft.TextField(
        label="Pedágios",
        suffix_text="R$",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
        border_radius=10,
        bgcolor = "WHITE" 
    )

    ida_volta = ft.Switch(label="Viagem de Ida e Volta", value=False)

    # ---------- ÁREA DE RESULTADOS ----------
    litros_txt = ft.Text("⛽ Litros Necessários: 0.0 L")
    combustivel_txt = ft.Text("💰 Custo Combustível: R$ 0.00")
    pedagios_txt = ft.Text("🏷️ Custo Pedágios: R$ 0.00")
    total_txt = ft.Text("💵 CUSTO TOTAL: R$ 0.00", size=18, weight="bold", color="green")

    card_resultado = ft.Card(
        visible=False,
        elevation=6,
        color="white",
        content=ft.Container(
            content=ft.Column([
                ft.Text("📊 Resumo da Viagem", size=20, weight="bold", color="#333"),
                ft.Divider(),
                litros_txt,
                combustivel_txt,
                pedagios_txt,
                ft.Divider(),
                total_txt
            ]),
            padding=20,
            border_radius=15,
        )
    )

    # ---------- FUNÇÃO DE CÁLCULO ----------
    def calcular_custo(e):
        try:
            dist = float(distancia.value.replace(',', '.'))
            cons = float(consumo.value.replace(',', '.'))
            preco = float(preco_comb.value.replace(',', '.'))
            pedagio = float(pedagios.value.replace(',', '.'))

            if ida_volta.value:
                dist *= 2

            litros = dist / cons
            custo_comb = litros * preco
            custo_ped = pedagio * (2 if ida_volta.value else 1)
            custo_total = custo_comb + custo_ped
            

            litros_txt.value = f"⛽ Litros Necessários: {litros:.2f} L"
            combustivel_txt.value = f"💰 Custo Combustível: R$ {custo_comb:.2f}"
            pedagios_txt.value = f"🏷️ Custo Pedágios: R$ {custo_ped:.2f}"
            total_txt.value = f"💵 CUSTO TOTAL: R$ {custo_total:.2f}"

            card_resultado.visible = True
            page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Preencha todos os campos com números válidos!"))
            page.snack_bar.open = True
            page.update()

    # ---------- BOTÃO ----------
    btn_calcular = ft.FilledButton(
        "CALCULAR CUSTO",
        on_click=calcular_custo,
        style=ft.ButtonStyle(
            bgcolor="#0077b6",
            color="white",
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=15
        )
    )

    # ---------- LAYOUT ----------
    page.add(
        ft.AppBar(title=ft.Text("🚗 Calculadora de Viagem", size=20, weight="bold"), center_title=True, bgcolor="#0077b6", color="white"),
        ft.Column([
            ft.Row([distancia, consumo], alignment = "center", vertical_alignment = "end"),
            ft.Row([preco_comb, pedagios], alignment = "center", vertical_alignment = "end"),
            ft.Row([ida_volta], alignment="center", vertical_alignment = "end"),
            btn_calcular,
            ft.Divider(),
            card_resultado
        ], expand=True, spacing=20, horizontal_alignment="center")
    )

ft.app(target=main)