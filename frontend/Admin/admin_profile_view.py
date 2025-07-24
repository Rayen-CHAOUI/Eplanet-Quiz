import flet as ft
import sqlite3


def admin_profile_view(page: ft.Page):
    user = page.session.get("user")
    if not user:
        page.go("/")
        return

    # Fields
    name_field = ft.TextField(
        label="Full Name",
        value=user["full_name"],
        width=400,
        border_radius=12,
        label_style=ft.TextStyle(color=ft.Colors.GREY_700),
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        bgcolor=ft.Colors.GREY_100,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
    )

    level_field = ft.Dropdown(
        label="Level",
        value=user["level"],
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
        bgcolor=ft.Colors.GREY_100,
        width=400,
    )

    password_field = ft.TextField(
        label="New Password",
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=12,
        label_style=ft.TextStyle(color=ft.Colors.GREY_700),
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        bgcolor=ft.Colors.GREY_100,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
    )

    confirm_password_field = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=12,
        label_style=ft.TextStyle(color=ft.Colors.GREY_700),
        text_style=ft.TextStyle(color=ft.Colors.BLACK),
        bgcolor=ft.Colors.GREY_100,
        border_color=ft.Colors.BLUE_300,
        focused_border_color=ft.Colors.BLUE_700,
    )

    message_text = ft.Text("", size=14)
    password_fields_container = ft.Column(controls=[], spacing=20)
    password_fields_visible = False

    def toggle_password_fields(_):
        nonlocal password_fields_visible
        password_fields_visible = not password_fields_visible
        if password_fields_visible:
            password_fields_container.controls = [password_field, confirm_password_field]
            toggle_password_button.text = "Cancel Password Change"
        else:
            password_fields_container.controls = []
            password_field.value = ""
            confirm_password_field.value = ""
            toggle_password_button.text = "Change Password"
        page.update()

    def update_user_data(_):
        name = name_field.value.strip()
        level = level_field.value.strip()
        new_password = password_field.value.strip()
        confirm_password = confirm_password_field.value.strip()

        if password_fields_visible and new_password != confirm_password:
            message_text.value = "Passwords do not match!"
            message_text.color = ft.Colors.RED
        else:
            try:
                conn = sqlite3.connect("backend/eplanet_users.db")
                cursor = conn.cursor()

                if password_fields_visible and new_password:
                    cursor.execute(
                        "UPDATE users SET full_name=?, level=?, password=? WHERE id=?",
                        (name, level, new_password, user["id"])
                    )
                else:
                    cursor.execute(
                        "UPDATE users SET full_name=?, level=? WHERE id=?",
                        (name, level, user["id"])
                    )

                conn.commit()
                conn.close()

                user["full_name"] = name
                user["level"] = level
                page.session.set("user", user)

                message_text.value = "Profile updated successfully!"
                message_text.color = ft.Colors.GREEN

            except Exception as e:
                print("Error:", e)
                message_text.value = "Failed to update profile!"
                message_text.color = ft.Colors.RED

        page.update()

    def show_confirmation_dialog(_):
        confirm_dialog.open = True
        page.update()

    def on_confirm(e):
        confirm_dialog.open = False
        page.update()
        update_user_data(e)

    def on_cancel(e):
        confirm_dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Changes"),
        content=ft.Text("Are you sure you want to save these profile changes?"),
        actions=[
            ft.TextButton("Cancel", on_click=on_cancel),
            ft.ElevatedButton("Yes, Save", on_click=on_confirm),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # 👉 Add dialog to overlay here
    page.overlay.append(confirm_dialog)

    def go_back(_):
        page.go("/admin_dashboard")

    toggle_password_button = ft.TextButton(
        text="Change Password",
        on_click=toggle_password_fields,
    )

    profile_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Edit Profile", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                name_field,
                level_field,
                toggle_password_button,
                password_fields_container,
                ft.ElevatedButton(
                    text="Save Changes",
                    icon=ft.Icons.SAVE_OUTLINED,
                    on_click=show_confirmation_dialog,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
                ),
                message_text,
                ft.TextButton("← Back to Dashboard", on_click=go_back),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=40,
        margin=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
        width=500,
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/admin_profile",
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[profile_card],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                )
            ],
            bgcolor=ft.Colors.GREY_100,
        )
    )
    page.update()
