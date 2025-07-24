import flet as ft
from backend.auth import authenticate_admin

def admin_login_view(page: ft.Page):
    error_text = ft.Text("", color=ft.Colors.RED_400, size=12)

    def do_login(_):
        user = authenticate_admin(user_id.value, password.value)
        if user:
            page.session.set("user", user)
            page.go("/admin_dashboard")
        else:
            error_text.value = "Invalid ID or Password."
            page.snack_bar = ft.SnackBar(ft.Text("Invalid ID or password."))
            page.snack_bar.open = True
            page.update()

    def go_signup(_):
        page.go("/admin_authenticate")

    def go_back(_):
        page.go("/")

    # Force light theme
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
 
    page.views.clear()
    page.views.append(
        ft.View(
            route="/admin_login",  
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src="assets/images/admin_logo.png",
                                width=180,
                                height=180
                            ),
                            ft.Text(
                                "Admin Platform",
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900
                            ),
                            ft.Text(
                                "Login to your Admin account",
                                size=18,
                                color=ft.Colors.GREY_800
                            ),
                            user_id := ft.TextField(
                                label="Enter your ID",
                                border_radius=12,
                                filled=True,
                                bgcolor=ft.Colors.GREY_100,
                                border_color=ft.Colors.BLUE_300,
                                focused_border_color=ft.Colors.BLUE_700
                            ),
                            password := ft.TextField(
                                label="Enter your Password",
                                border_radius=12,
                                filled=True,
                                bgcolor=ft.Colors.GREY_100,
                                border_color=ft.Colors.BLUE_300,
                                focused_border_color=ft.Colors.BLUE_700,
                                password=True,
                                can_reveal_password=True
                            ),
                            error_text,
                            ft.ElevatedButton(
                                "Login",
                                on_click=do_login,
                                width=200,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=14)
                                )
                            ),
                            ft.TextButton(
                                "Don't have an account ? Sign up",
                                on_click=go_signup,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE_700
                                )
                            ),
                            ft.Container(height=10),  # Spacer
                            ft.ElevatedButton(
                                "Return to Home",
                                on_click=go_back,
                                width=400,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=14),
                                    text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
                                )
                            ),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=400
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=40
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )
    page.update()
