import flet as ft
import requests

API_JOGOS_URL = "http://localhost:3000/jogos" 
API_DESENVOLVEDORAS_URL = "http://localhost:3000/desenvolvedoras"

def graf_desenvolvedora(page):

    def obter_dados_api():
        try:
            response_jogos = requests.get(API_JOGOS_URL)
            response_jogos.raise_for_status()
            jogos_data = response_jogos.json()

            response_desenvolvedoras = requests.get(API_DESENVOLVEDORAS_URL)
            response_desenvolvedoras.raise_for_status()
            desenvolvedoras_map = {str(dev["id"]): dev["nome"] for dev in response_desenvolvedoras.json()}

            for jogo in jogos_data:
                jogo["desenvolvedora_nome"] = desenvolvedoras_map.get(str(jogo.get("desenvolvedoraId")), "Desconhecida")
            
            return jogos_data
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar dados: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    jogos = obter_dados_api()
    
    dicionario = {}

    for j in jogos:
        desenvolvedora_nome = j['desenvolvedora_nome']
        dicionario[desenvolvedora_nome] = dicionario.get(desenvolvedora_nome, 0) + 1

    if not dicionario:
        return ft.Text("Nenhum dado disponível.")

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

    dicionario2 = dict(sorted(dicionario.items(), 
                        key=lambda item: item[1], reverse=True))

    total_jogos = sum(dicionario2.values())
    
    lista_valores = list(dicionario2.values())
    
    outras = 0
    if len(lista_valores) > 10:
        outras = sum(lista_valores[10:])    
    maior_qtd = 0
    if lista_valores:
        maior_qtd = max(lista_valores[0], outras if len(lista_valores) > 10 else 0)


    for i, (marca, qtd) in enumerate(dicionario2.items()):
        
        if i == 10:
            break
        
        largura_barra = (qtd / maior_qtd) * largura_max
        percentual = (qtd / total_jogos) * 100
        cor = cores[i % len(cores)]

        barra = ft.Container(
            width=largura_barra,
            height=30,
            bgcolor=cor,
            border_radius=5,
        )

        linha = ft.Row(
            [
                ft.Text(marca, width=100),
                barra,
                ft.Text(f"{qtd} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        linhas.append(linha)

    if outras > 0: 
        largura_barra = (outras / maior_qtd) * largura_max
        percentual = (outras / total_jogos) * 100
        cor = ft.Colors.GREY

        barra = ft.Container(
            width=largura_barra,
            height=30,
            bgcolor=cor,
            border_radius=5,
        )

        linha = ft.Row(
            [
                ft.Text("Outras desenvolvedoras", width=100),
                barra,
                ft.Text(f"{outras} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        linhas.append(linha)

    return ft.Column(
        [ft.Text("Jogos por Desenvolvedora", size=22, weight="bold")] + linhas, 
        scroll=ft.ScrollMode.AUTO
    )
