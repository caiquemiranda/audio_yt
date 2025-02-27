import flet as ft

def create_preview_container():
    return ft.Container(
        width=300,
        height=200,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        padding=10,
        visible=False
    )

def create_video_info():
    return ft.Column(
        controls=[
            ft.Text("", size=16, weight="bold", width=300),
            ft.Text("", size=14, color="grey"),
        ],
        visible=False
    ) 