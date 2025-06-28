import flet as ft
import requests
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

API_URL = "http://localhost:3000/jogos"

def buscar_jogos(page):
    snack = ft.SnackBar(ft.Text(""), open=False)

    campo_busca = ft.TextField(
        hint_text="Pesquisar por nome ou desenvolvedora...",
        width=400
    )

    resultado = ft.Column(scroll=ft.ScrollMode.AUTO)

    def obter_jogos_api():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            page.snack_bar = ft.Text(f"Erro ao buscar jogos: {err}")
            page.snack_bar.open = True
            page.update()
            return []

    def filtrar_jogos(e):
        texto = campo_busca.value.strip().lower()
        jogos = obter_jogos_api()

        resultado.controls.clear()

        if not jogos:
            resultado.controls.append(ft.Text("Erro ao carregar os jogos."))
        else:
            filtrados = [
                j for j in jogos
                if texto in j["nome"].lower() or texto in j["desenvolvedora"].lower()
            ]

            if not filtrados:
                resultado.controls.append(
                    ft.Text(f"Nenhum jogo encontrado para: '{texto}'", size=18)
                )
            else:
                tabela = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Nome do Jogo")),
                        ft.DataColumn(ft.Text("Desenvolvedora")),
                        ft.DataColumn(ft.Text("Gênero")),
                        ft.DataColumn(ft.Text("Quant.")),
                        ft.DataColumn(ft.Text("Preço R$")),
                    ],
                    rows=[]
                )

                for j in filtrados:
                    preco_f = locale.currency(j["preco"], grouping=True)
                    tabela.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(j["id"])),
                        ft.DataCell(ft.Text(j["nome"])),
                        ft.DataCell(ft.Text(j["desenvolvedora"])),
                        ft.DataCell(ft.Text(j["genero"])),
                        ft.DataCell(ft.Text(str(j["quant"]))),
                        ft.DataCell(ft.Text(preco_f)),
                    ]))

                resultado.controls.append(tabela)

        campo_busca.update()
        resultado.update()

    campo_busca.on_change = filtrar_jogos

    return ft.Column(
        [
            ft.Text("Buscar Jogos por Nome ou Desenvolvedora", size=22, weight="bold"),
            campo_busca,
            ft.Divider(),
            resultado
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
