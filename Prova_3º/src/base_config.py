# Configurações básicas da aplicação: tema, linguagem, tamanho da fonte.
import flet as ft

DEFAULT_THEME = "Light"
DEFAULT_LANGUAGE = "Português"
DEFAULT_FONT_SIZE = 14


class Config: # Configurações básicas da aplicação
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
    # Aplica as configurações da instância Config ao objeto Page do Flet.
    if config.theme == "Dark": # Tema escuro
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = ft.Colors.BLACK
        page.color = ft.Colors.WHITE
        sidebar_color = ft.Colors.BLACK38
        text_color = ft.Colors.WHITE
    else: # Tema claro
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
# Cria a barra lateral com botões de reiniciar e alternar tema.
    theme_button = ft.ElevatedButton(
        text=f"Tema: {config.theme}",
        on_click=toggle_theme_fn,
        width=160
    ) # Botão para alternar tema

    restart_button = ft.ElevatedButton(
        text="Reiniciar",
        on_click=restart_fn,
        width=160
    ) # Botão para reiniciar a aplicação

    info = ft.Column(
        [
            ft.Container(height=10),
            theme_button,
            restart_button,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        width=180,
    )# Barra lateral

    return info, theme_button