import flet as ft

def cad_jogos():
    campo1 = ft.TextField(label="Nome do Produto", expand=4)
    campo2 = ft.TextField(label="Quant.", expand=1)
    campo3 = ft.TextField(label="Preço R$", expand=2)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome do Produto")),
            ft.DataColumn(ft.Text("Quant.")),
            ft.DataColumn(ft.Text("Preço R$")),
        ],
        rows=[],
    )

    def enviar_click(e):
        valores = [campo1.value, campo2.value, campo3.value]
        if any(v.strip() == "" for v in valores):
            e.page.snack_bar.content = ft.Text("Preencha todos os campos")
            e.page.snack_bar.open = True
            e.page.update()            
            return
        tabela.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(v)) for v in valores]))
        campo1.value = campo2.value = campo3.value = ""
        e.page.update()

    def limpar_click(e):
        campo1.value = campo2.value = campo3.value = ""
        e.page.update()

    return ft.Column([
        ft.Text("Cadastro de Produtos", size=24, weight="bold"),

        # Campos em 3 por linha
        ft.Row([campo1, campo2, campo3], spacing=10),

        ft.Row([
            ft.ElevatedButton("Enviar", on_click=enviar_click),
            ft.ElevatedButton("Limpar", on_click=limpar_click),
        ]),
        ft.Divider(),
        ft.Text("Lista dos Produtos Cadastrados:"),
        tabela
    ], spacing=10)
