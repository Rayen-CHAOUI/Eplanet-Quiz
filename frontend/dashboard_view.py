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

    def go_to(route):
        def handler(_):
            page.go(route)
        return handler

    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Eplanet Quiz Dashboard", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Row(
                    controls=[
                        ft.TextButton("Add Question", on_click=go_to("/add_question"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                        ft.TextButton("Add Grammar", on_click=go_to("/add_grammar_lesson"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                        ft.TextButton("Add Vocabulary", on_click=go_to("/add_vocabulary_lesson"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                        ft.TextButton("Add Speaking", on_click=go_to("/add_speaking_lesson"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                        ft.TextButton("Add Listening", on_click=go_to("/add_listening_lesson"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                        ft.TextButton("Add Exercises", on_click=go_to("/add_exercice"), style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                        ft.IconButton(icon=ft.Icons.LOGOUT, tooltip="Logout", on_click=show_logout_dialog, icon_color=ft.Colors.WHITE),
                    ],
                    spacing=10
                )
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
                            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12, offset=ft.Offset(0, 3)),
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
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, offset=ft.Offset(0, 3), color=ft.Colors.BLACK12)
    )

    # Wide full-width button style
    def wide_button(label, color, route):
        return ft.FilledButton(
            text=label,
            on_click=go_to(route),
            height=60,
            width=600,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=14),
            )
        )

    # Vertical buttons list
    button_list = ft.Column(
        controls=[
            wide_button("Start the Quiz", ft.Colors.GREEN_600, "/quiz"),
            wide_button("Grammar Courses", ft.Colors.BLUE_600, "/grammar"),
            wide_button("Vocabulary Courses", ft.Colors.DEEP_ORANGE_400, "/vocabulary"),
            wide_button("Speaking", ft.Colors.PURPLE_500, "/speaking"),
            wide_button("Listening", ft.Colors.CYAN_600, "/listening"),
            wide_button("Exercises", ft.Colors.INDIGO_400, "/exercises"),
            wide_button("Students Ranking", ft.Colors.TEAL_500, "/users"),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/dashboard",
            controls=[
                top_nav,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            banner,
                            button_list,
                        ],
                        spacing=30,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=30,
                    expand=True,
                ),
                logout_dialog,
                start_quiz_dialog
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )
    )

    page.update()
