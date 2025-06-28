import flet as ft
import requests
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

API_URL = "http://localhost:3000/jogos"

def cad_jogos(page: ft.Page):
    campo1 = ft.TextField(label="Nome do Jogo", expand=4)
    campo2 = ft.TextField(label="Desenvolvedora", expand=3)
    campo3 = ft.TextField(label="Gênero", expand=3)
    campo4 = ft.TextField(label="Quant.", expand=1)
    campo5 = ft.TextField(label="Preço R$", expand=2)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome do Jogo")),
            ft.DataColumn(ft.Text("Desenvolvedora")),
            ft.DataColumn(ft.Text("Gênero")),
            ft.DataColumn(ft.Text("Quant.")),
            ft.DataColumn(ft.Text("Preço R$")),
        ],
        rows=[],
    )

    def carregar_jogos_api():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()

            jogos = response.json()
            tabela.rows.clear()

            for jogo in reversed(jogos):
                preco_f = locale.currency(jogo["preco"], grouping=True)
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(jogo["id"])),
                    ft.DataCell(ft.Text(jogo["nome"])),
                    ft.DataCell(ft.Text(jogo["desenvolvedora"])),
                    ft.DataCell(ft.Text(jogo["genero"])),
                    ft.DataCell(ft.Text(str(jogo["quant"]))),
                    ft.DataCell(ft.Text(preco_f)),
                ]))
            page.update()
        except Exception as err:
            page.snack_bar.content = ft.Text(f"Erro ao carregar jogos: {err}")
            page.snack_bar.open = True
            page.update()

    def enviar_click(e):
        valores = [campo1.value, campo2.value, campo3.value, campo4.value, campo5.value]
        if any(v.strip() == "" for v in valores):
            page.snack_bar.content = ft.Text("Preencha todos os campos")
            page.snack_bar.open = True
            page.update()
            return
        try:
            novo_jogo = {
                "nome": campo1.value,
                "desenvolvedora": campo2.value,
                "genero": campo3.value,
                "quant": int(campo4.value),
                "preco": float(campo5.value.replace(",", ".")),
            }

            response = requests.post(API_URL, json=novo_jogo)
            response.raise_for_status()

            page.snack_bar.content = ft.Text("Jogo cadastrado com sucesso!")
            page.snack_bar.open = True

            campo1.value = campo2.value = campo3.value = campo4.value = campo5.value = ""
            carregar_jogos_api()

        except ValueError:
            page.snack_bar.content = ft.Text("Quantidade deve ser número inteiro e preço válido.")
            page.snack_bar.open = True
        except requests.exceptions.RequestException as err:
            page.snack_bar.content = ft.Text(f"Erro ao enviar: {err}")
            page.snack_bar.open = True
        page.update()

    def limpar_click(e):
        campo1.value = campo2.value = campo3.value = campo4.value = campo5.value = ""
        page.update()

    carregar_jogos_api()

    return ft.Column([
        ft.Text("Cadastro de jogos", size=24, weight="bold"),
        ft.Row([campo1, campo2], spacing=10),
        ft.Row([campo3, campo4, campo5], spacing=10),
        ft.Row([
            ft.ElevatedButton("Enviar", on_click=enviar_click),
            ft.ElevatedButton("Limpar", on_click=limpar_click),
        ]),
        ft.Divider(),
        ft.Text("Lista de jogos cadastrados:", size=20, weight="bold"),
        ft.Container(
            content=ft.Column(
                [tabela],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            height=400,
            padding=5,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            bgcolor=ft.Colors.GREY_100
        )
    ], spacing=10)
