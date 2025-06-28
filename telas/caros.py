import flet as ft
import requests
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

API_URL = "http://localhost:3000/jogos" 

def graf_caros(page):

    def obter_jogos_api():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()

        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar jogos: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    jogos = obter_jogos_api()

    if not jogos:
        return ft.Text("Não há jogos cadastrados.")
    
    jogos2 = sorted(jogos, key=lambda j: j['preco'], reverse=True)

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

    linhas = []

    maior_preco = jogos2[0]['preco']

    for i, jogo in enumerate(jogos2):
        
        if i == 10:
            break
        
        largura_barra = (jogo['preco'] / maior_preco) * largura_max
        cor = cores[i % len(cores)]

        barra = ft.Container(
            width=largura_barra,
            height=30,
            bgcolor=cor,
            border_radius=5,
        )

        preco_f = locale.currency(jogo["preco"], grouping=True)

        linha = ft.Row(
            [
                ft.Text(f"{jogo['nome']} ({jogo['desenvolvedora']})", width=160),
                barra,
                ft.Text(preco_f, width=80, text_align=ft.TextAlign.RIGHT)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        linhas.append(linha)

    return ft.Column(
        [ft.Text("Jogos de maior preço: Top 10", size=22, weight="bold")] + linhas,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
