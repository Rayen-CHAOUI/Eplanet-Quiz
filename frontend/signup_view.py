import flet as ft
from backend.auth import register_user

def signup_view(page: ft.Page):
    error_text = ft.Text("", color=ft.Colors.RED_400, size=12)

    def do_signup(_):
        success, msg, _ = register_user(full_name.value, password.value, level.value)

        error_text.value = "" if success else f"{msg}"
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

        if success:
            page.go("/")

    def go_login(_):
        page.go("/")

    page.bgcolor = ft.Colors.BLUE_GREY_900

    page.views.clear()
    page.views.append(
        ft.View(
            route="/signup",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Eplanet Quiz", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text("Create your account", size=18, color=ft.Colors.GREY_300),
                            full_name := ft.TextField(
                                label="Full Name",
                                label_style=ft.TextStyle(color=ft.Colors.GREY_300),
                                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                                border_color=ft.Colors.GREY_500,
                                focused_border_color=ft.Colors.BLUE_300,
                                bgcolor=ft.Colors.BLUE_GREY_800
                            ),
                            password := ft.TextField(
                                label="Password",
                                label_style=ft.TextStyle(color=ft.Colors.GREY_300),
                                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                                border_color=ft.Colors.GREY_500,
                                focused_border_color=ft.Colors.BLUE_300,
                                password=True,
                                can_reveal_password=True,
                                bgcolor=ft.Colors.BLUE_GREY_800
                            ),
                            level := ft.Dropdown(
                                label="Level",
                                label_style=ft.TextStyle(color=ft.Colors.GREY_300),
                                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                                options=[
                                    ft.dropdown.Option("Beginner"),
                                    ft.dropdown.Option("Pre-intermediate"),
                                    ft.dropdown.Option("Intermediate"),
                                    ft.dropdown.Option("Upper-intermediate"),
                                    ft.dropdown.Option("Advanced"),
                                ],
                                border_color=ft.Colors.GREY_500,
                                focused_border_color=ft.Colors.BLUE_300,
                                bgcolor=ft.Colors.BLUE_GREY_800
                            ),
                            error_text,
                            ft.ElevatedButton("Register", on_click=do_signup, width=200),
                            ft.TextButton("Already have an account?  Login", on_click=go_login),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=400,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=20
                )
            ]
        )
    )
    page.update()
