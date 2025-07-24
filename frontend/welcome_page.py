import flet as ft
from flet import Icons


def welcome_page(page: ft.Page):
    page.title = "English Learning Plateform"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.GREY_50

    # Navigation handlers
    def navigate_to_login(e):
        page.go("/login")

    def navigate_to_admin_login(e):
        page.go("/admin_login")

    # Create the welcome page layout
    welcome_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src="assets/images/welcome_logo.png",
                                width=180,
                                height=180
                            ),
                            ft.Text(
                                "Welcome to the English Platform !",
                                size=48,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_800,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Choose your portal to continue",
                                size=18,
                                color=ft.Colors.GREY_600,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=ft.padding.only(top=80, bottom=60)
                ),

                # Buttons
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.PERSON, size=24, color=ft.Colors.BLUE),
                                            ft.Text("User Login", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=12
                                    ),
                                    on_click=navigate_to_login,
                                    style=ft.ButtonStyle(
                                        elevation={"default": 3, "hovered": 6},
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(horizontal=32, vertical=16)
                                    ),
                                    width=280,
                                    height=60
                                ),
                                margin=ft.margin.only(bottom=20)
                            ),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.ADMIN_PANEL_SETTINGS, size=24, color=ft.Colors.BLUE),
                                            ft.Text("Admin Login", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=12
                                    ),
                                    on_click=navigate_to_admin_login,
                                    style=ft.ButtonStyle(
                                        elevation={"default": 3, "hovered": 6},
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(horizontal=32, vertical=16)
                                    ),
                                    width=280,
                                    height=60
                                )
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    padding=ft.padding.symmetric(horizontal=40)
                ),

                # Footer
                ft.Container(
                    content=ft.Text(
                        "© developed by Rayen-CHAOUI",
                        size=12,
                        color=ft.Colors.BLUE_GREY,
                        text_align=ft.TextAlign.CENTER,
                        italic=True
                    ),
                    margin=ft.margin.only(top=100)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        padding=40,
        margin=40,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.GREY_400),
            offset=ft.Offset(0, 4)
        ),
        width=1000,
        alignment=ft.alignment.center
    )

    # Main gradient background
    main_container = ft.Container(
        content=ft.Column(
            controls=[welcome_container],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        gradient=ft.LinearGradient(
            colors=[ft.Colors.BLUE_50, ft.Colors.INDIGO_50, ft.Colors.PURPLE_50],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right
        ),
        alignment=ft.alignment.center
    )

    page.views.clear()
    page.views.append(
        ft.View(
            route="/welcome",
            controls=[main_container],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
    )
    page.update()
