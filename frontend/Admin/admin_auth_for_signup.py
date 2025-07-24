import flet as ft
from backend.auth import authenticate_admin

def admin_authenticate_view(page: ft.Page):
    error_text = ft.Text("", color=ft.Colors.RED_400)

    admin_logo = ft.Image(
        src="assets/images/admin_logo.png",
        width=180,
        height=180
    )

    admin_id = ft.TextField(
        label="Admin ID",
        width=300,
        border_radius=12,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
        bgcolor=ft.Colors.GREY_100,
    )
    admin_password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=12,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
        bgcolor=ft.Colors.GREY_100,
    )

    def verify_admin(_):
        admin = authenticate_admin(admin_id.value, admin_password.value)
        if admin:
            page.session.set("admin_auth", True)
            page.go("/admin_signup")
        else:
            error_text.value = "Access denied: Invalid credentials"
            page.update()

    def go_back(_):
        page.go("/admin_login")

    page.views.clear()
    page.views.append(
        ft.View(
            route="/admin_authenticate",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            admin_logo,
                            ft.Text("Admin Access Verification", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Text("Authenthication required to continue", size=14,color=ft.Colors.GREY),
                            admin_id,
                            admin_password,
                            error_text,
                            ft.ElevatedButton("Verify", on_click=verify_admin, width=300),
                            ft.TextButton("Back to Login", on_click=go_back)
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=400
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=30
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )
    )
    page.update()
