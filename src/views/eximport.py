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

    # --- OBSŁUGA IMPORTU (Wczytywanie pliku) ---
    def on_dialog_result(e):
        operation = current_action["operation"]
        key = current_action["key"]

        if not e.files:
            return

        try:
            if operation == "import" and e.files:
                file_path = e.files[0].path
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                save_data_to_storage(key, data)

                page.snack_bar = ft.SnackBar(ft.Text(f"Sukces! Zaimportowano dane."), bgcolor="green")
                page.snack_bar.open = True

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Błąd: {ex}"), bgcolor="red")
            page.snack_bar.open = True

        page.update()

    # Tworzenie FilePickera (tylko do importu)
    file_picker = ft.FilePicker()
    file_picker.on_result = on_dialog_result

    page.overlay.append(file_picker)
    page.update()

    # --- FUNKCJE PRZYCISKÓW ---

    def click_copy_to_clipboard(e):
        key_alias = e.control.data
        storage_key = KEY_MAPPING.get(key_alias)

        if storage_key:
            # 1. Pobierz dane
            data = get_data_from_storage(storage_key)

            # 2. Zamień na tekst (JSON)
            json_text = json.dumps(data, ensure_ascii=False, indent=4)

            # 3. Wrzuć do schowka systemowego
            page.set_clipboard(json_text)

            # 4. Pokaż komunikat
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Skopiowano {key_alias.upper()}! Wklej to teraz do maila lub notatnika."),
                bgcolor="orange"
            )
            page.snack_bar.open = True
            page.update()

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
    def create_row(title, key_alias):
        return ft.Container(
            content=ft.Row([
                ft.Text(title, size=20, width=120),

                # PRZYCISK 1: KOPIUJ (Zamiast Eksport)
                ft.ElevatedButton(
                    "Kopiuj",  # Zmieniona nazwa
                    icon="copy",  # Zmieniona ikona
                    data=key_alias,
                    on_click=click_copy_to_clipboard,  # Nowa funkcja
                    bgcolor="orange100",
                    color="black"
                ),
                ft.ElevatedButton(
                    "Wczytaj",
                    icon="download",
                    data=key_alias,
                    on_click=click_import,
                    bgcolor="blue100",
                    color="black"
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            border_radius=10,
            bgcolor="#212121"
        )

    return ft.View(
        route="/eximport",
        controls=[
            ft.AppBar(title=ft.Text("Kopia Zapasowa"), bgcolor="blue"),

            ft.Column([
                create_row("PAO", "pao"),
                create_row("Grupy 00-99", "groups"),
                create_row("Urodziny", "birthdays"),
            ], spacing=20),
        ],
        vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )