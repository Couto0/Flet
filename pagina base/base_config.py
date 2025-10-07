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

    # Retorna cores para outros elementos
    return {
        "sidebar_color": sidebar_color,
        "text_color": text_color,
    }