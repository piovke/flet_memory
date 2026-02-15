import flet as ft
from views.home import HomeView
from views.pi_page import PiPageView
from views.pao import PaoPageView


def main(page: ft.Page):
    page.title = "Memory Master"
    page.window.width = 350
    page.window.height = 730
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    # obsługa wstecz na telefonie
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_view_pop = view_pop

    def route_change(e):
        route = e.route if hasattr(e, "route") else e
        page.views.clear()

        if route == "/pi":
            page.views.append(PiPageView(page))
        elif route == "/pao":
            page.views.append(PaoPageView(page))
        else:
            page.views.append(HomeView(page))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Ręczne uruchomienie startu (naprawa pustego okna)
    route_change(page.route)


if __name__ == "__main__":
    ft.run(main)