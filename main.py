import flet as ft
from frontend.add_question_view import add_question_view
from frontend.lessons.add_exercices import add_exercice_view
from frontend.lessons.add_listening_lesson import add_listening_lesson_view
from frontend.lessons.add_speaking_lesson import add_speaking_lesson_view
from frontend.lessons.add_vocabulary_lesson import add_vocabulary_lesson_view
from frontend.lessons.exercices_page import exercises_view
from frontend.lessons.grammar_page import grammar_page
from frontend.lessons.add_grammar_lesson_view import add_grammar_lesson_view
from frontend.lessons.listening_page import listening_page
from frontend.lessons.speaking_page import speaking_page
from frontend.lessons.vocabulary_page import vocabulary_page
from frontend.login_view import login_view
from frontend.signup_view import signup_view
from frontend.dashboard_view import dashboard_view
from frontend.quiz_screen import quiz_screen
from frontend.result_screen import result_view
from frontend.user_list_view import user_list


def _route_change(page: ft.Page):
    route = page.route
    if route == "/":
        login_view(page)
    elif route == "/signup":
        signup_view(page)
    elif route == "/dashboard": 
        dashboard_view(page)
    elif route == "/quiz":
        quiz_screen(page)
    elif route == "/result":
        result_view(page)
    elif route == "/add_question":
        add_question_view(page)
    elif route == "/grammar":
        grammar_page(page)
    elif route == "/vocabulary":
        vocabulary_page(page)
    elif route == "/speaking":
        speaking_page(page)
    elif route == "/listening":
        listening_page(page)
    elif route == "/exercises":
        exercises_view(page)
    elif route == "/add_exercice":
        add_exercice_view(page)
    elif route == "/add_grammar_lesson":
        add_grammar_lesson_view(page)
    elif route == "/add_vocabulary_lesson":
        add_vocabulary_lesson_view(page)
    elif route == "/add_speaking_lesson":
        add_speaking_lesson_view(page)
    elif route == "/add_listening_lesson":
        add_listening_lesson_view(page)
    elif route == "/users":
        user_list(page)
    else:  # Error 404
        page.views.clear()
        page.views.append(
            ft.View(route, [ft.Text("Page not found.", size=24)]),
        )
        page.update()


def main(page: ft.Page):
    page.title = "Eplanet Quiz"
    page.window_width = 500
    page.on_route_change = lambda _: _route_change(page)
    _route_change(page)  # load initial view


if __name__ == "__main__":
    ft.app(target=main)
