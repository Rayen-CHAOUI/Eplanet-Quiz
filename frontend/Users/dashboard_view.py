import flet as ft
import sqlite3


def dashboard_view(page: ft.Page):
    user = page.session.get("user")
    if not user:
        page.go("/")
        return


    def close_dialog(_=None):
        page.dialog.open = False
        page.update()

    def confirm_logout_action(_=None):
        close_dialog()
        page.session.clear()
        page.go("/welcome")

    def confirm_start_action(_=None):
        close_dialog()
        page.go("/quiz")

    # Modern styled dialogs
    logout_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Logout", size=20, weight=ft.FontWeight.W_600),
        content=ft.Text("Are you sure you want to log out of your session?", size=14),
        actions=[
            ft.TextButton(
                "Cancel", 
                on_click=close_dialog,
                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
            ),
            ft.ElevatedButton(
                "Logout", 
                on_click=confirm_logout_action,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_500,
                    color=ft.Colors.WHITE,
                )
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=16),
    )

    start_quiz_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Start Assessment", size=20, weight=ft.FontWeight.W_600),
        content=ft.Text("Ready to begin your English proficiency assessment?", size=14),
        actions=[
            ft.TextButton(
                "Not Yet", 
                on_click=close_dialog,
                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
            ),
            ft.ElevatedButton(
                "Start Now", 
                on_click=confirm_start_action,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                )
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=16),
    )

    def show_logout_dialog(_):
        if logout_dialog not in page.controls:
            page.overlay.append(logout_dialog) 
        page.dialog = logout_dialog
        logout_dialog.open = True
        page.update()
    

    def show_start_dialog(_):
        if start_quiz_dialog not in page.controls:
            page.overlay.append(start_quiz_dialog)  
        page.dialog = start_quiz_dialog
        start_quiz_dialog.open = True
        page.update()

    def go_to(route):
        def handler(_):
            page.go(route)
        return handler

    # Modern top navigation with gradient background
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL_OUTLINED, color=ft.Colors.WHITE, size=28),
                        ft.Text(
                            "English Learning Platform", 
                            size=22, 
                            weight=ft.FontWeight.W_600, 
                            color=ft.Colors.WHITE
                        ),
                    ],
                    spacing=12,
                ),
                ft.Row(
                    controls=[
                        # User menu
                        ft.Container(
                            content=ft.PopupMenuButton(
                                content=ft.Row([
                                    ft.CircleAvatar(
                                        content=ft.Text(user['full_name'][0].upper(), color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                        bgcolor=ft.Colors.WHITE24,
                                        radius=18,
                                    ),
                                    ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=ft.Colors.WHITE70, size=20),
                                ], spacing=8),
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=18),
                                            ft.Text("Profile", size=14)
                                        ], spacing=8),
                                        on_click=go_to("/profile"),
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=18),
                                            ft.Text("Settings", size=14)
                                        ], spacing=8),
                                    ),
                                    ft.PopupMenuItem(
                                        content=ft.Row([
                                            ft.Icon(ft.Icons.LOGOUT_OUTLINED, size=18),
                                            ft.Text("Logout", size=14)
                                        ], spacing=8),
                                        on_click=show_logout_dialog,
                                    ),
                                ],
                                menu_position=ft.PopupMenuPosition.UNDER,
                            ),
                            padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        ),
                    ],
                    spacing=4
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=32, vertical=20),
        gradient=ft.LinearGradient(
            colors=[ft.Colors.BLUE_700, ft.Colors.BLUE_900],
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
        ),
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK26, offset=ft.Offset(0, 2)),
    )

    # Modern welcome banner with cards
    banner = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Text(
                                f"Welcome back, {user['full_name'].split()[0]} ! 👋",
                                size=45,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Text(
                                "Ready to continue your English learning journey?",
                                size=20,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Container(height=20),  # Spacer
                            ft.Row(
                                controls=[
                                    # User info cards
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("Student ID", size=15, color=ft.Colors.GREY_500, weight=ft.FontWeight.W_500),
                                                ft.Text(f"#{user['id']:05d}", size=25, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD),
                                            ],
                                            spacing=4,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        padding=20,
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=12,
                                        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
                                        width=150,
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("Current Level", size=15, color=ft.Colors.GREY_500, weight=ft.FontWeight.W_500),
                                                ft.Text(f"{user['level']}", size=22, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                                            ],
                                            spacing=4,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        padding=20,
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=12,
                                        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12, offset=ft.Offset(0, 2)),
                                        width=200,
                                    ),
                                ],
                                spacing=16,
                            ),
                        ],
                        spacing=8
                    ),
                    padding=40,
                ),
            ]
        ),
        padding=ft.padding.symmetric(vertical=30, horizontal=40),
        bgcolor=ft.Colors.TRANSPARENT,
    )

    # Modern feature cards with icons and better styling
    def feature_card(title, subtitle, icon, color, route=None, accent_color=None, on_click_handler=None):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=24),
                                padding=12,
                                bgcolor=f"{color}20",
                                border_radius=50,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(title, size=24, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_800),
                                    ft.Text(subtitle, size=19, color=ft.Colors.GREY_600),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=22, color=ft.Colors.GREY_400),
                        ],
                        spacing=16,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            ),
            padding=24,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=10, 
                spread_radius=0, 
                offset=ft.Offset(0, 4), 
                color=ft.Colors.BLACK12
            ),
            on_click=on_click_handler if on_click_handler else go_to(route),
            ink=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )



    CARD_WIDTH = 500  

    features_grid = ft.Column(
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Assessment Quiz", 
                        "Test your English proficiency", 
                        ft.Icons.QUIZ_OUTLINED, 
                        ft.Colors.GREEN_600, 
                        on_click_handler=show_start_dialog,
                        accent_color=ft.Colors.GREEN_50
                    )),
                    ft.Container(width=20),  # Spacer
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Grammar Courses", 
                        "Master English grammar rules", 
                        ft.Icons.AUTO_STORIES_OUTLINED, 
                        ft.Colors.BLUE_600, 
                        "/grammar",
                        ft.Colors.BLUE_50
                    )),
                ],
            ),
            ft.Container(height=20),  # Row spacer
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Vocabulary Builder", 
                        "Expand your word knowledge", 
                        ft.Icons.TRANSLATE_OUTLINED, 
                        ft.Colors.DEEP_ORANGE_500, 
                        "/vocabulary",
                        ft.Colors.BLACK
                    )),
                    ft.Container(width=20),
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Speaking Practice", 
                        "Improve pronunciation & fluency", 
                        ft.Icons.MIC_OUTLINED, 
                        ft.Colors.PURPLE_600, 
                        "/speaking",
                        ft.Colors.PURPLE_50
                    )),
                ],
            ),
            ft.Container(height=20),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Listening Skills", 
                        "Enhance comprehension abilities", 
                        ft.Icons.HEADPHONES_OUTLINED, 
                        ft.Colors.CYAN_600, 
                        "/listening",
                        ft.Colors.CYAN_50
                    )),
                    ft.Container(width=20),
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Practice Exercises", 
                        "Reinforce your learning", 
                        ft.Icons.FITNESS_CENTER_OUTLINED, 
                        ft.Colors.INDIGO_600, 
                        "/exercises",
                        ft.Colors.INDIGO_50
                    )),
                ],
            ),
            ft.Container(height=20),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(width=CARD_WIDTH, content=feature_card(
                        "Student Management", 
                        "View registered learners", 
                        ft.Icons.PEOPLE_OUTLINE, 
                        ft.Colors.TEAL_600, 
                        "/users",
                        ft.Colors.TEAL_50
                    )),
                ],
            ),
        ],
        spacing=0
    )


    page.views.clear()
    page.views.append(
        ft.View(
            route="/dashboard",
            controls=[
                top_nav,
                ft.Container(
                    content=ft.Column(
                        controls=[
                            banner,
                            ft.Container(
                                content=features_grid,
                                padding=ft.padding.symmetric(horizontal=40, vertical=20),
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    expand=True,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.GREY_50,
            padding=0,
        )
    )

    page.update()