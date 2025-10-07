import flet as ft
from base_config import Config, apply_config
from finance_utils import calculate_compound_interest, validate_investment_inputs


def main(page: ft.Page):
    page.title = "Painel de Configurações"
    config = Config()

    # Traduções simples
    def translate(key):
        translations = {
            "Português": {
                "welcome": "Bem-vindo à página Flet!",
                "settings": "Configurações",
                "theme": "Tema",
                "language": "Idioma",
                "font": "Tamanho da Fonte",
                "calculator": "Calculadora de Investimentos",
                "initial_value": "Valor Inicial (R$)",
                "monthly_deposit": "Aporte Mensal (R$)",
                "interest_rate": "Taxa de Juros Anual (%)",
                "time_period": "Período (anos)",
                "calculate": "Calcular",
                "final_amount": "Montante Final:",
                "total_invested": "Total Investido:",
                "interest_earned": "Juros Obtidos:",
                "evolution_chart": "Evolução do Investimento",
            },
            "Inglês": {
                "welcome": "Welcome to the Flet page!",
                "settings": "Settings",
                "theme": "Theme",
                "language": "Language",
                "font": "Font Size",
                "calculator": "Investment Calculator",
                "initial_value": "Initial Value ($)",
                "monthly_deposit": "Monthly Deposit ($)",
                "interest_rate": "Annual Interest Rate (%)",
                "time_period": "Time Period (years)",
                "calculate": "Calculate",
                "final_amount": "Final Amount:",
                "total_invested": "Total Invested:",
                "interest_earned": "Interest Earned:",
                "evolution_chart": "Investment Evolution",
            },
        }
        return translations.get(config.language, translations["Português"]).get(key, key)

    # Atualiza visual e textos
    def update_config(e=None):
        theme_colors = apply_config(page, config) or {}
        if "sidebar_color" in theme_colors:
            sidebar_container.bgcolor = theme_colors["sidebar_color"]
        if "text_color" in theme_colors:
            text.color = theme_colors["text_color"]
            title.color = theme_colors["text_color"]
            calculator_title.color = theme_colors["text_color"]
            result_text.color = theme_colors["text_color"]

        # aplica textos traduzidos
        text.value = translate("welcome")
        title.value = translate("settings")
        theme_dropdown.label = translate("theme")
        lang_dropdown.label = translate("language")
        font_slider.label = translate("font")
        calculator_title.value = translate("calculator")
        initial_value_field.label = translate("initial_value")
        monthly_deposit_field.label = translate("monthly_deposit")
        interest_rate_field.label = translate("interest_rate")
        time_period_field.label = translate("time_period")
        calculate_button.text = translate("calculate")
        chart_title.value = translate("evolution_chart")

        # Aplica o tamanho da fonte
        text.size = config.font_size
        title.size = max(config.font_size + 2, 16)
        calculator_title.size = max(config.font_size + 2, 16)
        result_text.size = config.font_size

        page.update()

    # Calculadora de Investimentos
    def calculate_investment(e):
        # Validar inputs
        is_valid, error_message = validate_investment_inputs(
            initial_value_field.value,
            monthly_deposit_field.value,
            interest_rate_field.value,
            time_period_field.value
        )
        
        if not is_valid:
            result_text.value = error_message
            page.update()
            return
        
        try:
            # Obter valores dos campos
            initial_value = float(initial_value_field.value or 0)
            monthly_deposit = float(monthly_deposit_field.value or 0)
            annual_interest_rate = float(interest_rate_field.value or 0)
            years = int(time_period_field.value or 0)
            
            # Calcular usando a função do finance_utils
            result = calculate_compound_interest(
                initial_value, monthly_deposit, annual_interest_rate, years
            )
            
            if 'error' in result:
                result_text.value = f"Erro no cálculo: {result['error']}"
                page.update()
                return
            
            # Atualizar resultado
            currency_symbol = "R$" if config.language == "Português" else "$"
            result_text.value = (
                f"{translate('final_amount')} {currency_symbol} {result['final_amount']:,.2f}\n"
                f"{translate('total_invested')} {currency_symbol} {result['total_invested']:,.2f}\n"
                f"{translate('interest_earned')} {currency_symbol} {result['interest_earned']:,.2f}"
            )
            
            # Atualizar gráfico apenas se houver dados
            if result['data_points']:
                # Limpar série anterior
                if hasattr(chart, 'data_series'):
                    chart.data_series.clear()
                
                # Criar nova série
                data_series = ft.LineChartData(
                    data_points=[
                        ft.LineChartDataPoint(month, amount) 
                        for month, amount in result['data_points']
                    ],
                    stroke_width=3,
                    color=ft.Colors.BLUE_400,
                    curved=False,  # Simplificado para evitar problemas
                    stroke_cap_round=True,
                )
                
                chart.data_series = [data_series]
            
            page.update()
            
        except Exception as ex:
            result_text.value = f"Erro: {str(ex)}"
            page.update()

    # Alterna a visibilidade da sidebar
    sidebar_visible = True

    def toggle_sidebar(e):
        nonlocal sidebar_visible
        sidebar_visible = not sidebar_visible
        sidebar_container.width = 250 if sidebar_visible else 60
        toggle_icon.icon = ft.Icons.MENU_OPEN if sidebar_visible else ft.Icons.MENU
        for c in sidebar.controls[1:]:
            c.visible = sidebar_visible
        page.update()

    # Botão de menu
    toggle_icon = ft.IconButton(
        icon=ft.Icons.MENU_OPEN,
        tooltip="Mostrar/ocultar menu",
        on_click=toggle_sidebar,
    )

    title = ft.Text(translate("settings"), weight="bold", size=max(config.font_size + 2, 16))

    # Controles de configuração
    theme_dropdown = ft.Dropdown(
        label=translate("theme"),
        value=config.theme,
        options=[ft.dropdown.Option("Light"), ft.dropdown.Option("Dark")],
        on_change=lambda e: (config.set_theme(e.control.value), update_config()),
    )

    lang_dropdown = ft.Dropdown(
        label=translate("language"),
        value=config.language,
        options=[ft.dropdown.Option("Português"), ft.dropdown.Option("Inglês")],
        on_change=lambda e: (config.set_language(e.control.value), update_config()),
    )

    font_slider = ft.Slider(
        label=translate("font"),
        min=10,
        max=32,
        value=config.font_size,
        divisions=22,
        on_change=lambda e: (config.set_font_size(int(e.control.value)), update_config()),
    )

    sidebar = ft.Column(
        [
            ft.Row([toggle_icon, title], alignment="start"),
            ft.Divider(),
            theme_dropdown,
            lang_dropdown,
            font_slider,
        ],
        spacing=15,
        expand=True,
        alignment="start",
    )

    sidebar_container = ft.Container(
        sidebar,
        width=250,
        bgcolor=ft.Colors.GREY_200,
        padding=15,
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
        ),
    )

    # Elementos da calculadora
    calculator_title = ft.Text(translate("calculator"), weight="bold", size=max(config.font_size + 2, 16))
    
    initial_value_field = ft.TextField(
        label=translate("initial_value"),
        value="1000",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )
    
    monthly_deposit_field = ft.TextField(
        label=translate("monthly_deposit"),
        value="100",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )
    
    interest_rate_field = ft.TextField(
        label=translate("interest_rate"),
        value="8",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )
    
    time_period_field = ft.TextField(
        label=translate("time_period"),
        value="10",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200
    )
    
    calculate_button = ft.ElevatedButton(
        text=translate("calculate"),
        on_click=calculate_investment
    )
    
    result_text = ft.Text(size=config.font_size)
    
    chart_title = ft.Text(translate("evolution_chart"), size=max(config.font_size, 14))
    
    # Gráfico simplificado
    chart = ft.LineChart(
        data_series=[],
        border=ft.border.all(1, ft.Colors.GREY_400),
        expand=True,
        height=300
    )

    # Layout da calculadora
    calculator_controls = ft.Column([
        calculator_title,
        ft.Row([initial_value_field, monthly_deposit_field]),
        ft.Row([interest_rate_field, time_period_field]),
        calculate_button,
        result_text,
    ], spacing=15)

    calculator_content = ft.Column([
        calculator_controls,
        ft.Divider(),
        chart_title,
        chart
    ], expand=True, scroll=ft.ScrollMode.ADAPTIVE)

    text = ft.Text(translate("welcome"), size=config.font_size)

    # Conteúdo principal com abas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Início",
                content=ft.Container(
                    ft.Column([text], alignment="center", horizontal_alignment="center"),
                    expand=True,
                    padding=20,
                )
            ),
            ft.Tab(
                text="Calculadora",
                content=ft.Container(
                    calculator_content,
                    expand=True,
                    padding=20,
                )
            ),
        ],
        expand=1,
    )

    content = ft.Container(tabs, expand=True)

    page.add(ft.Row([sidebar_container, content], expand=True))

    # aplica tudo inicialmente
    update_config()


ft.app(target=main)