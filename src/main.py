#imports
import flet as ft
import os
import winreg
import sys
import json
import ast
from datetime import date, time, datetime
from functions import *

def main(page: ft.Page):
    #creates starting size for window
    page.window.width, page.window.height = get_screen_size()
    page.window.frameless = True
    
    #get today's date
    today = date.today()

    # Scrollable task container so the bottom resize handle stays anchored
    tasks_view = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=8)

    def format_time(time_str):
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                return datetime.strptime(str(time_str), fmt).strftime("%I:%M %p").lstrip("0")
            except ValueError:
                continue
        return str(time_str)

    def parse_task_for_menu(raw_task):
        task_name = str(raw_task[0]) if len(raw_task) > 0 else ""

        task_date = today
        if len(raw_task) > 1 and raw_task[1]:
            date_str = str(raw_task[1]).strip().split(" ")[0]
            try:
                task_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                task_date = today

        task_time = time(12, 0)
        if len(raw_task) > 2 and raw_task[2]:
            for fmt in ("%H:%M:%S", "%H:%M"):
                try:
                    task_time = datetime.strptime(str(raw_task[2]).strip(), fmt).time()
                    break
                except ValueError:
                    continue

        task_remind = str(raw_task[3]) if len(raw_task) > 3 and raw_task[3] not in (None, "None") else ""

        task_week = [False] * 7
        if len(raw_task) > 4:
            if isinstance(raw_task[4], list) and len(raw_task[4]) == 7:
                task_week = [bool(x) for x in raw_task[4]]
            elif isinstance(raw_task[4], str):
                try:
                    parsed = ast.literal_eval(raw_task[4])
                    if isinstance(parsed, list) and len(parsed) == 7:
                        task_week = [bool(x) for x in parsed]
                except (ValueError, SyntaxError):
                    pass

        return [task_name, task_date, task_time, task_remind, task_week]

    def create_task_card(task, task_index):
        task_name = str(task[0])
        task_time = format_time(task[2]) if len(task) > 2 else ""

        def handle_delete(e):
            delete_task(task_index)
            load_tasks()

        return ft.Container(
            padding=10,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=6,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10,
                        expand=True,
                        controls=[
                            ft.Checkbox(),
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        value=task_name,
                                        size=16,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Text(
                                        value=task_time,
                                        size=12,
                                        color=ft.Colors.ON_SURFACE_VARIANT,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                content="Reschedule task",
                                on_click=lambda e: create_task_menu(
                                    parse_task_for_menu(task),
                                    task_index,
                                ),
                            ),
                            ft.PopupMenuItem(
                                content = "Delete Task",
                                on_click = handle_delete
                            ),                   
                        ],
                    ),
                ],
            ),
        )
    def load_tasks():
        tasks_view.controls.clear()
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
        
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                raw_data = f.read().strip()

            if raw_data:
                decoder = json.JSONDecoder()
                idx = 0
                task_index = 0
                while idx < len(raw_data):
                    while idx < len(raw_data) and raw_data[idx].isspace():
                        idx += 1
                    if idx >= len(raw_data):
                        break
                    try:
                        task, next_idx = decoder.raw_decode(raw_data, idx)
                        idx = next_idx
                        if isinstance(task, list) and len(task) > 0:
                            tasks_view.controls.append(create_task_card(task, task_index))
                            task_index+=1
                    except json.JSONDecodeError as e:
                        print(f"Error decoding task at index {idx}: {e}")
                        break
        page.update()

    task_creation = None

    #creates task creation menu
    def create_task_menu(task = None, task_index = None):
        nonlocal task_creation
        if task is None:
            task = ["", today, time(12, 0), "",[False] * 7]

        def handle_save(e):
            if task_index is not None:
                update_task(task_index, task, name.value, repeated.value, week_row)
            else:
                save_task(task, name.value, repeated.value, week_row)
            close_creation_menu(page, task_creation)
            load_tasks()

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
                                            on_click = lambda e: close_creation_menu(page, task_creation)
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
                                    on_click = handle_save
                                ),
                            ]
                        )
                    )
                )
            )
        )
        page.update()

    # Bottom-right resize handle for frameless window
    def on_resize(e: ft.DragUpdateEvent):
        page.window.width = max(250, page.window.width + e.local_delta.x)
        page.window.height = max(300, page.window.height + e.local_delta.y)
        page.update()

    resize_handle = ft.Row(
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.RESIZE_DOWN_RIGHT,
                on_pan_update=on_resize,
                content=ft.Icon(ft.Icons.DRAG_HANDLE, size=18, color=ft.Colors.OUTLINE),
            )
        ],
    )
       
    #adds top row, scrollable task view, and resize handle to the screen
    page.add(
        ft.SafeArea(
            content = ft.WindowDragArea(
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
            )
        ),
        tasks_view,
        resize_handle
    )

    #calls the loader when the app starts
    load_tasks()

#this auto starts the program
def enable_auto_start():
    if os.name == 'nt':
        app_name = "PlanWise"
        script_path = os.path.abspath(sys.argv[0])
        run_command = f'"{sys.executable}" "{script_path}"'
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, run_command)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Startup failed: {e}")

#runs program
if __name__ == "__main__":
    enable_auto_start()
    ft.run(main)