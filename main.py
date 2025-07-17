import flet as ft
from frontend.add_question_view import add_question_view
from frontend.admin_view import admin_view
from frontend.login_view import login_view
from frontend.signup_view import signup_view
from frontend.dashboard_view import dashboard_view 
from frontend.quiz_screen import quiz_screen
from frontend.result_screen import result_view

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
    elif route == "/admin_view_users":
        admin_view(page)
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
