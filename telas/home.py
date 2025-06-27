import flet as ft

def home(page):
    return ft.View(
        "/",
        controls=[
            ft.Text("Página Inicial"),
            ft.ElevatedButton("Ir para Cad", on_click=lambda _: page.go("/cadastro")),
        ]
    )