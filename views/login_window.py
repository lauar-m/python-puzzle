import flet as ft
from utils.components import create_button, create_card, PRIMARY_COLOR
from data.services import AuthService


def LoginWindow(content: ft.Column, on_success):
    # Elementos da UI
    username = ft.TextField(
        label="Nome de usuário",
        width=300,
        autofocus=True
    )
    password = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=300
    )

    # Mensagens de erro
    warning = ft.Text("Preencha todos os campos", color="red", size=12, visible=False)
    warning_wrong_password = ft.Text("Senha incorreta", color="red", size=12, visible=False)
    warning_unexpected_error = ft.Text("Erro inesperado. Tente novamente.", color="red", size=12, visible=False)
    warning_weak_username = ft.Text("Nome de usuário deve ter no mínimo 3 caracteres", color="red", size=12, visible=False)
    warning_weak_password = ft.Text("Senha deve ter no mínimo 8 caracteres", color="red", size=12, visible=False)

    # Função de login
    def fazer_login(e):
        # Resetar mensagens de erro
        warning_wrong_password.visible = False
        warning.visible = False
        warning_unexpected_error.visible = False
        warning_weak_username.visible = False
        warning_weak_password.visible = False

        if not username.value or not password.value:
            warning.visible = True
            login_context.update()
            return

        # Tenta autenticar
        user, error = AuthService.authenticate_user(
            username=username.value.strip(),
            password=password.value
        )

        if error:
            if "invalid credentials" in error.lower():
                warning_wrong_password.visible = True
            elif "username must be at least 3 characters long" in error.lower():
                warning_weak_username.visible = True
            elif "password must be at least 8 characters long" in error.lower():
                warning_weak_password.visible = True
            else:
                warning_unexpected_error.visible = True
            login_context.update()
        else:
            on_success(user)

    # Criar formulário
    form_login = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            username,
            password,
            warning,
            warning_wrong_password,
            warning_unexpected_error,
            warning_weak_username,
            warning_weak_password,
            create_button(
                "Entrar",
                ft.Icons.LOGIN,
                action=fazer_login,
                largura=200,
                color=PRIMARY_COLOR,
            ),
        ],
    )

    # Criar card e layout principal
    card = create_card("🔐 Login", form_login)

    login_context = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[card],
    )

    # Adicionar à página e retornar o conteúdo
    content.controls.append(login_context)
