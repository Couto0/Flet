import flet as ft
from base_config import Config, apply_config


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
            },
            "Inglês": {
                "welcome": "Welcome to the Flet page!",
                "settings": "Settings",
                "theme": "Theme",
                "language": "Language",
                "font": "Font Size",
            },
        }
        return translations.get(config.language, translations["Português"]).get(key, key)

    # Atualiza visual e textos (agora aplica tamanho de fonte corretamente)
    def update_config(e=None):
        # apply_config retorna cores (conforme base_config.py que te mandei antes)
        theme_colors = apply_config(page, config) or {}
        # trocar cores da sidebar se retornadas
        if "sidebar_color" in theme_colors:
            sidebar_container.bgcolor = theme_colors["sidebar_color"]
        if "text_color" in theme_colors:
            text.color = theme_colors["text_color"]
            title.color = theme_colors["text_color"]

        # aplica textos traduzidos
        text.value = translate("welcome")
        title.value = translate("settings")
        theme_dropdown.label = translate("theme")
        lang_dropdown.label = translate("language")
        font_slider.label = translate("font")

        # **Aplique o tamanho da fonte aqui** (corrige o problema)
        # Texto principal:
        text.size = config.font_size
        # Título da sidebar: um pouco maior que o corpo
        title.size = max(config.font_size + 2, 16)

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

    # Controles
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

    text = ft.Text(translate("welcome"), size=config.font_size)

    content = ft.Container(
        ft.Column([text], alignment="center", horizontal_alignment="center"),
        expand=True,
        padding=20,
    )

    page.add(ft.Row([sidebar_container, content], expand=True))

    # aplica tudo inicialmente
    update_config()


ft.app(target=main)
