import flet as ft

DEFAULT_THEME = "Light"
DEFAULT_LANGUAGE = "Português"
DEFAULT_FONT_SIZE = 14


class Config:
    def __init__(self):
        self.theme = DEFAULT_THEME
        self.language = DEFAULT_LANGUAGE
        self.font_size = DEFAULT_FONT_SIZE

    def set_theme(self, value):
        self.theme = value

    def set_language(self, value):
        self.language = value

    def set_font_size(self, value):
        self.font_size = value


def apply_config(page: ft.Page, config: Config):
    """
    Aplica configuração básica de tema na página.
    Retorna um dicionário com cores úteis para usar na UI.
    """
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


def create_sidebar(restart_fn, toggle_theme_fn, config: Config):
    """
    Retorna uma Column configurada para ser usada como sidebar.
    restart_fn e toggle_theme_fn são callbacks (funções) que serão chamadas pelos botões.
    """
    theme_button = ft.ElevatedButton(
        text=f"Tema: {config.theme}",
        on_click=toggle_theme_fn,
        width=160
    )

    restart_button = ft.ElevatedButton(
        text="Reiniciar Jogo",
        on_click=restart_fn,
        width=160
    )

    info = ft.Column(
        [
            ft.Text("Jogo do Milhão", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Instruções:", size=12),
            ft.Text("Responda cada pergunta para subir de nível.", size=12),
            ft.Container(height=10),
            theme_button,
            restart_button,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        width=180,
        padding=10,
    )

    return info, theme_button