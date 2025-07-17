import flet as ft
from backend.auth import authenticate_user

def login_view(page: ft.Page):
    error_text = ft.Text("", color=ft.Colors.RED_400, size=12)

    def do_login(_):
        user = authenticate_user(user_id.value, password.value)
        if user:
            page.session.set("user", user)
            page.go("/dashboard")
        else:
            error_text.value = "Invalid ID or password."
            page.snack_bar = ft.SnackBar(ft.Text("Invalid ID or password."))
            page.snack_bar.open = True
            page.update()

    def go_signup(_):
        page.go("/signup")

    page.bgcolor = ft.Colors.BLUE_GREY_900

    page.views.clear()
    page.views.append(
        ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Eplanet Quiz", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text("Login to your account", size=18, color=ft.Colors.GREY_300),
                            user_id := ft.TextField(
                                label="Your 5‑digit ID",
                                label_style=ft.TextStyle(color=ft.Colors.GREY_300),
                                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                                border_color=ft.Colors.GREY_500,
                                focused_border_color=ft.Colors.BLUE_300,
                                autofocus=True,
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
                            error_text,
                            ft.ElevatedButton("Login", on_click=do_login, width=200),
                            ft.TextButton("Don't have an account?  Sign up", on_click=go_signup),
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
