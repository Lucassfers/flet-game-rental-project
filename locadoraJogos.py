import flet as ft
from telas.jogos import cad_jogos
from telas.desenvolvedora import graf_desenvolvedora
from telas.caros import graf_caros
from telas.buscar_jogos import buscar_jogos

def main(page: ft.Page):
    page.title = "Locadora de Jogos Avenida"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    snack = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack
    page.overlay.append(snack)

    conteudo_dinamico = ft.Column()

    def navigate(e):
        rota = e.control.data
        if rota == "cad_jogos":
            conteudo_dinamico.controls = [cad_jogos(page)]
        if rota == "graf_desenvolvedora":
            conteudo_dinamico.controls = [graf_desenvolvedora(page)]
        if rota == "graf_caros":
            conteudo_dinamico.controls = [graf_caros(page)]
        if rota == "buscar_jogos":
            conteudo_dinamico.controls = [buscar_jogos(page)]
        page.update()
            

    nav_buttons = ft.Row([
        ft.ElevatedButton("Jogos", data="cad_jogos", on_click=navigate),
        ft.ElevatedButton("Desenvolvedoras com mais jogos", data="graf_desenvolvedora", on_click=navigate),
        ft.ElevatedButton("Jogos mais caros", data="graf_caros", on_click=navigate),
        ft.ElevatedButton("Buscar jogos por Nome/Marca", data="buscar_jogos" ,on_click=navigate)

    ], alignment=ft.MainAxisAlignment.CENTER)

    conteudo_dinamico.controls = [cad_jogos(page)]

    page.add(
        ft.Column([
            ft.Text("Locadora de Jogos - Controle de locação", size=30, weight="bold", text_align="center"),
            nav_buttons,
            ft.Divider(),
            conteudo_dinamico
        ], scroll=ft.ScrollMode.AUTO)
    )

ft.app(target=main)