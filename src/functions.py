import flet as ft
import tkinter as tk
import json

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
    with open("tasks.json", "a") as json_file:
        json.dump(str_tasks, json_file, indent=4)