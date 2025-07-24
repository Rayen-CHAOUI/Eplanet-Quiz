import flet as ft
import sqlite3
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def result_view(page: ft.Page):
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

    def generate_pdf(path: str):
        if not path:
            return

        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4

        # Logo
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, x=40, y=height - 100, width=60, height=60, mask='auto')

        # Title
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(colors.HexColor("#263238"))
        c.drawString(120, height - 70, "Eplanet Quiz Result Report")

        # User info
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.HexColor("#455A64"))
        c.drawString(40, height - 130, f"Name: {user['full_name']}")
        c.drawString(40, height - 150, f"Level: {user['level']}")

        # Summary
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor("#004D40"))
        c.drawString(40, height - 190, f"Correct: {correct}")
        c.setFillColor(colors.HexColor("#B71C1C"))
        c.drawString(150, height - 190, f"Wrong: {wrong}")
        c.setFillColor(colors.HexColor("#FF6F00"))
        c.drawString(250, height - 190, f"Skipped: {skipped}")

        # Table header
        y = height - 230
        c.setFillColor(colors.HexColor("#263238"))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "No.")
        c.drawString(80, y, "Question")
        c.drawString(400, y, "Status")

        # Table rows
        c.setFont("Helvetica", 11)
        for idx, a in enumerate(answers):
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
            status = "Skipped" if a["selected"] is None else ("Correct" if a["selected"] == a["correct"] else "Wrong")
            color = {"Correct": colors.green, "Wrong": colors.red, "Skipped": colors.orange}[status]

            c.setFillColor(colors.black)
            c.drawString(40, y, str(idx + 1))
            c.drawString(80, y, a["question"][:50] + "...")
            c.setFillColor(color)
            c.drawString(400, y, status)

        c.save()

        page.dialog = ft.AlertDialog(
            title=ft.Text("PDF Exported Successfully"),
            content=ft.Text(f"Saved to: {path}"),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dialog())],
        )
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    # FilePicker for PDF export
    file_picker = ft.FilePicker(on_result=lambda e: generate_pdf(e.path if e.files else None))
    page.overlay.append(file_picker)

    # UI Components
    title = ft.Text("Your Quiz Results", size=36, weight=ft.FontWeight.BOLD, color=PRIMARY)

    user_info = ft.Text(f"{user['full_name']} • Level: {user['level']}", size=25, color=ft.Colors.BLUE_GREY_600)

    result_summary = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(f"Correct: {correct}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                padding=15, bgcolor=ft.Colors.GREEN_50, border_radius=16
            ),
            ft.Container(
                content=ft.Text(f"Wrong: {wrong}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                padding=15, bgcolor=ft.Colors.RED_50, border_radius=16
            ),
            ft.Container(
                content=ft.Text(f"Skipped: {skipped}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_800),
                padding=15, bgcolor=ft.Colors.AMBER_50, border_radius=16
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Question Table
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

    for idx, a in enumerate(answers):
        if a["selected"] is None:
            status_text, status_color, bg_color = "Skipped", ft.Colors.AMBER_800, ft.Colors.AMBER_50
        elif a["selected"] == a["correct"]:
            status_text, status_color, bg_color = "Correct", ft.Colors.GREEN_700, ft.Colors.GREEN_50
        else:
            status_text, status_color, bg_color = "Wrong", ft.Colors.RED_700, ft.Colors.RED_50

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
        on_click=lambda _: page.go("/dashboard"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            bgcolor=ACCENT,
            color=ft.Colors.WHITE
        )
    )

    extract_button = ft.FilledButton(
        "Download as PDF",
        icon=ft.Icons.PICTURE_AS_PDF,
        on_click=lambda _: file_picker.save_file(
            dialog_title="Save Quiz Result as PDF",
            file_name=f"quiz_result_{user['full_name'].replace(' ', '_')}.pdf",
            allowed_extensions=["pdf"]
        ),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            bgcolor=PRIMARY,
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
                ft.Row([extract_button, back_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
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
            route="/result",
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
