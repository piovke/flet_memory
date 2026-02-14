import flet as ft
from .functions import *

def PaoPageView(page):
    pao_data = load_pao()
    return ft.View(
        route = "/pao"
    )