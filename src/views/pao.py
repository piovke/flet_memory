import flet as ft
from flet_core import MainAxisAlignment

from .functions import *


def PaoPageView(page):
    def delete_all_data():
        keys_to_remove = [GROUPS_KEY, PAO_KEY, BIRTHDAY_KEY]

        # KROK 1: Usuwanie z Client Storage (To jest to, co "pamięta" mimo usunięcia plików)
        try:
            if hasattr(page, 'client_storage') and page.client_storage:
                # Metoda clear() czyści CAŁY schowek aplikacji
                page.client_storage.clear()
                print("Wyczyszczono Client Storage.")

                # Alternatywnie, jeśli chcesz usunąć tylko konkretne klucze, a nie wszystko:
                # for key in keys_to_remove:
                #     page.client_storage.remove(key)
        except Exception as e:
            print(f"Błąd podczas czyszczenia Client Storage: {e}")

        # KROK 2: Usuwanie fizycznych plików JSON
        for key in keys_to_remove:
            filename = f"{key}.json"
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Usunięto plik: {filename}")
            except Exception as e:
                print(f"Nie udało się usunąć pliku {filename}: {e}")

        # Opcjonalnie: Pokaż komunikat użytkownikowi
        page.snack_bar = ft.SnackBar(ft.Text("Wszystkie dane zostały usunięte!"), bgcolor="red")
        page.snack_bar.open = True
        page.update()
    # delete_all_data()

    pao_data = load_data(page, PAO_KEY)

    # Kontener na listę przycisków
    rows_of_buttons = ft.ListView(expand=True, spacing=8, padding=10)

    def open_bottom_sheet(pair):
        key = str(pair)
        data = pao_data.get(key, {}) if pao_data else {}

        # making lists of words
        list_p = ft.Row(wrap=True)
        list_a = ft.Row(wrap=True)
        list_o = ft.Row(wrap=True)
        for person in data.get("P", []):
            list_p.controls.append(
                ft.OutlinedButton(
                    person,
                    style=ft.ButtonStyle(
                        padding=8,
                    ),
                on_click=lambda e, word=person,digit_pair=key: delete_pao_word_dialog(word_to_delete=word, pao="P", pair=digit_pair)
                ),            )
        for action in data.get("A", []):
            list_a.controls.append(
                ft.OutlinedButton(
                    action,
                    style=ft.ButtonStyle(
                        padding=8
                    ) ,
                on_click=lambda e, word=action,digit_pair=key: delete_pao_word_dialog(word_to_delete=word, pao="A", pair=digit_pair)
                ),            )
        for obj in data.get("O", []):
            list_o.controls.append(
                ft.OutlinedButton(
                    obj,
                    style=ft.ButtonStyle(
                        padding=8
                    ),
                on_click=lambda e, word=obj,digit_pair=key: delete_pao_word_dialog(word_to_delete=word, pao="O", pair=digit_pair)
                ),            )

        def close_bs(e):
            bs.open = False
            page.update()

        # Definicja BottomSheet
        bs = ft.BottomSheet(
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        # Nagłówek
                        ft.Row(
                            [
                                ft.Text(f"Pair: {pair}", size=24, weight=ft.FontWeight.BOLD),
                                ft.IconButton(icon="close", on_click=close_bs)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),

                        ft.Divider(),

                        # Treść
                        ft.Text(f"Person:"),
                        list_p,
                        ft.Text(f"Action:"),
                        list_a,
                        ft.Text(f"Object:"),
                        list_o,

                        ft.Container(height=20),

                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon="add",
                                    bgcolor="blue",
                                    on_click=lambda e: open_add_pao_dialog(pair)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            expand=True
                        )
                    ],
                    tight=False,
                )
            ),
            dismissible=True,
            enable_drag=True,
        )
        #open panel
        page.bottom_sheet = bs
        bs.open = True
        page.update()

    def open_add_pao_dialog(pair):
        def close_dlg(e):
            dlg.open = False
            page.update()

        def save_click(e):
            add_pao(page, pair_text.value, list(category_selector.selected)[0], word_text.value)
            #update
            nonlocal pao_data
            pao_data = load_data(page, PAO_KEY)
            close_dlg(e)

        category_selector = ft.SegmentedButton(
            segments=[
                ft.Segment(
                    value="P",
                    label=ft.Text("Person")
                ),
                ft.Segment(
                    value="A",
                    label=ft.Text("Action")
                ),
                ft.Segment(
                    value="O",
                    label=ft.Text("Object")
                ),
            ],
            allow_multiple_selection=False,
            allow_empty_selection=False,
            selected={"A"},
        )

        pair_text = ft.TextField(label="Pair", value=pair)
        word_text = ft.TextField(label="Word", value="")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(rf"Add word"),
            content=ft.Column([
                pair_text,
                category_selector,
                word_text,
            ], height=200, tight=True),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton("Anuluj", on_click=close_dlg),
                        ft.FilledButton("Zapisz", on_click=save_click)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ],
        )
        page.overlay.clear()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def delete_pao_word_dialog(pair, pao, word_to_delete):
        def close_dlg(e):
            dlg.open = False
            page.update()

        def confirm_delete(e):
            delete_pao(page, pair, pao, word_to_delete)
            #update
            nonlocal pao_data
            pao_data = load_data(page, PAO_KEY)
            close_dlg(e)

        pao_string = "Action" if pao =="A" else "Person" if pao =="P" else "Object"

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Text("Delete word?"),
                    ft.Text(rf"{pair}", weight=ft.FontWeight.BOLD, size=32)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            content=ft.Column([
                ft.Row(
                    controls=[
                        ft.Text(f"{word_to_delete}", size=24, weight=ft.FontWeight.W_600)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,expand=True),
                ft.Row(
                    controls=[
                        ft.Text(f"({pao_string})")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, expand=True),
            ], height=80, tight=True),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton("Anuluj", on_click=close_dlg),
                        ft.FilledButton("Usuń", on_click=confirm_delete)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()


    def create_button_list():
        for i in range(0, 100, 4):
            row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            for j in range(i, i + 4):
                val = f"{j:02d}"

                btn = ft.OutlinedButton(
                    content=ft.Text(val, size=20),
                    height=35,
                    on_click=lambda e, pair=val: open_bottom_sheet(pair),
                    width=80
                )
                row.controls.append(btn)
            rows_of_buttons.controls.append(row)

    create_button_list()

    return ft.View(
        route="/pao",
        controls=[
            ft.AppBar(
                title=ft.Text("PAO"),
                bgcolor="blue",
            ),
            rows_of_buttons,
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon="add",
                        bgcolor="blue",
                        on_click=lambda e: open_add_pao_dialog("")
                    )
                ],
                alignment=MainAxisAlignment.END,
            )

        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )