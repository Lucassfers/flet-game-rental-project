import flet as ft

def cadastro(page):
    return ft.View(
        "/cadastro",
        controls=[
            ft.Text("Página de Cadastro"),
            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
        ]
    )