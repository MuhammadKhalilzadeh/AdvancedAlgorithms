import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from weather_data import WEATHER_DATA, MONTHLY_WEATHER
from themes import get_theme_colors, get_weather_theme
from PIL import Image, ImageTk
import os

WEATHER_ICONS = {
    "☀️": "sunny.png",
    "⛅": "cloudy.png",
    "☁️": "cloudy.png",
    "🌧️": "rainy.png",
    "⛈️": "stormy.png",
    "🌨️": "snowy.png",
    "🌫️": "foggy.png",
    "🌙": "cloudy.png",
}

def create_weather_icons():
    icons_dir = os.path.join("assets", "icons")
    os.makedirs(icons_dir, exist_ok=True)
    
    def create_icon(name, color):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([12, 12, 52, 52], fill=color)
        img.save(os.path.join(icons_dir, f"{name}.png"))
    
    create_icon("sunny", "#FFD700")
    create_icon("partly-cloudy", "#E2E8F0")
    create_icon("cloudy", "#CBD5E1")
    create_icon("rainy", "#3B82F6")
    create_icon("stormy", "#475569")
    create_icon("snowy", "#94A3B8")
    create_icon("foggy", "#E2E8F0")

def load_weather_icon(weather_icon, theme="light"):
    icon_name = WEATHER_ICONS.get(weather_icon, "sunny.png")
    icon_path = os.path.join("assets", "images", icon_name)
    if not os.path.exists(icon_path):
        icon_path = os.path.join("assets", "images", "sunny.png")
    if not os.path.exists(icon_path):
        from PIL import ImageDraw
        img = Image.new('RGBA', (64, 64), (200, 200, 200, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse([8, 8, 56, 56], fill=(255, 215, 0, 255))
        return ImageTk.PhotoImage(img)
    img = Image.open(icon_path)
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_glass_frame(parent, theme="light", app_state=None, **kwargs):
    colors = get_theme_colors(theme)
    frame = tk.Frame(parent,
                    bg=colors["bg"],
                    highlightbackground=colors["glass_border"],
                    highlightthickness=1,
                    **kwargs)
    
    frame.configure(relief="flat")
    frame.bind("<Map>", lambda e: frame.configure(relief="flat"))
    
    def on_enter(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_state["current_theme"]
            colors = get_theme_colors(current_theme)
            frame.configure(bg=colors["button_hover"])
            frame.configure(highlightbackground=colors["accent"])
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=colors["accent"])
    
    def on_leave(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_state["current_theme"]
            colors = get_theme_colors(current_theme)
            frame.configure(bg=colors["bg"])
            frame.configure(highlightbackground=colors["glass_border"])
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=colors["text"])
    
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    
    return frame

def get_weather_for_date(date):
    day_index = date.day - 1
    weather_type = MONTHLY_WEATHER[day_index]
    return WEATHER_DATA[weather_type]

def create_weather_tile(parent, date, column, theme="light", app_state=None):
    colors = get_theme_colors(theme)
    frame = create_glass_frame(parent, theme=theme, app_state=app_state, padx=20, pady=20)
    frame.grid(row=0, column=column, padx=20, pady=20, sticky="nsew")

    date_label = ttk.Label(
        frame,
        text=date.strftime("%a\n%d %b"),
        style="Date.TLabel",
        anchor="center",
        font=("Segoe UI", 13, "bold")
    )
    date_label.pack(pady=(5, 10))

    weather = get_weather_for_date(date)

    icon_image = load_weather_icon(weather["icon"], theme)
    icon_container = tk.Label(
        frame,
        image=icon_image,
        bg=colors["glass_bg"],
        bd=0,
        highlightthickness=0
    )
    icon_container.image = icon_image
    icon_container.pack(pady=(0, 10))

    desc_label = ttk.Label(
        frame,
        text=weather["description"],
        style="Modern.TLabel",
        anchor="center",
        font=("Segoe UI", 11, "bold")
    )
    desc_label.pack(pady=(0, 8))

    temp_frame = ttk.Frame(frame, style="Modern.TFrame")
    temp_frame.pack(pady=(0, 5))

    min_temp = ttk.Label(temp_frame, text=f"Min: {weather['temp_range']['min']}°C", style="Temp.TLabel", font=("Segoe UI", 10))
    avg_temp = ttk.Label(temp_frame, text=f"Avg: {weather['temp_range']['avg']}°C", style="Temp.TLabel", font=("Segoe UI", 10, "bold"))
    max_temp = ttk.Label(temp_frame, text=f"Max: {weather['temp_range']['max']}°C", style="Temp.TLabel", font=("Segoe UI", 10))

    min_temp.pack(pady=1)
    avg_temp.pack(pady=1)
    max_temp.pack(pady=1)

    def on_tile_click(event):
        theme = get_weather_theme(weather["description"])
        app_state["change_theme"](theme)

    frame.bind("<Button-1>", on_tile_click)
    for child in frame.winfo_children():
        child.bind("<Button-1>", on_tile_click)

    return frame

def create_weather_section(container, app_state):
    weather_container = ttk.Frame(container, style="Modern.TFrame")
    weather_container.pack(fill="x", padx=20, pady=(20, 10))
    
    weather_title = ttk.Label(
        weather_container,
        text="Weather Forecast",
        style="Title.TLabel",
        font=("Segoe UI", 16, "bold")
    )
    weather_title.pack(anchor="w", pady=(0, 10))
    
    weather_content = ttk.Frame(weather_container, style="Modern.TFrame")
    weather_content.pack(fill="x", expand=True)
    
    app_state["canvas"] = tk.Canvas(weather_content, 
                                  bg=app_state["colors"]["bg"],
                                  highlightthickness=0,
                                  height=400)
    app_state["canvas"].pack(side="left", fill="x", expand=True)
    
    app_state["scrollable_frame"] = ttk.Frame(app_state["canvas"], style="Modern.TFrame")
    app_state["scrollable_frame"].bind("<Configure>",
        lambda e: app_state["canvas"].configure(scrollregion=app_state["canvas"].bbox("all")))
    
    app_state["canvas"].create_window((0, 0),
                                    window=app_state["scrollable_frame"],
                                    anchor="nw")
    
    app_state["scrollable_frame"].grid_columnconfigure(tuple(range(7)), weight=1)
    app_state["scrollable_frame"].grid_rowconfigure(0, weight=1)
    
    create_initial_tiles(app_state)
    
    see_more_container = ttk.Frame(weather_content, style="Modern.TFrame")
    see_more_container.pack(side="right", padx=(10, 0))
    create_see_more_button(see_more_container, app_state)

def create_initial_tiles(app_state):
    for i in range(7):
        date = app_state["current_date"] + timedelta(days=i)
        create_weather_tile(app_state["scrollable_frame"], date, i, theme=app_state["current_theme"], app_state=app_state)

def create_see_more_button(parent, app_state):
    button_frame = create_glass_frame(parent, theme=app_state["current_theme"], app_state=app_state, padx=15, pady=15)
    button_frame.pack(side="right", padx=15, pady=15)
    
    see_more = ttk.Button(button_frame,
                         text=f"See {app_state['remaining_days']} More Days →",
                         style="Modern.TButton",
                         command=lambda: show_remaining_days(app_state))
    see_more.pack(expand=True, fill="both", padx=10, pady=10)
    app_state["see_more"] = see_more

def show_remaining_days(app_state):
    app_state["scrollable_frame"].grid_columnconfigure(tuple(range(app_state["days_in_month"])), weight=1)
    
    for i in range(7, app_state["days_in_month"]):
        date = app_state["current_date"] + timedelta(days=i)
        create_weather_tile(app_state["scrollable_frame"], date, i, theme=app_state["current_theme"], app_state=app_state)
    
    app_state["see_more"].configure(text="All Days Shown")
    app_state["see_more"].configure(state="disabled")