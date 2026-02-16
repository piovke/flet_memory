import flet as ft

def HomeView(page):
    return ft.View(
        route="/",
        controls=[
            ft.AppBar(title=ft.Text("Pamietaj"), bgcolor="blue"),
            ft.Container(
                content=ft.Column([
                    ft.Text("", size=30),
                    ft.FilledButton("PiPamietaj", on_click=lambda _: page.go("/pi"), width=400),
                    ft.FilledButton("PAO", on_click=lambda _: page.go("/pao"), width=400),
                    ft.FilledButton("Dates", on_click=lambda _: page.go("/dates"), width=400),
                    ft.FilledButton("export/import", on_click=lambda _: page.go("/eximport"), width=400),
                ]),
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        ]
    )