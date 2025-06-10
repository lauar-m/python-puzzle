import flet as ft
from utils.components import create_button, create_card, PRIMARY_COLOR


def LoginWindow(content: ft.Column, on_success):
    nome_usuario = ft.TextField(label="Nome de usuário", width=300)
    senha = ft.TextField(
        label="Senha", password=True, can_reveal_password=True, width=300
    )

    warning = ft.Text("Preencha todos os campos.", color="red", size=12, visible=False)

    def fazer_login(e):
        if nome_usuario.value.strip() and senha.value.strip():
            warning.visible = False
            on_success(nome_usuario.value.strip())
        else:
            warning.visible = True
            content.update()

    form_login = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            nome_usuario,
            senha,
            warning,
            create_button(
                "Entrar",
                ft.Icons.LOGIN,
                action=fazer_login,
                largura=200,
                color=PRIMARY_COLOR,
            ),
        ],
    )

    card = create_card("🔐 Login", form_login)

    content.controls.append(
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[card],
        )
    )
