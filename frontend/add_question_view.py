import flet as ft
import sqlite3
import os
import shutil


def add_question_view(page: ft.Page):
    db_path = "backend/quiz_questions.db"
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/audio", exist_ok=True)

    # --- UI Fields ---
    question = ft.TextField(label="Question", multiline=True, filled=True, border_radius=12)
    choice_a = ft.TextField(label="Choice A", filled=True, border_radius=12)
    choice_b = ft.TextField(label="Choice B", filled=True, border_radius=12)
    choice_c = ft.TextField(label="Choice C", filled=True, border_radius=12)
    choice_d = ft.TextField(label="Choice D", filled=True, border_radius=12)

    correct_choice = ft.Dropdown(
        label="Correct Answer",
        options=[
            ft.dropdown.Option("A"), ft.dropdown.Option("B"),
            ft.dropdown.Option("C"), ft.dropdown.Option("D")
        ],
        filled=True,
        border_radius=12,
        width=200
    )

    image_file = ft.Text("No image uploaded", size=14, color=ft.Colors.RED_400)
    audio_file = ft.Text("No audio uploaded", size=14, color=ft.Colors.RED_400)

    img_picker = ft.FilePicker()
    audio_picker = ft.FilePicker()

    def pick_image(_):
        img_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])

    def pick_audio(_):
        audio_picker.pick_files(allow_multiple=False, allowed_extensions=["mp3", "wav"])

    def on_image_result(e: ft.FilePickerResultEvent):
        if e.files:
            src = e.files[0].path
            filename = os.path.basename(src)
            shutil.copy(src, f"assets/images/{filename}")
            image_file.value = f"Image: {filename}"
            image_file.color = ft.Colors.GREEN_600
            image_file.data = filename
            show_snackbar(f"Image '{filename}' added", ft.Colors.GREEN_400)

    def on_audio_result(e: ft.FilePickerResultEvent):
        if e.files:
            src = e.files[0].path
            filename = os.path.basename(src)
            shutil.copy(src, f"assets/audio/{filename}")
            audio_file.value = f"Audio: {filename}"
            audio_file.color = ft.Colors.GREEN_600
            audio_file.data = filename
            show_snackbar(f"Audio '{filename}' added", ft.Colors.GREEN_400)

    def show_snackbar(message: str, bgcolor=ft.Colors.RED_400):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=bgcolor,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    def save_question(_):
        if not question.value or not correct_choice.value:
            show_snackbar("Please fill in all required fields!")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                image_path TEXT,
                audio_path TEXT,
                choice_a TEXT,
                choice_b TEXT,
                choice_c TEXT,
                choice_d TEXT,
                correct_choice TEXT
            )
            """)
            cursor.execute("""
            INSERT INTO questions (
                question_text, image_path, audio_path,
                choice_a, choice_b, choice_c, choice_d, correct_choice
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question.value,
                image_file.data if hasattr(image_file, "data") else None,
                audio_file.data if hasattr(audio_file, "data") else None,
                choice_a.value,
                choice_b.value,
                choice_c.value,
                choice_d.value,
                correct_choice.value
            ))
            conn.commit()
            conn.close()

            for field in [question, choice_a, choice_b, choice_c, choice_d]:
                field.value = ""
            correct_choice.value = None
            image_file.value = "No image uploaded"
            audio_file.value = "No audio uploaded"
            image_file.color = audio_file.color = ft.Colors.RED_400
            image_file.data = audio_file.data = None

            show_snackbar("Question saved successfully!", ft.Colors.TEAL_400)

        except Exception as e:
            show_snackbar(f"Error saving question: {e}")

    # File picker event binding
    img_picker.on_result = on_image_result
    audio_picker.on_result = on_audio_result
    page.overlay.extend([img_picker, audio_picker])

    # --- Layout ---
    nav_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Add Question", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_700),
                ft.ElevatedButton(
                    "Back to Dashboard",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/dashboard"),
                    bgcolor=ft.Colors.TEAL_100,
                    color=ft.Colors.TEAL_900
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=10,
        bgcolor=ft.Colors.TEAL_50
    )

    form_card = ft.Container(
        content=ft.Column(
            controls=[
                question,
                ft.Row([choice_a, choice_b], spacing=10),
                ft.Row([choice_c, choice_d], spacing=10),
                correct_choice,
                ft.Row(
                    [
                        ft.FilledButton("Upload Image", icon=ft.Icons.IMAGE, on_click=pick_image),
                        ft.FilledButton("Upload Audio", icon=ft.Icons.AUDIOTRACK, on_click=pick_audio)
                    ],
                    spacing=10
                ),
                ft.Row([image_file, audio_file], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.FilledButton("Save Question", on_click=save_question, width=220, bgcolor=ft.Colors.TEAL_400),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=800,
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 6)
        ),
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/add-question",
            controls=[
                nav_bar,
                ft.Container(
                    content=form_card,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50
        )
    )
    page.update()
