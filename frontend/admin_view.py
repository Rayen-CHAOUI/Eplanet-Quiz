import flet as ft
import sqlite3

def fetch_all_users():
    conn = sqlite3.connect("eplanet_users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

def admin_view(page: ft.Page):
    user = page.session.get("user")

    if not user:
        page.go("/")
        return

    users_data = fetch_all_users()

    title = ft.Text("Admin Dashboard – All Users", size=30, weight=ft.FontWeight.BOLD)
    
    table_header = ft.Row(
        controls=[
            ft.Text("ID", weight="bold", width=50),
            ft.Text("Full Name", weight="bold", width=150),
            ft.Text("Password", weight="bold", width=150),
            ft.Text("Level", weight="bold", width=100),
            ft.Text("Right", weight="bold", width=60),
            ft.Text("Wrong", weight="bold", width=60),
            ft.Text("Created At", weight="bold", width=200),
        ],
        spacing=10,
    )

    table_rows = [
        ft.Row(
            controls=[
                ft.Text(str(u[0]), width=50),
                ft.Text(u[1], width=150),
                ft.Text(u[2], width=150),
                ft.Text(u[3], width=100),
                ft.Text(str(u[4]), width=60),
                ft.Text(str(u[5]), width=60),
                ft.Text(u[6], width=200),
            ],
            spacing=10,
        )
        for u in users_data
    ]

    page.views.clear()
    page.views.append(
        ft.View(
            route="/admin_view_users",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [title, table_header] + table_rows,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=10,
                    ),
                    padding=20,
                    expand=True,
                )
            ],
        )
    )
    page.update()
