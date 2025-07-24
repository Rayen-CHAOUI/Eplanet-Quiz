import flet as ft
from frontend.Admin.admin_auth_for_signup import admin_authenticate_view
from frontend.Admin.admin_dashboard import admin_dashboard_view
from frontend.Admin.admin_login import admin_login_view
from frontend.Admin.admin_profile_view import admin_profile_view
from frontend.Admin.admin_user_edit import admin_user_edit
from frontend.Admin.lesson_admin_view.admin_quiz_screen import admin_quiz_screen
from frontend.Admin.lesson_admin_view.admin_result_screen import admin_result_view
from frontend.Admin.lesson_admin_view.admin_exercices_page import admin_exercises_view
from frontend.Admin.lesson_admin_view.admin_grammar_page import admin_grammar_page
from frontend.Admin.lesson_admin_view.admin_listening_page import admin_listening_page
from frontend.Admin.lesson_admin_view.admin_speaking_page import admin_speaking_page
from frontend.Admin.lesson_admin_view.admin_vocabulary_page import admin_vocabulary_page
from frontend.Admin.admin_signup import admin_signup_view
from frontend.Admin.admin_user_list_view import admin_user_list
from frontend.Admin.lesson_admin_view.add_question_view import add_question_view
from frontend.Admin.add_lessons.add_exercices import add_exercice_view
from frontend.Admin.add_lessons.add_listening_lesson import add_listening_lesson_view
from frontend.Admin.add_lessons.add_speaking_lesson import add_speaking_lesson_view
from frontend.Admin.add_lessons.add_vocabulary_lesson import add_vocabulary_lesson_view
from frontend.Users.user_lesson_view.exercices_page import exercises_view
from frontend.Users.user_lesson_view.grammar_page import grammar_page
from frontend.Admin.add_lessons.add_grammar_lesson_view import add_grammar_lesson_view
from frontend.Users.user_lesson_view.listening_page import listening_page
from frontend.Users.user_lesson_view.speaking_page import speaking_page
from frontend.Users.user_lesson_view.vocabulary_page import vocabulary_page
from frontend.Users.login_view import login_view
from frontend.Users.profile_view import profile_view
from frontend.Users.signup_view import signup_view
from frontend.Users.dashboard_view import dashboard_view
from frontend.Users.quiz_screen import quiz_screen
from frontend.Users.result_screen import result_view
from frontend.Users.user_list_view import user_list
from frontend.welcome_page import welcome_page


def _route_change(page: ft.Page):
    route = page.route
    if route == "/":
        welcome_page(page)
    elif route == "/welcome":
        welcome_page(page)
    elif route == "/login":
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
    elif route == "/profile":
        profile_view(page)
    elif route == "/admin_login":
        admin_login_view(page)
    elif route == "/admin_dashboard":
        admin_dashboard_view(page)
    elif route == "/admin_signup":
        admin_signup_view(page)
    elif route == "/admin_grammar":
        admin_grammar_page(page)
    elif route == "/admin_vocabulary":
        admin_vocabulary_page(page)
    elif route == "/admin_speaking":
        admin_speaking_page(page)
    elif route == "/admin_listening":
        admin_listening_page(page)
    elif route == "/admin_exercises":
        admin_exercises_view(page)
    elif route == "/admin_profile":
        admin_profile_view(page)
    elif route == "/admin_quiz":
        admin_quiz_screen(page)
    elif route == "/admin_result":
        admin_result_view(page)
    elif route == "/admin_users":
        admin_user_list(page)
    elif route.startswith("/admin_user_edit"):
        admin_user_edit(page)
    elif route == "/admin_authenticate":
        admin_authenticate_view(page)
    else:  # Error 404
        page.views.clear()
        page.views.append(
            ft.View(route, [ft.Text("oops ! Page not found.", size=24)]),
        )
        page.update()


def main(page: ft.Page):
    page.title = "English Learning Plateform"
    page.window_width = 500
    page.on_route_change = lambda _: _route_change(page)
    _route_change(page)  # load initial view


if __name__ == "__main__":
    ft.app(target=main)
