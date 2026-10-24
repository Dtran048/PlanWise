#imports
import flet as ft
from datetime import date, time
from functions import *

def main(page: ft.Page):
    #creates starting size for window
    page.window.width, page.window.height = get_screen_size() 
    
    #get today's date
    today = date.today()

    task_creation = None

    #close task creation menu
    def close_creation_menu():
        nonlocal task_creation
        page.overlay.remove(task_creation)

    #creates task creation menu
    def create_task_menu(task = ["", today, time(12, 0), "",[False] * 7]):
        nonlocal task_creation
        page.overlay.append(
            task_creation := ft.SafeArea(
                content = ft.Container(
                    alignment = ft.Alignment.CENTER,
                    content = ft.Container(
                        padding = 20,
                        border_radius = 10,
                        bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        content = ft.Column(
                            tight = True,
                            spacing = 15,
                            controls = [
                                ft.Row(
                                    tight = True,
                                    spacing = 10,
                                    controls = [
                                        name := ft.TextField(
                                            hint_text = "Task name", 
                                            value = task[0],
                                            width = 220
                                        ),
                                        ft.IconButton(
                                            icon = ft.Icons.CLOSE,
                                            on_click = close_creation_menu
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    tight = True,
                                    spacing = 10,
                                    controls = [
                                        ft.Button(
                                            content = ft.Text(value=task[1].strftime(" %B %d %Y")),
                                            on_click = lambda e: page.show_dialog(date_selector(task[1], e.control, task))
                                        ),
                                        ft.Button(
                                            content = ft.Text(value=task[2].strftime("%H:%M")),
                                            on_click = lambda e: page.show_dialog(time_selector(task[2], e.control, task))
                                        )
                                    ]
                                ),
                                ft.Row(
                                    tight = True,
                                    spacing = 10,
                                    controls = [
                                        ft.Text(value = " Remind me"),
                                        repeated := ft.Dropdown(                     
                                            width = 170,
                                            value = task[3],                    
                                            options = [
                                                ft.DropdownOption(key = "on_day", text = "On Day"),
                                                ft.DropdownOption(key = "week_before", text = "Week Before")       
                                            ]
                                        ) 
                                    ]
                                ),
                                ft.Text(" Repeating"),
                                week_row := ft.Row(
                                    tight = True,
                                    spacing = 0,
                                    controls = week_day_buttons(task[4])
                                ),
                                ft.Button(
                                    content = "Save",
                                    on_click = lambda e: save_task(task, name.value, repeated.value, week_row)
                                ),
                            ]
                        )
                    )
                )
            )
        )
       
    #creates top row
    page.add(
        ft.SafeArea(
            content = ft.Container(
                content = ft.Row(
                    controls = [
                        ft.Text(
                            value = today.strftime(" %B %d"),
                            size = 35
                        ),
                        ft.IconButton(
                            icon = ft.Icons.ADD,
                            icon_size = 35,
                            style = ft.ButtonStyle(shape=ft.CircleBorder()),
                            on_click = lambda e: create_task_menu()
                        ),
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
        ),
    )

#runs program
if __name__ == "__main__":
    ft.run(main)
