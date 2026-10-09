import flet as ft
import datetime
import tkinter as tk

def main(page: ft.Page):
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    page.window.width = screen_width * .3 
    page.window.height = screen_height * .8
    page.update()
    
    
    today = datetime.date.today()
    
    
    
    top_row = ft.Row(
        controls=[
            ft.Text(value=today.strftime("%B %d"), size=50, font_family="Consolas"),
            ft.Button(ft.Text(value="+", size=30),style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=20)) 
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    
    
    
    
    page.add(top_row)
        
      
        
            


if __name__ == "__main__":
    ft.run(main)
