import flet as ft
from .digits import cyfry
import json
import os

GROUPS_FILE = "groups.json"
def load_groups():
    if not os.path.exists(GROUPS_FILE):
        return {}
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Błąd ładowania JSON: {e}")
        return {}

def save_groups(data):
    try:
        with open(GROUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd zapisu JSON: {e}")

buttons_list = []
chunks = [cyfry[i:i+6] for i in range(0,len(cyfry),6)]
for i,chunk in enumerate(chunks):
    btn = ft.OutlinedButton(
        content=chunk,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=lambda e, code=i: print(f"Kliknięto grupę: {code}")
    )
    buttons_list.append(btn)

def PiPageView(page):
    return ft.View(
        route="/pi",
        controls=[
            ft.AppBar(title=ft.Text("PiPamietaj"), bgcolor="red"),
            ft.ListView(
                controls = buttons_list,
                expand = True,
                spacing = 10,
                padding = 20
            ),
            ft.FilledButton("Wróć", on_click=lambda _: page.go("/")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )