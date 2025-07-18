import flet as ft
import sqlite3
import os

DB_PATH = "backend/courses/vocabulary.db"

def load_vocabulary_lessons():
    if not os.path.exists(DB_PATH):
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM VocabularyLessons ORDER BY id")
        lessons = [row[0] for row in cursor.fetchall()]
        conn.close()
        return lessons
    except Exception as e:
        print("Failed to load vocabulary lessons:", e)
        return []

def vocabulary_page(page: ft.Page):
    lessons = load_vocabulary_lessons()
    if not lessons:
        lessons = ["No vocabulary lessons found."]

    index = ft.Ref[int]()
    lesson_text = ft.Ref[ft.Text]()

    index.current = 0

    def update_content():
        lesson_text.current.value = lessons[index.current]
        page.update()

    def go_next(_):
        if index.current < len(lessons) - 1:
            index.current += 1
            update_content()

    def go_previous(_):
        if index.current > 0:
            index.current -= 1
            update_content()

    # Top navigation bar
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Vocabulary Courses", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.FilledButton("Return to Home", on_click=lambda _: page.go("/dashboard"))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=20,
        bgcolor=ft.Colors.BLUE_800
    )

    # Main lesson display
    course_display = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(ref=lesson_text, size=26, text_align=ft.TextAlign.LEFT),
                ft.Row(
                    controls=[
                        ft.FilledButton("Previous", on_click=go_previous),
                        ft.FilledButton("Next", on_click=go_next)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30
                )
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=40,
        expand=True
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/vocabulary",
            controls=[top_nav, course_display],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )
    )

    update_content()
    page.update()
