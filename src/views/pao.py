import flet as ft
from .functions import *

def PaoPageView(page):
    pao_data = load_data(page, PAO_KEY)

    rows_of_buttons = ft.ListView(expand=True, spacing=8, padding=10)

    def create_list():
        for i in range(0,100,4):
            row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            for j in range(i,i+4):
                btn = ft.OutlinedButton(
                    content=ft.Text(f"{j:02d}", size=20),
                    height=35
                )
                row.controls.append(btn)
            rows_of_buttons.controls.append(row)

    create_list()

    return ft.View(
        route = "/pao",
        controls=[
            rows_of_buttons,
            ft.IconButton(
                icon="add"
            )
        ],
         # vertical_alignment=ft.MainAxisAlignment.CENTER,
         horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

