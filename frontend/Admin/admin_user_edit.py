import flet as ft
import sqlite3
import urllib.parse
import hashlib

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def admin_user_edit(page: ft.Page):
    parsed_url = urllib.parse.urlparse(page.route)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    user_id = query_params.get("id", [None])[0]

    if not user_id:
        page.go("/admin_users")
        return

    def get_user_data(user_id):
        conn = sqlite3.connect("backend/eplanet_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, level FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def update_user_data(_):
        full_name = name_field.value.strip()
        level = level_field.value.strip()
        new_password = password_field.value.strip()

        conn = sqlite3.connect("backend/eplanet_users.db")
        cursor = conn.cursor()

        if new_password:
            hashed_password = _hash_password(new_password)
            cursor.execute(
                "UPDATE users SET full_name = ?, level = ?, password = ? WHERE id = ?",
                (full_name, level, hashed_password, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET full_name = ?, level = ? WHERE id = ?",
                (full_name, level, user_id)
            )

        conn.commit()
        conn.close()
        status_text.value = "User updated successfully!"
        status_text.color = ft.Colors.GREEN
        page.update()

    def show_confirmation_dialog(_):
        confirm_dialog.open = True
        page.update()

    def on_confirm(e):
        confirm_dialog.open = False
        update_user_data(e)

    def on_cancel(e):
        confirm_dialog.open = False
        page.update()

    def go_back(_):
        page.go("/admin_users")

    user_data = get_user_data(user_id)
    if not user_data:
        page.go("/admin_users")
        return

    name_field = ft.TextField(
        label="Full Name",
        value=user_data[0],
        width=400,
        border_radius=12,
        bgcolor=ft.Colors.GREY_100,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
        label_style=ft.TextStyle(color=ft.Colors.GREY_700)
    )

    level_field = ft.Dropdown(
        label="Level",
        value=user_data[1],
        options=[
            ft.dropdown.Option("Beginner"),
            ft.dropdown.Option("Pre-intermediate"),
            ft.dropdown.Option("Intermediate"),
            ft.dropdown.Option("Upper-intermediate"),
            ft.dropdown.Option("Advanced"),
        ],
        width=400,
        bgcolor=ft.Colors.GREY_100,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        label_style=ft.TextStyle(color=ft.Colors.GREY_700)
    )

    password_field = ft.TextField(
        label="New Password",
        value="",
        width=400,
        password=True,
        can_reveal_password=True,
        border_radius=12,
        bgcolor=ft.Colors.GREY_100,
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
        label_style=ft.TextStyle(color=ft.Colors.GREY_700)
    )

    status_text = ft.Text("", size=14)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Changes"),
        content=ft.Text("Are you sure you want to save these changes?"),
        actions=[
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Yes, Save", on_click=on_confirm),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(confirm_dialog)

    page.views.append(
        ft.View(
            route="/admin_user_edit",
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=30,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Edit User", size=30, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton("Back to Users", on_click=go_back),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Container(height=20),
                            name_field,
                            level_field,
                            password_field,
                            ft.Container(height=10),
                            ft.ElevatedButton(
                                "Save Changes",
                                icon=ft.Icons.SAVE_OUTLINED,
                                on_click=show_confirmation_dialog,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                            ),
                            status_text
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            ],
            bgcolor=ft.Colors.GREY_50,
            scroll=ft.ScrollMode.AUTO
        )
    )
    page.update()
