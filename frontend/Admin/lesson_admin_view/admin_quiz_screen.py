import flet as ft
import sqlite3
import os
import asyncio


def admin_quiz_screen(page: ft.Page):
    db_path = "backend/quiz_questions.db"
    image_dir = "assets/images"
    audio_dir = "assets/audio"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

    user = page.session.get("user")
    current_index = 0
    selected_answers = []
    selected_option = None

    timer_text = ft.Text("20:00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600)

    async def start_timer():
        seconds_left = 20 * 60
        while seconds_left >= 0:
            mins = seconds_left // 60
            secs = seconds_left % 60
            timer_text.value = f"{mins:02d}:{secs:02d}"
            timer_text.update()
            await asyncio.sleep(1)
            seconds_left -= 1

        for i in range(current_index, len(questions)):
            selected_answers.append({
                "question": questions[i][1],
                "selected": None,
                "correct": questions[i][8]
            })
        page.session.set("quiz_answers", selected_answers)
        page.go("/admin_result")

    progress = ft.Text("", size=24, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87)
    question_text = ft.Text("", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK87)
    image = ft.Image(src="", width=320, height=200, visible=False)
    audio = ft.Audio(src="", autoplay=False)
    choices = []

    next_btn = ft.FilledButton(
        "Next",
        visible=False,
        width=200,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.TEAL_400,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
    )

    def close_dialog(_=None):
        confirm_dialog.open = False
        page.update()

    def confirm_exit(_=None):
        confirm_dialog.open = False
        page.update()
        for i in range(current_index, len(questions)):
            selected_answers.append({
                "question": questions[i][1],
                "selected": None,
                "correct": questions[i][8]
            })
        page.session.set("quiz_answers", selected_answers)
        page.go("/admin_result")

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Exit Quiz"),
        content=ft.Text("Are you sure you want to exit the quiz? Your progress will be submitted."),
        actions=[
            ft.TextButton("Cancel", on_click=close_dialog),
            ft.FilledButton("Yes, Submit", on_click=confirm_exit)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def show_exit_dialog(_):
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    for _ in range(4):
        btn = ft.ElevatedButton(
            text="",
            width=360,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TEAL_100,
                color=ft.Colors.BLACK87,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )
        choices.append(btn)

    def load_question(index):
        nonlocal selected_option
        selected_option = None
        next_btn.visible = False

        if index >= len(questions):
            page.session.set("quiz_answers", selected_answers)
            page.go("/admin_result")
            return

        q = questions[index]
        question_text.value = q[1]
        image_file = q[2]
        audio_file = q[3]
        options = [q[4], q[5], q[6], q[7]]

        progress.value = f"Question {index + 1} of {len(questions)}"

        image.visible = bool(image_file)
        image.src = os.path.join(image_dir, image_file) if image_file else ""

        audio.visible = bool(audio_file)
        audio.src = os.path.join(audio_dir, audio_file) if audio_file else ""

        for i, btn in enumerate(choices):
            btn.text = options[i]
            btn.data = chr(65 + i)
            btn.bgcolor = ft.Colors.TEAL_100
            btn.on_click = handle_answer

        page.update()

    def handle_answer(e):
        nonlocal selected_option
        selected_option = e.control.data

        for btn in choices:
            btn.bgcolor = ft.Colors.TEAL_100
        e.control.bgcolor = ft.Colors.TEAL_400

        next_btn.visible = True
        page.update()

    def next_question(_):
        nonlocal current_index, selected_option

        correct = questions[current_index][8]
        q_text = questions[current_index][1]

        selected_answers.append({
            "question": q_text,
            "selected": selected_option,
            "correct": correct
        })

        current_index += 1
        load_question(current_index)

    next_btn.on_click = next_question

    sidebar = ft.Container(
        width=300,
        padding=20,
        bgcolor=ft.Colors.BLUE_50,
        content=ft.Column(
            spacing=20,
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column([
                    ft.Text("Timer", size=22, weight=ft.FontWeight.W_600),
                    timer_text,
                    ft.Divider(),
                    ft.Text(f"User: {user['full_name']}", size=18),
                    ft.Text(f"Level: {user['level']}", size=18),
                    ft.Divider(),
                    progress,
                ]),
                ft.OutlinedButton(
                    "Exit Exam",
                    width=160,
                    style=ft.ButtonStyle(
                        color=ft.Colors.RED_400,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=show_exit_dialog
                )
            ]
        )
    )

    quiz_content = ft.Container(
        content=ft.Column(
            controls=[
                question_text,
                image,
                audio,
                ft.Column(choices, spacing=12),
                ft.Row([next_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
        ),
        width=800,
        padding=30,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 4),
            spread_radius=1
        ),
    )

    layout = ft.Row(
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            sidebar,
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=quiz_content
            )
        ]
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/admin_quiz",
            controls=[
                layout,
                confirm_dialog
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50
        )
    )

    load_question(current_index)
    page.run_task(start_timer)
    page.update()
