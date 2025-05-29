import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar
from themes import get_theme_colors
from weather_section import create_weather_section
from news_section import create_news_section
from styles import apply_modern_style

def create_menu(root, app_state):
    menubar = tk.Menu(root, bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
    root.config(menu=menubar)
    
    theme_menu = tk.Menu(menubar, tearoff=0, bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
    menubar.add_cascade(label="Theme", menu=theme_menu)
    
    theme_menu.add_command(label="Light", command=lambda: change_theme("light", app_state))
    theme_menu.add_command(label="Dark", command=lambda: change_theme("dark", app_state))
    
    theme_menu.add_separator()
    theme_menu.add_command(label="Exit", command=root.quit)

def change_theme(theme, app_state):
    if theme == app_state["current_theme"]:
        return

    app_state["current_theme"] = theme
    app_state["colors"] = get_theme_colors(theme)
    
    app_state["root"].configure(bg=app_state["colors"]["bg"])
    
    for widget in app_state["main_container"].winfo_children():
        if isinstance(widget, ttk.Frame):
            widget.configure(style="Modern.TFrame")
            for child in widget.winfo_children():
                if isinstance(child, ttk.Frame):
                    child.configure(style="Modern.TFrame")
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, (tk.Frame, ttk.Frame)):
                            grandchild.configure(style="Modern.TFrame")
    
    app_state["canvas"].configure(bg=app_state["colors"]["bg"])
    
    for menu in app_state["root"].winfo_children():
        if isinstance(menu, tk.Menu):
            menu.configure(bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
            for submenu in menu.winfo_children():
                if isinstance(submenu, tk.Menu):
                    submenu.configure(bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
    
    apply_modern_style(app_state)
    
    for widget in app_state["scrollable_frame"].winfo_children():
        if isinstance(widget, tk.Frame):
            widget.configure(bg=app_state["colors"]["bg"],
                           highlightbackground=app_state["colors"]["glass_border"])
            
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=app_state["colors"]["bg"],
                                  fg=app_state["colors"]["text"])
                elif isinstance(child, ttk.Label):
                    child.configure(style="Modern.TLabel")
                elif isinstance(child, ttk.Frame):
                    child.configure(style="Modern.TFrame")
                    for temp_label in child.winfo_children():
                        if isinstance(temp_label, ttk.Label):
                            temp_label.configure(style="Temp.TLabel")

def on_mousewheel(event, canvas):
    canvas.xview_scroll(int(-1*(event.delta/120)), "units")

def init_app():
    root = tk.Tk()
    root.title("Weather & News Dashboard")
    
    app_state = {
        "root": root,
        "current_theme": "light",
        "colors": get_theme_colors("light"),
        "current_date": datetime.now(),
        "days_in_month": calendar.monthrange(datetime.now().year, datetime.now().month)[1],
        "remaining_days": calendar.monthrange(datetime.now().year, datetime.now().month)[1] - datetime.now().day + 1,
        "change_theme": lambda theme: change_theme(theme, app_state)
    }
    
    root.configure(bg=app_state["colors"]["bg"])
    
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    create_menu(root, app_state)
    apply_modern_style(app_state)
    
    app_state["main_container"] = ttk.Frame(root, style="Modern.TFrame")
    app_state["main_container"].pack(fill="both", expand=True)
    
    create_weather_section(app_state["main_container"], app_state)
    create_news_section(app_state["main_container"], app_state)
    
    app_state["canvas"].bind_all("<MouseWheel>", lambda e: on_mousewheel(e, app_state["canvas"]))
    
    return root

def main():
    root = init_app()
    root.mainloop()

if __name__ == "__main__":
    main()