import flet as ft
import tkinter as tk

#get screen size and calculate starting window size
def get_screen_size():
    root = tk.Tk()
    width = root.winfo_screenwidth() * .3 
    height = root.winfo_screenheight() * .8
    root.destroy()
    return(width, height)

#date picker
def date_selector(date,button):
    def date_change(e: ft.Event[ft.DatePicker]):
        selected_date = e.control.value
        button.content.value = selected_date.strftime("%B %d %Y")

    return ft.DatePicker(
        first_date = date,
        current_date = date,
        on_change = date_change
    )

#time picker
def time_selector(time,button):
    def time_change(e: ft.Event[ft.TimePicker]):
        selected_time = e.control.value
        button.content.value = selected_time.strftime("%I:%M %p")
    
    return ft.TimePicker(
        value = time,
        entry_mode = ft.TimePickerEntryMode.DIAL,
        on_change = time_change
    )

def day_selection(e):
    button = e.control
    button.data = not button.data
    button.bgcolor = ft.Colors.BLUE if button.data else ft.Colors.BLACK


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


