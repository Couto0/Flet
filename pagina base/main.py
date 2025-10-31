import flet as ft
from base_config import add_sidebar_config

def main(page: ft.Page):
    add_sidebar_config(page)

ft.app(target=main)