import flet as ft
from base_config import create_sidebar
from finance_utils import calculate_compound_interest, validate_investment_inputs


def main(page: ft.Page):
    page.title = "Calculadora de Investimentos"

    # Cria (mas não adiciona) a sidebar
    config, sidebar = create_sidebar(page)

    # Campos de entrada
    initial_value_field = ft.TextField(label="Valor Inicial (R$)", value="1000", width=200)
    monthly_deposit_field = ft.TextField(label="Aporte Mensal (R$)", value="100", width=200)
    interest_rate_field = ft.TextField(label="Taxa de Juros Anual (%)", value="8", width=200)
    time_period_field = ft.TextField(label="Período (anos)", value="10", width=200)

    result_text = ft.Text(size=config.font_size)

    chart = ft.LineChart(
        data_series=[],
        border=ft.border.all(1, ft.Colors.GREY_400),
        expand=True,
        height=300,
    )

    def calculate_investment(e):
        is_valid, error_message = validate_investment_inputs(
            initial_value_field.value,
            monthly_deposit_field.value,
            interest_rate_field.value,
            time_period_field.value,
        )

        if not is_valid:
            result_text.value = error_message
            page.update()
            return

        result = calculate_compound_interest(
            float(initial_value_field.value or 0),
            float(monthly_deposit_field.value or 0),
            float(interest_rate_field.value or 0),
            int(time_period_field.value or 0),
        )

        if "error" in result:
            result_text.value = f"Erro: {result['error']}"
        else:
            result_text.value = (
                f"Montante Final: R$ {result['final_amount']:,.2f}\n"
                f"Total Investido: R$ {result['total_invested']:,.2f}\n"
                f"Juros Obtidos: R$ {result['interest_earned']:,.2f}"
            )

            chart.data_series.clear()
            chart.data_series.append(
                ft.LineChartData(
                    data_points=[
                        ft.LineChartDataPoint(m, a) for m, a in result["data_points"]
                    ],
                    stroke_width=3,
                    color=ft.Colors.BLUE_400,
                )
            )

        page.update()

    calculate_button = ft.ElevatedButton(text="Calcular", on_click=calculate_investment)

    calculator_content = ft.Column(
        [
            ft.Text("Calculadora de Investimentos", weight="bold", size=config.font_size + 2),
            ft.Row([initial_value_field, monthly_deposit_field]),
            ft.Row([interest_rate_field, time_period_field]),
            calculate_button,
            result_text,
            ft.Divider(),
            ft.Text("Evolução do Investimento", size=config.font_size + 1),
            chart,
        ],
        spacing=15,
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    content = ft.Container(calculator_content, expand=True, padding=20)

    #  Adiciona tudo uma única vez
    page.add(ft.Row([sidebar, content], expand=True))


ft.app(target=main)
