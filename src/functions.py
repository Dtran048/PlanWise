import flet as ft
import tkinter as tk
import json
import os

#get screen size and calculate starting window size
def get_screen_size():
    root = tk.Tk()
    width = root.winfo_screenwidth() * .3 
    height = root.winfo_screenheight() * .8
    root.destroy()
    return(width, height)

#close task creation menu
def close_creation_menu(page, task):
    page.overlay.remove(task)

#date picker
def date_selector(date,button, task):
    def date_change(e: ft.Event[ft.DatePicker]):
        task[1] = e.control.value
        button.content.value = task[1].strftime("%B %d %Y")

    return ft.DatePicker(
        first_date = date,
        current_date = date,
        on_change = date_change
    )

#time picker
def time_selector(time,button, task):
    def time_change(e: ft.Event[ft.TimePicker]):
        task[2] = e.control.value
        button.content.value = task[2].strftime("%I:%M %p")
    
    return ft.TimePicker(
        value = time,
        entry_mode = ft.TimePickerEntryMode.DIAL,
        on_change = time_change
    )

#toggles day buttons
def day_selection(e):
    button = e.control
    button.data = not button.data
    button.bgcolor = ft.Colors.BLUE if button.data else ft.Colors.BLACK

#create a button for each day of the week
def create_day_buttons(day,selected):
    return ft.Button(
        width = 35,
        content = day,
        style = ft.ButtonStyle(
            shape = ft.CircleBorder(),
            padding = 0,
            visual_density = ft.VisualDensity.COMPACT
            ),
        data = selected,
        bgcolor = ft.Colors.BLUE if selected else ft.Colors.BLACK,
        on_click = day_selection
    )

#list for weekdays
weekdays = ["S","M","T", "W", "T", "F", "S"]

#create buttons for each day of the week
def week_day_buttons(week):
    return[create_day_buttons(day, selected) for day, selected in zip(weekdays, week)]

#saves user inputted data
def save_task(task, name, repeated, week_row):
    task = [
        name,
        task[1], 
        task[2], 
        repeated, 
        [button.data for button in week_row.controls]
    ]
    str_tasks = [str(item) for item in task]
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
    with open(json_path, "a", encoding="utf-8") as json_file:
        json.dump(str_tasks, json_file, indent=4)

# updates an existing task in tasks.json by index
def update_task(task_index, task, name, repeated, week_row):
    updated_task = [
        name,
        task[1],
        task[2],
        repeated,
        [button.data for button in week_row.controls]
    ]
    str_task = [str(item) for item in updated_task]
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

    all_tasks = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = f.read().strip()

        decoder = json.JSONDecoder()
        idx = 0
        while idx < len(raw_data):
            while idx < len(raw_data) and raw_data[idx].isspace():
                idx += 1
            if idx >= len(raw_data):
                break
            try:
                item, next_idx = decoder.raw_decode(raw_data, idx)
                idx = next_idx
                all_tasks.append(item)
            except json.JSONDecodeError:
                break

    if 0 <= task_index < len(all_tasks):
        all_tasks[task_index] = str_task

    with open(json_path, "w", encoding="utf-8") as json_file:
        for item in all_tasks:
            json.dump(item, json_file, indent=4)

# deletes a task from tasks.json by index
def delete_task(task_index):
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

    all_tasks = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = f.read().strip()

        decoder = json.JSONDecoder()
        idx = 0
        while idx < len(raw_data):
            while idx < len(raw_data) and raw_data[idx].isspace():
                idx += 1
            if idx >= len(raw_data):
                break
            try:
                item, next_idx = decoder.raw_decode(raw_data, idx)
                idx = next_idx
                all_tasks.append(item)
            except json.JSONDecodeError:
                break

    if 0 <= task_index < len(all_tasks):
        all_tasks.pop(task_index)

    with open(json_path, "w", encoding="utf-8") as json_file:
        for item in all_tasks:
            json.dump(item, json_file, indent=4)