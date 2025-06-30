import flet as ft
import requests
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

API_JOGOS_URL = "http://localhost:3000/jogos"
API_DESENVOLVEDORAS_URL = "http://localhost:3000/desenvolvedoras"

def buscar_jogos(page: ft.Page):
    campo_busca = ft.TextField(
        hint_text="Pesquisar por nome, desenvolvedora ou gênero...",
        width=400,
        autofocus=True
    )

    resultado = ft.Column(scroll=ft.ScrollMode.AUTO)
    mensagem_inicial = ft.Text("Digite algo para buscar jogos", size=18, italic=True)
    resultado.controls.append(mensagem_inicial)
    
    def carregar_desenvolvedoras():
        try:
            response = requests.get(API_DESENVOLVEDORAS_URL)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar desenvolvedoras: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    def carregar_jogos():
        try:
            response = requests.get(API_JOGOS_URL)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar jogos: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    def filtrar_jogos(e):
        texto_busca = campo_busca.value.strip().lower()
        resultado.controls.clear()

        if not texto_busca:
            resultado.controls.append(ft.Text("Digite algo para buscar jogos", size=18, italic=True))
            page.update()
            return

        try:
            jogos = carregar_jogos()
            desenvolvedoras = carregar_desenvolvedoras()
            
            dev_map = {str(dev["id"]): dev["nome"] for dev in desenvolvedoras}
            
            jogos_com_info = []
            for jogo in jogos:
                jogo_completo = jogo.copy()
                jogo_completo["desenvolvedora"] = dev_map.get(str(jogo.get("desenvolvedoraId")), "Desconhecida")
                jogos_com_info.append(jogo_completo)
            
            jogos_filtrados = [
                j for j in jogos_com_info
                if (texto_busca in j["nome"].lower() or 
                    texto_busca in j["desenvolvedora"].lower() or
                    texto_busca in j["genero"].lower())
            ]

            if not jogos_filtrados:
                resultado.controls.append(
                    ft.Text(f"Nenhum jogo encontrado para: '{texto_busca}'", size=18)
                )
            else:
                tabela = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Nome")),
                        ft.DataColumn(ft.Text("Desenvolvedora")),
                        ft.DataColumn(ft.Text("Gênero")),
                        ft.DataColumn(ft.Text("Quant.")),
                        ft.DataColumn(ft.Text("Preço")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(jogo["id"])),
                                ft.DataCell(ft.Text(jogo["nome"])),
                                ft.DataCell(ft.Text(jogo["desenvolvedora"])),
                                ft.DataCell(ft.Text(jogo["genero"])),
                                ft.DataCell(ft.Text(str(jogo["quant"]))),
                                ft.DataCell(ft.Text(locale.currency(jogo["preco"], grouping=True))),
                            ]
                        ) for jogo in jogos_filtrados
                    ],
                    width=800
                )
                resultado.controls.append(tabela)

        except Exception as err:
            resultado.controls.append(
                ft.Text(f"Erro ao buscar jogos: {err}", color="red")
            )

        page.update()

    campo_busca.on_change = filtrar_jogos

    return ft.Column(
        [
            ft.Text("Busca de Jogos", size=24, weight="bold"),
            ft.Row(
                [
                    campo_busca,
                    ft.IconButton(
                        icon=ft.Icons.SEARCH,
                        on_click=filtrar_jogos,
                        tooltip="Buscar"
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(),
            resultado
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )