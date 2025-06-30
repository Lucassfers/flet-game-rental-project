import flet as ft
import requests
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

API_JOGOS_URL = "http://localhost:3000/jogos" 
API_DESENVOLVEDORAS_URL = "http://localhost:3000/desenvolvedoras"

def graf_caros(page):

    def obter_desenvolvedoras():
        try:
            response = requests.get(API_DESENVOLVEDORAS_URL)
            response.raise_for_status()
            return {str(dev["id"]): dev["nome"] for dev in response.json()}
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar desenvolvedoras: {err}"))
            page.snack_bar.open = True
            page.update()
            return {}

    def obter_jogos():
        try:
            response = requests.get(API_JOGOS_URL)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar jogos: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    desenvolvedoras_map = obter_desenvolvedoras()
    jogos = obter_jogos()

    if not jogos:
        return ft.Text("Não há jogos cadastrados.")

    for jogo in jogos:
        dev_id = str(jogo.get("desenvolvedoraId"))
        jogo["desenvolvedora_nome"] = desenvolvedoras_map.get(dev_id, "Desconhecida")
    
    jogos_ordenados = sorted(jogos, key=lambda j: j['preco'], reverse=True)[:10]

    cores = [
        ft.Colors.BLUE,
        ft.Colors.GREEN,
        ft.Colors.ORANGE,
        ft.Colors.PINK,
        ft.Colors.PURPLE,
        ft.Colors.CYAN,
        ft.Colors.RED,
        ft.Colors.YELLOW,
        ft.Colors.AMBER,
        ft.Colors.BROWN
    ]

    largura_max = 1000
    maior_preco = jogos_ordenados[0]['preco'] if jogos_ordenados else 1

    linhas = []
    for i, jogo in enumerate(jogos_ordenados):
        largura_barra = (jogo['preco'] / maior_preco) * largura_max
        preco_formatado = locale.currency(jogo["preco"], grouping=True)

        linhas.append(
            ft.Row(
                [
                    ft.Text(f"{jogo['nome']} ({jogo['desenvolvedora_nome']})", width=160), 
                    ft.Container(
                        width=largura_barra,
                        height=30,
                        bgcolor=cores[i % len(cores)],
                        border_radius=5,
                    ),
                    ft.Text(preco_formatado, width=80, text_align=ft.TextAlign.RIGHT)
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )
        )

    return ft.Column(
        [
            ft.Text("Jogos de maior preço: Top 10", size=22, weight="bold"),
            *linhas
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )