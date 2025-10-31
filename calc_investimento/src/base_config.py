import flet as ft

DEFAULT_THEME = "Light"
DEFAULT_FONT_SIZE = 14


class Config:
    def __init__(self):
        self.theme = DEFAULT_THEME
        self.font_size = DEFAULT_FONT_SIZE

    def set_theme(self, value):
        self.theme = value

    def set_font_size(self, value):
        self.font_size = value


def apply_config(page: ft.Page, config: Config):
    if config.theme == "Dark":
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = ft.Colors.BLACK
        page.color = ft.Colors.WHITE
        sidebar_color = ft.Colors.BLACK38
        text_color = ft.Colors.WHITE
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.bgcolor = ft.Colors.BLUE_GREY_50
        page.color = ft.Colors.BLACK
        sidebar_color = ft.Colors.GREY_200
        text_color = ft.Colors.BLACK

    return {
        "sidebar_color": sidebar_color,
        "text_color": text_color,
    }


def create_sidebar(page: ft.Page):
    """
    Cria e retorna a barra lateral de configurações e o objeto Config.
    NÃO adiciona nada à página automaticamente.
    """
    config = Config()

    def update_config(e=None):
        theme_colors = apply_config(page, config)
        sidebar_container.bgcolor = theme_colors["sidebar_color"]
        title.color = theme_colors["text_color"]
        title.size = max(config.font_size + 2, 16)
        page.update()

    sidebar_visible = True

    def toggle_sidebar(e):
        nonlocal sidebar_visible
        sidebar_visible = not sidebar_visible
        sidebar_container.width = 250 if sidebar_visible else 60
        toggle_icon.icon = ft.Icons.MENU_OPEN if sidebar_visible else ft.Icons.MENU
        for c in sidebar.controls[1:]:
            c.visible = sidebar_visible
        page.update()

    toggle_icon = ft.IconButton(
        icon=ft.Icons.MENU_OPEN,
        tooltip="Mostrar/ocultar menu",
        on_click=toggle_sidebar,
    )

    title = ft.Text("Configurações", weight="bold", size=max(config.font_size + 2, 16))

    theme_dropdown = ft.Dropdown(
        label="Tema",
        value=config.theme,
        options=[ft.dropdown.Option("Light"), ft.dropdown.Option("Dark")],
        on_change=lambda e: (config.set_theme(e.control.value), update_config()),
    )

    font_slider = ft.Slider(
        label="Tamanho da Fonte",
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

    apply_config(page, config)
    return config, sidebar_container
