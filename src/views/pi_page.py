import flet as ft
from .functions import *

cyfry = "141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420"

def PiPageView(page):
    # ładowanie danych
    groups_data = load_data(page, GROUPS_KEY)

    state={"show_text": False}

    chunks = [cyfry[i:i + 6] for i in range(0, len(cyfry), 6)]
    list_view = ft.ListView(expand=True, spacing=10, padding=20)

    def open_edit_dialog(index, chunk_digits):
        key = str(index)
        current_data = groups_data.get(key, {})

        txt_p = ft.TextField(label="Person", value=current_data.get("P", ""))
        txt_a = ft.TextField(label="Action", value=current_data.get("A", ""))
        txt_o = ft.TextField(label="Object", value=current_data.get("O", ""))

        def close_dlg(e):
            dlg.open = False
            page.update()

        # if word doesnt exists adds it
        def add_pao(digit_pair, pao, text):
            data = load_data(page, PAO_KEY)

            if digit_pair not in data:
                data[digit_pair] = {"P": [], "A": [], "O": []}

            if text not in data[digit_pair][pao] and text != "":
                data[digit_pair][pao].append(text)
                save_data(page, PAO_KEY, data)

        def save_click(e):
            groups_data[key] = {
                "digits": chunk_digits,
                "P": txt_p.value,
                "A": txt_a.value,
                "O": txt_o.value
            }
            save_data(page, GROUPS_KEY, groups_data)

            # save words to major dictionary
            add_pao(str(chunk_digits[0:2]), "P", txt_p.value)
            add_pao(str(chunk_digits[2:4]), "A", txt_a.value)
            add_pao(str(chunk_digits[4:6]), "O", txt_o.value)

            close_dlg(e)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(rf"Group {index}:   {chunk_digits}"),
            content=ft.Column([
                ft.Text(f"Cyfry: {chunk_digits}"),
                txt_p,
                txt_a,
                txt_o
            ], height=300, tight=True),
            actions=[
                ft.TextButton("Anuluj", on_click=close_dlg),
                ft.FilledButton("Zapisz", on_click=save_click)
            ],
        )
        page.overlay.clear()
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def toggle_mode(e):
        state["show_text"] = e.control.value
        render_list(run_update=True)

    def render_list(run_update):
        new_controls =[]

        for i, chunk in enumerate(chunks):
            key = str(i)
            is_described = key in groups_data
            chunk_data = groups_data.get(key, {})

            if state["show_text"]:
                digits_display = f"{chunk[0:2]}  {chunk[2:4]}  {chunk[4:6]}"
                p = chunk_data.get("P", "")
                a = chunk_data.get("A", "")
                o = chunk_data.get("O", "")
                words_display = f"{p} {a} {o}"

                btn_content = ft.Column([
                    ft.Row([
                        ft.Text(digits_display, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_500,)
                    ], alignment=ft.MainAxisAlignment.CENTER, height=18),
                    # ft.Row([
                    ft.Text(words_display, size=18, color=ft.colors.BLUE_800, text_align=ft.TextAlign.CENTER)
                    # ], height=62)
                ])

                btn_height = 80

            else:
                btn_content= ft.Text(chunk, size=20, weight=ft.FontWeight.W_600)
                btn_height = 40

            btn = ft.OutlinedButton(
                content=btn_content,
                height=btn_height,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    side=ft.BorderSide(2, ft.colors.GREEN if is_described else ft.colors.GREY_500),
                    padding=8,
                ),
                on_click=lambda e, idx=i, ch=chunk: open_edit_dialog(index=idx, chunk_digits=ch)
            )
            new_controls.append(btn)

        list_view.controls = new_controls
        if run_update:
            list_view.update()

    render_list(run_update=False)

    return ft.View(
        route="/pi",
        controls=[
            ft.AppBar(
                title=ft.Text("PiPamietaj"),
                bgcolor="blue",
                actions=[
                    ft.Row([
                        ft.Text("Tekst", color="white"),
                        ft.Switch(value=False, on_change=toggle_mode, active_color="white", active_track_color="green"),
                        ft.Container(width=10)
                    ])
                ]
            ),
            list_view,
            ft.FilledButton("Wróć", on_click=lambda _: page.go("/")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
