import flet as ft
import requests
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

API_JOGOS_URL = "http://localhost:3000/jogos"
API_DESENVOLVEDORAS_URL = "http://localhost:3000/desenvolvedoras"

def cad_jogos(page: ft.Page):
    campo_nome = ft.TextField(label="Nome do Jogo", expand=5)
    dropdown_desenvolvedora = ft.Dropdown(label="Desenvolvedora", options=[],expand=4)
    campo_genero = ft.TextField(label="Gênero",expand=3)
    campo_quant = ft.TextField(label="Quantidade",expand=1)
    campo_preco = ft.TextField(label="Preço (R$)",expand=2)
    campo_nova_desenvolvedora = ft.TextField(label="Nova Desenvolvedora", width=200)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Desenvolvedora")),
            ft.DataColumn(ft.Text("Gênero")),
            ft.DataColumn(ft.Text("Quant.")),
            ft.DataColumn(ft.Text("Preço")),
        ],
        rows=[],
    )
    def toggle_nova_desenvolvedora(e):
        campo_nova_desenvolvedora.visible = not campo_nova_desenvolvedora.visible
        page.update()

    def cadastrar_desenvolvedora(nome):
        try:
            response = requests.post(
                API_DESENVOLVEDORAS_URL,
                json={"nome": nome}
            )
            response.raise_for_status()
            return response.json()
        except Exception as err:
            page.snack_bar.content = ft.Text(f"Erro ao cadastrar desenvolvedora: {err}")
            page.snack_bar.open = True
            page.update()
            return None

    def carregar_desenvolvedoras():
        try:
            response = requests.get(API_DESENVOLVEDORAS_URL)
            response.raise_for_status()
            desenvolvedoras_data = response.json()
            options = []
            for dev in desenvolvedoras_data:
                options.append(ft.dropdown.Option(key=str(dev["id"]), text=dev["nome"]))
            dropdown_desenvolvedora.options = options
            page.update()
        except Exception as err:
            page.snack_bar.content = ft.Text(f"Erro ao carregar desenvolvedoras: {err}")
            page.snack_bar.open = True
            page.update()

    def carregar_jogos_tabela():
        tabela.rows.clear()
        try:
            response_jogos = requests.get(API_JOGOS_URL)
            response_jogos.raise_for_status()
            jogos = response_jogos.json()
            response_desenvolvedoras = requests.get(API_DESENVOLVEDORAS_URL)
            response_desenvolvedoras.raise_for_status()
            desenvolvedoras_map = {str(dev["id"]): dev["nome"] for dev in response_desenvolvedoras.json()}
            for jogo in jogos:
                nome_desenvolvedora = desenvolvedoras_map.get(str(jogo.get("desenvolvedoraId")), "Desconhecida")
                preco_f = locale.currency(jogo["preco"], grouping=True)
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(jogo["id"])),
                    ft.DataCell(ft.Text(jogo["nome"])),
                    ft.DataCell(ft.Text(nome_desenvolvedora)),
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
        if campo_nova_desenvolvedora.visible and campo_nova_desenvolvedora.value:
            nova_dev = cadastrar_desenvolvedora(campo_nova_desenvolvedora.value)
            if nova_dev:
                dropdown_desenvolvedora.options.append(
                    ft.dropdown.Option(
                        key=str(nova_dev["id"]),
                        text=nova_dev["nome"]
                    )
                )
                dropdown_desenvolvedora.value = str(nova_dev["id"])
                campo_nova_desenvolvedora.value = ""
                toggle_nova_desenvolvedora(e)
                page.snack_bar.content = ft.Text("Desenvolvedora cadastrada com sucesso!")
                page.snack_bar.open = True
        nome = campo_nome.value
        genero = campo_genero.value
        quant_str = campo_quant.value
        preco_str = campo_preco.value
        desenvolvedora_id = dropdown_desenvolvedora.value
        if not nome or not genero or not quant_str or not preco_str or not desenvolvedora_id:
            page.snack_bar.content = ft.Text("Preencha todos os campos")
            page.snack_bar.open = True
            page.update()
            return
        try:
            quant = int(quant_str)
            preco = float(preco_str.replace(",", "."))
        except ValueError:
            page.snack_bar.content = ft.Text("Quantidade deve ser número inteiro e preço válido.")
            page.snack_bar.open = True
            page.update()
            return
        novo_jogo = {
            "nome": nome,
            "desenvolvedoraId": desenvolvedora_id,
            "genero": genero,
            "quant": quant,
            "preco": preco,
        }

        try:
            response = requests.post(API_JOGOS_URL, json=novo_jogo)
            response.raise_for_status()
            page.snack_bar.content = ft.Text("Jogo cadastrado com sucesso!")
            page.snack_bar.open = True
            campo_nome.value = ""
            campo_genero.value = ""
            campo_quant.value = ""
            campo_preco.value = ""
            dropdown_desenvolvedora.value = ""
            carregar_jogos_tabela()

        except requests.exceptions.RequestException as err:
            page.snack_bar.content = ft.Text(f"Erro ao enviar: {err}")
            page.snack_bar.open = True
        page.update()

    def limpar_click(e):
        campo_nome.value = ""
        dropdown_desenvolvedora.value = ""
        campo_genero.value = ""
        campo_quant.value = ""
        campo_preco.value = ""
        page.update()

    carregar_desenvolvedoras()
    carregar_jogos_tabela()

    linha_nome_desenvolvedora = ft.Row(
    [
        ft.Container(campo_nome, expand=5),
        ft.Container(dropdown_desenvolvedora, expand=4),
        ft.Container(campo_nova_desenvolvedora, expand=4),
    ],
    spacing=10,
    alignment=ft.MainAxisAlignment.START
)

    return ft.Column([
        ft.Text("Cadastro de jogos", size=24, weight="bold"),
        linha_nome_desenvolvedora,
        ft.Row([campo_genero, campo_quant, campo_preco], spacing=10),
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
            ),
            height=400,
            padding=5,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            bgcolor=ft.Colors.GREY_100
        )
    ], spacing=10)
