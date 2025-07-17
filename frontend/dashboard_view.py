import flet as ft
import sqlite3


def dashboard_view(page: ft.Page):
    user = page.session.get("user")
    if not user:
        page.go("/")
        return

    def load_all_users():
        try:
            conn = sqlite3.connect("backend/eplanet_users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, level, right_answers, wrong_answers, created_at FROM users")
            users = cursor.fetchall()
            conn.close()
            return users
        except Exception as e:
            print("Failed to load users:", e)
            return []

    # Confirm dialog close helpers
    def close_dialog(_=None):
        page.dialog.open = False
        page.update()

    def confirm_logout_action(_=None):
        close_dialog()
        page.session.clear()
        page.go("/")

    def confirm_start_action(_=None):
        close_dialog()
        page.go("/quiz")

    logout_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Log Out"),
        content=ft.Text("Are you sure you want to log out?"),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.FilledButton("Logout", on_click=confirm_logout_action),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    start_quiz_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Start Quiz"),
        content=ft.Text("Are you ready to start the quiz now ?"),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.FilledButton("Yes, Start", on_click=confirm_start_action),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def show_logout_dialog(_):
        page.dialog = logout_dialog
        logout_dialog.open = True
        page.update()

    def show_start_dialog(_):
        page.dialog = start_quiz_dialog
        start_quiz_dialog.open = True
        page.update()

    def add_question(_):
        page.go("/add_question")

    # Top Nav Bar
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Eplanet Quiz Dashboard", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=show_logout_dialog, icon_color=ft.Colors.WHITE)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=25, vertical=16),
        bgcolor=ft.Colors.BLUE_800,
    )

    banner = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src="assets/images/eplanet_logo.png", width=300, height=300),
                
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            f"Welcome, {user['full_name']}!",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_900,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(f"ID: {user['id']}", size=30, color=ft.Colors.BLACK87),
                                    ft.Text(f"Level: {user['level']}", size=30, color=ft.Colors.BLACK87),
                                ],
                                spacing=5
                            ),
                            padding=12,
                            bgcolor=ft.Colors.BLUE_GREY_100,
                            border_radius=12,
                            shadow=ft.BoxShadow(
                                blur_radius=8,
                                color=ft.Colors.BLACK12,
                                offset=ft.Offset(0, 3),
                            )
                        )
                    ],
                    spacing=12
                ),
                ft.Image(src="assets/images/eplanet_logo.png", width=300, height=300),
            ]
        ),
        padding=ft.padding.symmetric(vertical=20, horizontal=30),
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=10,
            spread_radius=1,
            offset=ft.Offset(0, 3),
            color=ft.Colors.BLACK12
        )
    )

    # Buttons
    start_quiz_btn = ft.FilledButton(
        "Start Quiz",
        width=200,
        on_click=show_start_dialog,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_500,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
    )

    add_question_btn = ft.FilledButton(
        "Add Question",
        width=200,
        on_click=add_question,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.INDIGO_400,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
    )

    # Users table
    users = load_all_users()

    user_list_title = ft.Text(
        "All Students",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.INDIGO_900
    )

    user_table = ft.Column(
        controls=[
            ft.Row([
                ft.Text("Id",    weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.BLACK87),
                ft.Text("Name",  weight=ft.FontWeight.BOLD, width=250, color=ft.Colors.BLACK87),
                ft.Text("Level", weight=ft.FontWeight.BOLD, width=250, color=ft.Colors.BLACK87),
                ft.Text("Right", weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.GREEN_800),
                ft.Text("Wrong", weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.RED_800),
                ft.Text("Joined", weight=ft.FontWeight.BOLD, width=250, color=ft.Colors.BLACK87),
            ])
        ] + [
            ft.Row([
                ft.Text(u[0], width=150, color=ft.Colors.BLACK),
                ft.Text(u[1], width=250, color=ft.Colors.BLACK),
                ft.Text(u[2], width=250, color=ft.Colors.BLUE_800),
                ft.Text(str(u[3]), width=150, color=ft.Colors.GREEN_700),
                ft.Text(str(u[4]), width=150, color=ft.Colors.RED_700),
                ft.Text(u[5], width=250, color=ft.Colors.BLACK),
            ], spacing=10)
            for u in users if u[0] != user['full_name']
        ],
        spacing=8
    )

    user_card = ft.Container(
        content=ft.Column([user_list_title, user_table], spacing=15),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12, offset=ft.Offset(0, 3))
    )

    footer_text = ft.Text(
        "developed by CHAOUI RAYEN",
        size=15,
        italic=True,
        color=ft.Colors.BLUE_600
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/dashboard",
            controls=[
                top_nav,
                ft.Container(
                    content=ft.Column(
                        [
                            banner,
                            ft.Row([start_quiz_btn, add_question_btn], spacing=20),
                            ft.Divider(height=30),
                            user_card,
                        ],
                        spacing=30,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=30,
                    expand=True,
                ),
                ft.Container(
                    content=footer_text,
                    alignment=ft.alignment.bottom_right,
                    padding=10
                ),
                logout_dialog,
                start_quiz_dialog
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )
    )

    page.update()
