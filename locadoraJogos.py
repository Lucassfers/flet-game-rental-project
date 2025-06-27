import flet as ft
from cadastros.clientes import cad_clientes
from cadastros.emprestimos import cad_emprestimos
from cadastros.jogos import cad_jogos
from cadastros.locacao import cad_locacao

def main(page: ft.Page):
    page.title = "Cantina Escolar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    snack = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack
    page.overlay.append(snack)

    conteudo_dinamico = ft.Column()

    def navigate(e):
        rota = e.control.data
        if rota == "cad_jogos":
            conteudo_dinamico.controls = [cad_jogos()]
        elif rota == "cad_clientes":
            conteudo_dinamico.controls = [cad_clientes()]
        elif rota == "cad_emprestimos":
            conteudo_dinamico.controls = [cad_emprestimos()]
        elif rota == "cad_locacao":
            conteudo_dinamico.controls = [cad_locacao()]
        page.update()

    nav_buttons = ft.Row([
        ft.ElevatedButton("Jogos", data="cad_jogos", on_click=navigate),
        ft.ElevatedButton("Clientes", data="cad_clientes", on_click=navigate),
        ft.ElevatedButton("Emprestimos", data="cad_emprestimos", on_click=navigate),
        ft.ElevatedButton("Locações", data="cad_locacao", on_click=navigate),
    ], alignment=ft.MainAxisAlignment.CENTER)

    conteudo_dinamico.controls = [cad_jogos()]

    page.add(
        ft.Column([
            ft.Text("Locadora de Jogos - Controle de locação", size=30, weight="bold", text_align="center"),
            nav_buttons,
            ft.Divider(),
            conteudo_dinamico
        ], scroll=ft.ScrollMode.AUTO)
    )

ft.app(target=main)
