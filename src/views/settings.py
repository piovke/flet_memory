import flet as ft
from .functions import load_data, save_data, SETTINGS_KEY

#freaky so you can add more settings and update app
def load_settings(page):
    default_settings = {
        "ignore_parentheses": True,
        "show_help": True,
        "hide_suggestions_on_keyboard": False,

        "letters": {
            "0": "z s",
            "1": "j dż",
            "2": "d t",
            "3": "w f",
            "4": "cz r",
            "5": "l ł",
            "6": "sz ż",
            "7": "m n",
            "8": "g k",
            "9": "p b",
        }

    }
    saved_settings = load_data(page, SETTINGS_KEY)
    settings = default_settings.copy()
    if isinstance(saved_settings, dict):
        settings.update(saved_settings)
    return settings

def SettingsView(page):
    settings = load_data(page, SETTINGS_KEY)

    return ft.View(
        route="/settings",
        controls=[
            ft.AppBar(title=ft.Text("Settings"), bgcolor="blue"),
            ft.Container(
                content=ft.Column([
                    ft.Text("", size=30),
                ]),
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        ]
    )