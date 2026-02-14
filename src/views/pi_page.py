import flet as ft
import json
from pathlib import Path

cyfry = "141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420"
CURRENT_DIR = Path(__file__).parent
ROOT_DIR = CURRENT_DIR.parent.parent
STORAGE_DIR = ROOT_DIR / "storage"

# Definiujemy pełne ścieżki do plików
GROUPS_FILE = STORAGE_DIR / "groups.json"
PAO_FILE = STORAGE_DIR / "pao.json"

def load_groups():
    if not GROUPS_FILE.exists():
        return {}
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Błąd ładowania groups.json: {e}")
        return {}

def load_pao():
    if not PAO_FILE.exists():
        return {}
    try:
        with open(PAO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Błąd ładowania pao.json: {e}")
        return {}

def save_groups(data):
    try:
        with open(GROUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd zapisu JSON: {e}")

def save_pao(data):
    try:
        with open(PAO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd zapisu JSON: {e}")


def PiPageView(page):

    groups_data = load_groups()
    pao_data = load_pao()
    buttons_list = []
    chunks = [cyfry[i:i + 6] for i in range(0, len(cyfry), 6)]

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
            data = load_pao()

            if digit_pair not in data:
                data[digit_pair] = {"P": [], "A": [], "O": []}

            if text not in data[digit_pair][pao] and text != "":
                data[digit_pair][pao].append(text)
                save_pao(data)

        def save_click(e):
            groups_data[key] = {
                "digits": chunk_digits,
                "P": txt_p.value,
                "A": txt_a.value,
                "O": txt_o.value
            }
            save_groups(groups_data)

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

    ### generating buttons###
    for i, chunk in enumerate(chunks):
        is_described = str(i) in groups_data
        btn = ft.OutlinedButton(
            content=ft.Text(chunk),
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda e, idx=i, ch=chunk: open_edit_dialog(index=idx, chunk_digits=ch)
        )
        buttons_list.append(btn)

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
