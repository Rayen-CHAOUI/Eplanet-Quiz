import flet as ft
import sqlite3


def admin_result_view(page: ft.Page):
    answers = page.session.get("quiz_answers") or []
    user = page.session.get("user")

    if not user:
        page.go("/")
        return

    correct = sum(1 for a in answers if a["selected"] == a["correct"])
    wrong = sum(1 for a in answers if a["selected"] and a["selected"] != a["correct"])
    skipped = sum(1 for a in answers if a["selected"] is None)

    # Update DB
    try:
        conn = sqlite3.connect("backend/eplanet_users.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET right_answers = right_answers + ?,
                wrong_answers = wrong_answers + ?
            WHERE id = ?
        """, (correct, wrong, user["id"]))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Failed to update user score:", e)

    # Colors
    PRIMARY = ft.Colors.BLUE_GREY_900
    ACCENT = ft.Colors.TEAL_500
    BG = ft.Colors.BLUE_GREY_50

    title = ft.Text(
        "Your Quiz Results",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=PRIMARY
    )

    user_info = ft.Text(
        f"{user['full_name']} • Level: {user['level']}",
        size=25,
        color=ft.Colors.BLUE_GREY_600
    )

    result_summary = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(f"Correct: {correct}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                padding=15,
                bgcolor=ft.Colors.GREEN_50,
                border_radius=16
            ),
            ft.Container(
                content=ft.Text(f"Wrong: {wrong}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                padding=15,
                bgcolor=ft.Colors.RED_50,
                border_radius=16
            ),
            ft.Container(
                content=ft.Text(f"Skipped: {skipped}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_800),
                padding=15,
                bgcolor=ft.Colors.AMBER_50,
                border_radius=16
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Table headers
    table = ft.Column(
        controls=[
            ft.Row([
                ft.Text("No.", width=50, weight=ft.FontWeight.BOLD, color=PRIMARY),
                ft.Text("Question", expand=True, weight=ft.FontWeight.BOLD, color=PRIMARY),
                ft.Text("Status", width=120, weight=ft.FontWeight.BOLD, color=PRIMARY)
            ])
        ],
        spacing=12
    )

    # Table rows
    for idx, a in enumerate(answers):
        if a["selected"] is None:
            status_text = "Skipped"
            status_color = ft.Colors.AMBER_800
            bg_color = ft.Colors.AMBER_50
        elif a["selected"] == a["correct"]:
            status_text = "Correct"
            status_color = ft.Colors.GREEN_700
            bg_color = ft.Colors.GREEN_50
        else:
            status_text = "Wrong"
            status_color = ft.Colors.RED_700
            bg_color = ft.Colors.RED_50

        table.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(str(idx + 1), width=50, color=PRIMARY),
                    ft.Text(a["question"], expand=True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, color=PRIMARY),
                    ft.Text(status_text, width=120, color=status_color, weight=ft.FontWeight.BOLD),
                ]),
                padding=12,
                border_radius=12,
                bgcolor=bg_color
            )
        )

    back_button = ft.FilledButton(
        "Back to Dashboard",
        icon=ft.Icons.HOME,
        on_click=lambda _: page.go("/admin_dashboard"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            bgcolor=ACCENT,
            color=ft.Colors.WHITE
        )
    )

    result_card = ft.Container(
        content=ft.Column(
            [
                title,
                user_info,
                ft.Divider(height=20),
                result_summary,
                ft.Divider(height=30),
                ft.Text("Question Review", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY),
                table,
                ft.Divider(height=30),
                ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=25,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=30,
        width=850,
        bgcolor=ft.Colors.WHITE,
        border_radius=30,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 6),
        )
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/admin_result",
            bgcolor=BG,
            controls=[
                ft.Container(
                    content=result_card,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    )

    page.update()
