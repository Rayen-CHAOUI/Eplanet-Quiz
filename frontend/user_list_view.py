import flet as ft
import sqlite3

def user_list(page: ft.Page):
    def fetch_users():
        conn = sqlite3.connect("backend/eplanet_users.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, full_name, level, right_answers, wrong_answers, created_at
            FROM users
        """)
        users = cursor.fetchall()
        conn.close()
        return users

    def go_back(_):
        page.go("/dashboard")

    table_rows = []
    users = fetch_users()

    for index, user in enumerate(users):
        bg_color = ft.Colors.WHITE if index % 2 == 0 else ft.Colors.GREY_100
        table_rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(user[0]))),
                    ft.DataCell(ft.Text(user[1])),
                    ft.DataCell(ft.Text(user[2])),
                    ft.DataCell(ft.Text(str(user[3]))),
                    ft.DataCell(ft.Text(str(user[4]))),
                    ft.DataCell(ft.Text(user[5])),
                ],
                color=bg_color  
            )
        )

    page.views.append(
        ft.View(
            route="/users",
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Registered Users", size=30, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton("Back to Dashboard", on_click=go_back)
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Container(
                                content=ft.DataTable(
                                    columns=[
                                        ft.DataColumn(label=ft.Text("ID")),
                                        ft.DataColumn(label=ft.Text("Full Name")),
                                        ft.DataColumn(label=ft.Text("Level")),
                                        ft.DataColumn(label=ft.Text("Right Answers")),
                                        ft.DataColumn(label=ft.Text("Wrong Answers")),
                                        ft.DataColumn(label=ft.Text("Created At")),
                                    ],
                                    rows=table_rows,
                                ),
                                alignment=ft.alignment.center,
                                padding=20,
                                bgcolor=ft.Colors.GREY_50,
                                border_radius=12,
                                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_300)
                            )
                        ],
                        spacing=30,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO,
                    )
                )
            ]
        )
    )
    page.update()
