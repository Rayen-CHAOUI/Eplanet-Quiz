import flet as ft
import sqlite3
import os
import shutil

def add_listening_lesson_view(page: ft.Page):
    db_path = "backend/courses/listening.db"
    os.makedirs("assets/images", exist_ok=True)

    # UI Fields
    lesson_text = ft.TextField(label="Lesson Text", multiline=True, filled=True, border_radius=12, expand=True)
    image_file = ft.Text("No image uploaded", size=14, color=ft.Colors.RED_400)

    img_picker = ft.FilePicker()

    def pick_image(_):
        img_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"])

    def on_image_result(e: ft.FilePickerResultEvent):
        if e.files:
            src = e.files[0].path
            filename = os.path.basename(src)
            dest = f"assets/images/{filename}"
            shutil.copy(src, dest)
            image_file.value = f"Image: {filename}"
            image_file.color = ft.Colors.GREEN_600
            image_file.data = filename
            show_snackbar(f"Image '{filename}' uploaded!", ft.Colors.GREEN_400)

    def show_snackbar(message: str, bgcolor=ft.Colors.RED_400):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=bgcolor,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    def save_lesson(_):
        if not lesson_text.value.strip():
            show_snackbar("Lesson text is required!")
            return

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS listeningLesson (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    image TEXT
                )
            """)
            cursor.execute("""
                INSERT INTO listeningLesson (content, image) VALUES (?, ?)
            """, (
                lesson_text.value.strip(),
                image_file.data if hasattr(image_file, "data") else None
            ))
            conn.commit()
            conn.close()

            # Clear form
            lesson_text.value = ""
            image_file.value = "No image uploaded"
            image_file.color = ft.Colors.RED_400
            image_file.data = None

            show_snackbar("Lesson saved successfully!", ft.Colors.TEAL_400)

        except Exception as e:
            show_snackbar(f"Error saving lesson: {e}")

    # File Picker Binding
    img_picker.on_result = on_image_result
    page.overlay.append(img_picker)

    # Top Nav
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Add Listening Lesson", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.ElevatedButton(
                    "Back to Dashboard",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.go("/admin_dashboard"),
                    bgcolor=ft.Colors.BLUE_100,
                    color=ft.Colors.BLUE_900
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=10,
        bgcolor=ft.Colors.BLUE_50
    )

    form_card = ft.Container(
        content=ft.Column(
            controls=[
                lesson_text,
                ft.Row([
                    ft.FilledButton("Upload Image", icon=ft.Icons.IMAGE, on_click=pick_image),
                    image_file
                ], alignment=ft.MainAxisAlignment.START),
                ft.FilledButton("Save Lesson", icon=ft.Icons.SAVE, on_click=save_lesson, width=200, bgcolor=ft.Colors.BLUE_500)
            ],
            spacing=20
        ),
        width=800,
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 4))
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/add_listening_lesson",
            controls=[
                top_nav,
                ft.Container(content=form_card, alignment=ft.alignment.center, expand=True)
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50
        )
    )
    page.update()
