import flet as ft
import sqlite3
import os


def exercises_view(page: ft.Page):
    db_path = "backend/courses/exercises.db"
    image_dir = "assets/images"
    audio_dir = "assets/audio"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises")
    questions = cursor.fetchall()
    conn.close()

    current_index = 0
    selected_answers = []
    selected_option = None

    # UI elements
    progress = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)
    question_text = ft.Text("", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK87)
    image = ft.Image(src="", width=300, height=200, visible=False)
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

    # Exit confirmation dialog
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
        page.session.set("exercises_answers", selected_answers)
        page.go("/dashboard")

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Exit Exercises"),
        content=ft.Text("Are you sure you want to exit the exercises? Your progress will be submitted."),
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

    exit_btn = ft.OutlinedButton(
        "Exit Exercises",
        width=150,
        style=ft.ButtonStyle(
            color=ft.Colors.TEAL_700,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=show_exit_dialog
    )

    # Create answer choice buttons
    for _ in range(4):
        btn = ft.ElevatedButton(
            text="",
            width=320,
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
            page.session.set("exercises_answers", selected_answers)
            page.go("/dashboard")
            return

        q = questions[index]
        question_text.value = q[1]
        image_file = q[2]
        audio_file = q[3]
        options = [q[4], q[5], q[6], q[7]]

        progress.value = f"Question {index + 1} of {len(questions)}"

        image.visible = bool(image_file)
        if image_file:
            image.src = os.path.join(image_dir, image_file)

        audio.visible = bool(audio_file)
        audio.src = os.path.join(audio_dir, audio_file) if audio_file else ""

        for i, btn in enumerate(choices):
            btn.text = options[i]
            btn.data = chr(65 + i)
            btn.bgcolor = ft.Colors.TEAL_100
            btn.disabled = False
            btn.on_click = handle_answer

        page.update()

    def handle_answer(e):
        nonlocal selected_option
        if selected_option is not None:
            return  # Prevent selecting again

        selected_option = e.control.data
        correct_answer = questions[current_index][8]

        # Show correct/incorrect feedback
        for btn in choices:
            if btn.data == correct_answer:
                btn.bgcolor = ft.Colors.GREEN_300  # Correct option
            elif btn.data == selected_option:
                btn.bgcolor = ft.Colors.RED_300  # Incorrect option
            btn.disabled = True  # Disable all buttons

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

    top_nav = ft.Container(
        content=ft.Row(
            controls=[progress, exit_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        bgcolor=ft.Colors.TEAL_50,
        border_radius=ft.border_radius.all(8),
    )

    quiz_card = ft.Container(
        content=ft.Column(
            controls=[
                top_nav,
                question_text,
                image,
                audio,
                ft.Column(choices, spacing=10),
                ft.Row([next_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        width=600,
        padding=20,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 5),
            spread_radius=1
        ),
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/exercises",
            controls=[
                ft.Container(content=quiz_card, alignment=ft.alignment.top_center, expand=True),
                confirm_dialog
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50
        )
    )

    load_question(current_index)
    page.update()
