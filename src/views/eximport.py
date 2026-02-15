import flet as ft
import json
from .functions import GROUPS_KEY, PAO_KEY, BIRTHDAY_KEY


def ExImportView(page):
    KEY_MAPPING = {
        "pao": PAO_KEY,
        "groups": GROUPS_KEY,
        "birthdays": BIRTHDAY_KEY
    }

    current_action = {
        "operation": None,
        "key": None
    }

    def get_data_from_storage(key):
        if hasattr(page, 'client_storage') and page.client_storage:
            if page.client_storage.contains_key(key):
                return page.client_storage.get(key)
        return {}

    def save_data_to_storage(key, data):
        if hasattr(page, 'client_storage') and page.client_storage:
            page.client_storage.set(key, data)

    # --- OBSŁUGA FILE PICKERA ---
    def on_dialog_result(e):
        operation = current_action["operation"]
        key = current_action["key"]

        if not e.files and not e.path:
            return

        try:
            if operation == "import" and e.files:
                file_path = e.files[0].path
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                save_data_to_storage(key, data)

                page.snack_bar = ft.SnackBar(ft.Text(f"Sukces! Zaimportowano dane."), bgcolor="green")
                page.snack_bar.open = True

            elif operation == "export" and e.path:
                data = get_data_from_storage(key)

                with open(e.path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                page.snack_bar = ft.SnackBar(ft.Text(f"Sukces! Zapisano w: {e.path}"), bgcolor="green")
                page.snack_bar.open = True

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Błąd: {ex}"), bgcolor="red")
            page.snack_bar.open = True

        page.update()

    # Tworzenie FilePickera
    file_picker = ft.FilePicker()
    file_picker.on_result = on_dialog_result

    page.overlay.append(file_picker)
    page.update()

    # --- FUNKCJE PRZYCISKÓW ---

    def click_export(e):
        key_alias = e.control.data
        storage_key = KEY_MAPPING.get(key_alias)

        if storage_key:
            current_action["operation"] = "export"
            current_action["key"] = storage_key

            file_picker.save_file(
                dialog_title=f"Eksportuj {key_alias.upper()}",
                file_name=f"{key_alias}_backup.json",
                allowed_extensions=["json"]
            )

    def click_import(e):
        key_alias = e.control.data
        storage_key = KEY_MAPPING.get(key_alias)

        if storage_key:
            current_action["operation"] = "import"
            current_action["key"] = storage_key

            file_picker.pick_files(
                dialog_title=f"Wybierz plik {key_alias.upper()}",
                allowed_extensions=["json"],
                allow_multiple=False
            )

    # --- UI ---
    def create_row(title, key_alias, bg_color_str):
        return ft.Container(
            content=ft.Row([
                ft.Text(title, size=20, width=90),
                ft.ElevatedButton(
                    "Eksport",
                    # POPRAWKA: Używamy zwykłego tekstu dla ikony
                    icon="upload",
                    data=key_alias,
                    on_click=click_export,
                    bgcolor="green100",
                    color="black"
                ),
                ft.ElevatedButton(
                    "Import",
                    # POPRAWKA: Używamy zwykłego tekstu dla ikony
                    icon="download",
                    data=key_alias,
                    on_click=click_import,
                    bgcolor="blue100",
                    color="black"
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor=bg_color_str,
            border_radius=10
        )

    return ft.View(
        route="/eximport",
        controls=[
            ft.AppBar(title=ft.Text("Eksport / Import"), bgcolor="blue"),

            ft.Column([
                create_row("PAO", "pao", "amber50"),
                create_row("Grupy", "groups", "amber50"),
                create_row("Urodziny", "birthdays", "amber50"),
            ], spacing=15),

            ft.Container(height=20),
            ft.FilledButton("Wróć do Menu", on_click=lambda _: page.go("/"), width=200)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )