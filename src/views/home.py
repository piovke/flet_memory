import flet as ft

def HomeView(page):
    return ft.View(
        route="/",
        controls=[
            ft.AppBar(title=ft.Text("Strona Główna"), bgcolor="blue"),
            ft.Container(
                content=ft.Column([
                    ft.Text("pamietaj", size=30),
                    ft.FilledButton("PiPamietaj", on_click=lambda _: page.go("/pi")),
                    ft.FilledButton("Birthdays", on_click=lambda _: page.go("/birthdays")),
                    ft.FilledButton("export/import", on_click=lambda _: page.go("/eximport")),
                ]),
                alignment=ft.Alignment(0, 0),
                expand=True
            )
        ]
    )