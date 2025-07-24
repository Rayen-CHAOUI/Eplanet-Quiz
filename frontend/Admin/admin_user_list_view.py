import flet as ft
import sqlite3


def admin_user_list(page: ft.Page):
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
        page.go("/admin_dashboard")

    def go_to_edit(user_id):
        def handler(_):
            page.go(f"/admin_user_edit?id={user_id}")
        return handler

    users = fetch_users()

    table_rows = []
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
                color=bg_color,
                on_select_changed=go_to_edit(user[0])
            )
        )

    # ---------- Graphic summary logic ------------
    graphic_container = ft.Column(visible=False, spacing=20)

    def toggle_graphics_view(e):
        graphic_container.visible = not graphic_container.visible
        e.control.text = "Hide Graphics" if graphic_container.visible else "Show Graphics"
        graphic_container.update()
        e.control.update()


    # Add user progress bars
    for user in users:
        user_id, full_name, level, right, wrong, created = user
        total = right + wrong if (right + wrong) > 0 else 1
        graphic_container.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{full_name} | Level: {level} | Joined: {created}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Text("Correct", width=80),
                            ft.ProgressBar(value=right / total, width=300, color=ft.Colors.GREEN),
                            ft.Text(f"{right}/{total}")
                        ]),
                        ft.Row([
                            ft.Text("Wrong", width=80),
                            ft.ProgressBar(value=wrong / total, width=300, color=ft.Colors.RED),
                            ft.Text(f"{wrong}/{total}")
                        ])
                    ],
                    spacing=5
                ),
                padding=10,
                bgcolor=ft.Colors.GREY_100,
                border_radius=8
            )
        )

    # ---------- UI Rendering ------------
    page.views.append(
        ft.View(
            route="/admin_users",
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
                                    ft.Row([
                                        ft.ElevatedButton("Show Graphics", on_click=toggle_graphics_view),
                                        ft.ElevatedButton("Back to Dashboard", on_click=go_back),
                                    ])
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
                            ),
                            graphic_container
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
