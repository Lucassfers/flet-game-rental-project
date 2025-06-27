import flet as ft

def cad_emprestimos():
    entradas = [ft.TextField(label=f"Campo {i+1}") for i in range(4)]
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Campo 1")),
            ft.DataColumn(ft.Text("Campo 2")),
            ft.DataColumn(ft.Text("Campo 3")),
            ft.DataColumn(ft.Text("Campo 4")),
        ],
        rows=[],
    )

    def enviar_click(e):
        valores = [campo.value for campo in entradas]
        if any(v.strip() == "" for v in valores):
            e.page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos"))
            e.page.snack_bar.open = True
            e.page.update()
            return
        tabela.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(v)) for v in valores]))
        for campo in entradas:
            campo.value = ""
        e.page.update()

    def limpar_click(e):
        for campo in entradas:
            campo.value = ""
        e.page.update()

    return ft.Column([
        ft.Text("Cadastro de Vendas", size=24, weight="bold"),
        *entradas,
        ft.Row([
            ft.ElevatedButton("Enviar", on_click=enviar_click),
            ft.ElevatedButton("Limpar", on_click=limpar_click),
        ]),
        ft.Divider(),
        ft.Text("Itens Cadastrados:"),
        tabela
    ], spacing=10)
