import flet as ft

def main(page: ft.Page):
    page.title = 'CAPTURANDO DADOS'
    page.horizontal_alighment = ft.CrossAxisAlignment.CENTER
    page.vertical_aligment = ft.MainAxisAlignment.SPACE_EVENLY
    page.padding = 50

    def clique_botao(e):
        txt_saudação.value = f'Ola, {tf_nome.value}!'
        page.update()
        tf_nome.focus()

    tf_nome = ft.TextField(label = 'digite seu nome: ', on_submit=clique_botao)
    btn_ok = ft.ElevatedButton('MOSTRAR', on_click=clique_botao)
    txt_saudação = ft.Text('Ola,...!')


    page.add(
        tf_nome,
        btn_ok,
        txt_saudação,
    )

    tf_nome.focus()
    
ft.app(main)