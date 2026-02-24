import flet as ft
from .functions import *
from .settings import load_settings
import re

cyfry = "141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420"

def PiPageView(page):
    # ładowanie danych
    groups_data = load_data(page, GROUPS_KEY)
    settings = load_settings(page)

    state={"show_text": False}

    chunks = [cyfry[i:i + 6] for i in range(0, len(cyfry), 6)]
    list_view = ft.ListView(expand=True, spacing=10, padding=20)

    def open_edit_dialog(index, chunk_digits):
        key = str(index)
        current_data = groups_data.get(key, {})
        digits_p = chunk_digits[0:2]
        digits_a = chunk_digits[2:4]
        digits_o = chunk_digits[4:6]

        txt_p = ft.TextField(label=f"Person ({digits_p})", value=current_data.get("P", ""))
        txt_a = ft.TextField(label=f"Action ({digits_a})", value=current_data.get("A", ""))
        txt_o = ft.TextField(label=f"Object ({digits_o})", value=current_data.get("O", ""))

        def suggest_pao_word(pair, pao, textfield):
            # lists of suggestions
            suggestions = get_pao_suggestions(page, pair, pao)

            def use_suggestion(e):
                textfield.value = e.control.label.value
                page.update()

            suggestions_row = ft.Row(
                controls=[],
                wrap=False,
                scroll=ft.ScrollMode.HIDDEN,
                spacing=5,
                height=50,
                vertical_alignment=ft.CrossAxisAlignment.START
            )

            if len(suggestions) == 0:
                pao_string = "Action" if pao == "A" else "Person" if pao == "P" else "Object"
                suggestions_row.controls.append(
                    ft.Text(f"No {pao_string} for digits {pair}", size=12, color="grey")
                )
            else:
                for suggestion in suggestions:
                    suggestions_row.controls.append(
                        ft.Chip(
                            label=ft.Text(suggestion, size=12),
                            on_click=use_suggestion,
                            height=32,
                        )
                    )
            return suggestions_row

        def close_dlg(e):
            dlg.open = False
            page.update()

        def save_click(e):
            groups_data[key] = {
                "digits": chunk_digits,
                "P": txt_p.value.strip(),
                "A": txt_a.value.strip(),
                "O": txt_o.value.strip()
            }
            save_data(page, GROUPS_KEY, groups_data)

            def format_text(text):
                result = text
                if settings["ignore_parentheses"]:
                    result = re.sub(r'\s?\(.*?\)', '', text)
                return result.strip()

            # save words to major dictionary
            add_pao(page, str(digits_p), "P", format_text(txt_p.value))
            add_pao(page, str(digits_a), "A", format_text(txt_a.value))
            add_pao(page, str(digits_o), "O", format_text(txt_o.value))

            render_list(run_update=True)
            close_dlg(e)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(rf"Group {index}:   {chunk_digits}"),
            content=ft.Column([
                txt_p,
                suggest_pao_word(digits_p, "P", txt_p),
                txt_a,
                suggest_pao_word(digits_a, "A", txt_a),
                txt_o,
                suggest_pao_word(digits_o, "O", txt_o),
            ], height=380, tight=True),
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

    def toggle_mode(e):
        state["show_text"] = e.control.value
        render_list(run_update=True)

    def render_list(run_update):
        new_controls =[]

        for i, chunk in enumerate(chunks):
            key = str(i)
            chunk_data = groups_data.get(key, {})
            is_described = key in groups_data

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
                    ft.Text(words_display, size=20, color=ft.colors.BLUE_800, text_align=ft.TextAlign.CENTER)
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
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
