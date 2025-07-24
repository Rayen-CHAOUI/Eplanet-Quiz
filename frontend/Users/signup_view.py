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
        page.go("/login")

    # Light theme setup
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT

    page.views.clear()
    page.views.append(
        ft.View(
            route="/signup",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src="assets/images/english_logo.png",
                                width=180,
                                height=180
                            ),
                            ft.Text("English Platform", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Text("Create your account", size=18, color=ft.Colors.GREY_800),
                            full_name := ft.TextField(
                                label="Full Name",
                                border_radius=12,
                                label_style=ft.TextStyle(color=ft.Colors.GREY_700),
                                text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                bgcolor=ft.Colors.GREY_100,
                                border_color=ft.Colors.BLUE_300,
                                focused_border_color=ft.Colors.BLUE_700
                            ),
                            password := ft.TextField(
                                label="Password",
                                border_radius=12,
                                label_style=ft.TextStyle(color=ft.Colors.GREY_700),
                                text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                bgcolor=ft.Colors.GREY_100,
                                border_color=ft.Colors.BLUE_300,
                                focused_border_color=ft.Colors.BLUE_700,
                                password=True,
                                can_reveal_password=True,
                            ),
                            level := ft.Dropdown(
                                label="Level",
                                label_style=ft.TextStyle(color=ft.Colors.GREY_700),
                                text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                options=[
                                    ft.dropdown.Option("Beginner"),
                                    ft.dropdown.Option("Pre-intermediate"),
                                    ft.dropdown.Option("Intermediate"),
                                    ft.dropdown.Option("Upper-intermediate"),
                                    ft.dropdown.Option("Advanced"),
                                ],
                                border_color=ft.Colors.GREY_400,
                                focused_border_color=ft.Colors.BLUE_400,
                                bgcolor=ft.Colors.GREY_100
                            ),
                            error_text,
                            ft.ElevatedButton("Register", on_click=do_signup, width=200),
                            ft.TextButton("Already have an account ?  Login", on_click=go_login),
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
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )
    page.update()
