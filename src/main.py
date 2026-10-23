import flet as ft
import datetime 
from datetime import time
import tkinter as tk

def main(page: ft.Page):
    #get screen size
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    #calculate window size
    page.window.width = screen_width * .3 
    page.window.height = screen_height * .8
    page.update()
    
    #get today's date
    today = datetime.date.today()

    #create item
    def create_item(e):
        item_creation.visible = not item_creation.visible
        item_creation.update()

    #to do list item creation
    item_name = ft.TextField(hint_text = "Item Name", width=screen_width * .125)
    item_date = datetime.date.today()
    date_text = ft.Text(value=item_date.strftime(" %B %d %Y"))
    item_time = time(12, 0)
    time_text = ft.Text(value=item_time.strftime("%H:%M"))

    #updates date
    def date_change(e: ft.Event[ft.DatePicker]):
        item_date = e.control.value
        date_text.value = item_date.strftime(" %B %d %Y")
        date_text.update()      

    #date picker
    Date_picker = ft.DatePicker(
        first_date=datetime.date.today(),
        current_date=today,
        on_change=date_change
    )

    #updates time
    def time_change(e: ft.Event[ft.TimePicker]):
        item_time = e.control.value
        time_text.value = item_time.strftime(" %H %M")
        time_text.update()   
    
    #time picker
    Time_picker = ft.TimePicker(
        value=time(hour=12, minute=00),
        entry_mode=ft.TimePickerEntryMode.DIAL,
        on_change=time_change
    )

    #function for when button is clicked
    def day_selection(e: ft.Event[ft.Button]):
        e.control.data =  not e.control.data
        if e.control.data:
            e.control.bgcolor = ft.Colors.BLUE
        else:
            e.control.bgcolor = ft.Colors.BLACK
        e.control.update()

    #list for weekdays
    weekdays = ["S","M","T", "W", "T", "F", "S"]

    #button template for weekdays
    def create_week_buttons(day):
        return ft.Button(
            width=35,
            content=day,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=0,visual_density=ft.VisualDensity.COMPACT
                ),
            data= False,
            bgcolor = ft.Colors.BLACK,
            on_click=day_selection,
        )

    #loop to create buttons
    day_buttons = [
        create_week_buttons(day) for day in weekdays
    ]

    #create overlay for item creation
    page.overlay.append(
        item_creation := ft.SafeArea(
            visible=False,
            content=ft.Container(
                alignment=ft.Alignment.CENTER,
                content=ft.Container(
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    content=ft.Column(
                        tight=True,
                        spacing=10,
                        controls=[
                            item_name,
                            ft.Row(
                                tight=True,
                                spacing=10,
                                controls=[
                                    ft.Button(
                                        content = date_text,
                                        on_click=lambda _: page.show_dialog(Date_picker)
                                    ),
                                    ft.Button(
                                        content = time_text,
                                        on_click=lambda _: page.show_dialog(Time_picker)
                                    )
                                ]
                            ),
                            ft.Row(
                                tight=True,
                                spacing=10,
                                controls=[
                                    ft.Text(
                                        value=" Remind me",
                                    ),
                                    ft.Dropdown(
                                        width=170,
                                        value="",
                                        options=[
                                            ft.DropdownOption(key="on_day", text="On Day"),
                                            ft.DropdownOption(key="week_before", text="Week Before"),
                                        ]
                                    ) 
                                ]
                            ),
                            ft.Text(" Repeating"),
                            ft.Row(
                                tight=True,
                                spacing=0,
                                controls=day_buttons
                            )
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
                content=ft.Row(
                    controls=[
                        ft.Text(
                            value=today.strftime(" %B %d"),
                            size=35
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            icon_size=35,
                            style=ft.ButtonStyle(shape=ft.CircleBorder()),
                            on_click=create_item
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)

