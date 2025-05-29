import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from weather_data import WEATHER_DATA, MONTHLY_WEATHER
import calendar
from PIL import Image, ImageTk
import os
from themes import THEMES, WEATHER_THEMES, get_theme_colors, get_weather_theme

# Weather icon mapping (now using images directory)
WEATHER_ICONS = {
    "☀️": "sunny.png",
    "⛅": "cloudy.png",      # Use cloudy for partly cloudy
    "☁️": "cloudy.png",
    "🌧️": "rainy.png",
    "⛈️": "stormy.png",
    "🌨️": "snowy.png",
    "🌫️": "foggy.png",
    "🌙": "cloudy.png",     # Use cloudy for night as placeholder
}

def create_weather_icons():
    """Create weather icons if they don't exist"""
    icons_dir = os.path.join("assets", "icons")
    os.makedirs(icons_dir, exist_ok=True)
    
    # Create a simple weather icon
    def create_icon(name, color):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        # Draw a simple circle for the icon
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([12, 12, 52, 52], fill=color)
        img.save(os.path.join(icons_dir, f"{name}.png"))
    
    # Create icons for each weather type
    create_icon("sunny", "#FFD700")  # Gold
    create_icon("partly-cloudy", "#E2E8F0")  # Light gray
    create_icon("cloudy", "#CBD5E1")  # Gray
    create_icon("rainy", "#3B82F6")  # Blue
    create_icon("stormy", "#475569")  # Dark gray
    create_icon("snowy", "#94A3B8")  # Light blue
    create_icon("foggy", "#E2E8F0")  # Light gray

def load_weather_icon(weather_icon, theme="light"):
    """Load and resize weather icon, fallback to a generated placeholder if missing"""
    icon_name = WEATHER_ICONS.get(weather_icon, "sunny.png")
    icon_path = os.path.join("assets", "images", icon_name)
    if not os.path.exists(icon_path):
        # Fallback to sunny.png if the specific icon is missing
        icon_path = os.path.join("assets", "images", "sunny.png")
    if not os.path.exists(icon_path):
        # If even sunny.png is missing, create a placeholder image in memory
        from PIL import ImageDraw
        img = Image.new('RGBA', (64, 64), (200, 200, 200, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse([8, 8, 56, 56], fill=(255, 215, 0, 255))  # yellow circle
        return ImageTk.PhotoImage(img)
    img = Image.open(icon_path)
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def create_glass_frame(parent, theme="light", app_state=None, **kwargs):
    """Create a frame with enhanced glass-morphic effect"""
    colors = get_theme_colors(theme)
    frame = tk.Frame(parent,
                    bg=colors["glass_bg"],
                    highlightbackground=colors["glass_border"],
                    highlightthickness=1,
                    **kwargs)
    
    # Add shadow effect
    frame.configure(relief="flat")
    frame.bind("<Map>", lambda e: frame.configure(relief="flat"))
    
    # Add hover effect
    def on_enter(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_state["current_theme"]
            colors = get_theme_colors(current_theme)
            frame.configure(bg=colors["button_hover"])
            frame.configure(highlightbackground=colors["accent"])
            # Add a subtle glow effect
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=colors["accent"])
    
    def on_leave(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_state["current_theme"]
            colors = get_theme_colors(current_theme)
            frame.configure(bg=colors["glass_bg"])
            frame.configure(highlightbackground=colors["glass_border"])
            # Restore original colors
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=colors["text"])
    
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    
    return frame

def get_weather_for_date(date):
    """Get weather data for a specific date from our static data"""
    day_index = date.day - 1
    weather_type = MONTHLY_WEATHER[day_index]
    return WEATHER_DATA[weather_type]

def create_weather_tile(parent, date, column, theme="light", app_state=None):
    """Create a single weather tile with modern styling and improved image presentation"""
    colors = get_theme_colors(theme)
    frame = create_glass_frame(parent, theme=theme, app_state=app_state, padx=20, pady=20)
    frame.grid(row=0, column=column, padx=20, pady=20, sticky="nsew")

    # Add date label with accent color
    date_label = ttk.Label(
        frame,
        text=date.strftime("%a\n%d %b"),
        style="Date.TLabel",
        anchor="center",
        font=("Segoe UI", 13, "bold")
    )
    date_label.pack(pady=(5, 10))

    # Get weather data
    weather = get_weather_for_date(date)

    # Add weather image (centered, with a subtle border/shadow)
    icon_image = load_weather_icon(weather["icon"], theme)
    icon_container = tk.Label(
        frame,
        image=icon_image,
        bg=colors["glass_bg"],
        bd=0,
        highlightthickness=0
    )
    icon_container.image = icon_image  # Keep a reference
    icon_container.pack(pady=(0, 10))

    # Add weather description (centered, modern font)
    desc_label = ttk.Label(
        frame,
        text=weather["description"],
        style="Modern.TLabel",
        anchor="center",
        font=("Segoe UI", 11, "bold")
    )
    desc_label.pack(pady=(0, 8))

    # Add temperature labels with modern styling and spacing
    temp_frame = ttk.Frame(frame, style="Modern.TFrame")
    temp_frame.pack(pady=(0, 5))

    min_temp = ttk.Label(temp_frame, text=f"Min: {weather['temp_range']['min']}°C", style="Temp.TLabel", font=("Segoe UI", 10))
    avg_temp = ttk.Label(temp_frame, text=f"Avg: {weather['temp_range']['avg']}°C", style="Temp.TLabel", font=("Segoe UI", 10, "bold"))
    max_temp = ttk.Label(temp_frame, text=f"Max: {weather['temp_range']['max']}°C", style="Temp.TLabel", font=("Segoe UI", 10))

    min_temp.pack(pady=1)
    avg_temp.pack(pady=1)
    max_temp.pack(pady=1)

    # Add click event to change theme
    def on_tile_click(event):
        theme = get_weather_theme(weather["description"])
        change_theme(theme, app_state)

    frame.bind("<Button-1>", on_tile_click)
    # Also bind to all child widgets to ensure the click event is captured
    for child in frame.winfo_children():
        child.bind("<Button-1>", on_tile_click)

    return frame

def apply_modern_style(app_state):
    """Apply modern styling to the application"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles with glass-morphic effects
    style.configure("Modern.TFrame",
                   background=app_state["colors"]["glass_bg"],
                   relief="flat",
                   borderwidth=0)
    
    style.configure("Modern.TLabel",
                   background=app_state["colors"]["glass_bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 10))
    
    style.configure("Date.TLabel",
                   background=app_state["colors"]["glass_bg"],
                   foreground=app_state["colors"]["accent"],
                   font=("Segoe UI", 12, "bold"))
    
    style.configure("Temp.TLabel",
                   background=app_state["colors"]["glass_bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 9))
    
    style.configure("Modern.TButton",
                   background=app_state["colors"]["glass_bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 10),
                   padding=10,
                   relief="flat",
                   borderwidth=0)
    
    style.map("Modern.TButton",
              background=[("active", app_state["colors"]["button_hover"])],
              foreground=[("active", app_state["colors"]["accent"])])

def create_menu(root, app_state):
    """Create the menu bar"""
    menubar = tk.Menu(root, bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
    root.config(menu=menubar)
    
    # Theme menu
    theme_menu = tk.Menu(menubar, tearoff=0, bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
    menubar.add_cascade(label="Theme", menu=theme_menu)
    
    # Add theme options
    theme_menu.add_command(label="Light", command=lambda: change_theme("light", app_state))
    theme_menu.add_command(label="Dark", command=lambda: change_theme("dark", app_state))
    
    # Add separator
    theme_menu.add_separator()
    
    # Add exit option
    theme_menu.add_command(label="Exit", command=root.quit)

def change_theme(theme, app_state):
    """Change the application theme with smooth transition"""
    if theme == app_state["current_theme"]:
        return

    app_state["current_theme"] = theme
    app_state["colors"] = get_theme_colors(theme)
    
    # Update root window with smooth transition
    app_state["root"].configure(bg=app_state["colors"]["bg"])
    
    # Update canvas with smooth transition
    app_state["canvas"].configure(bg=app_state["colors"]["bg"])
    
    # Update menu colors
    for menu in app_state["root"].winfo_children():
        if isinstance(menu, tk.Menu):
            menu.configure(bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
            for submenu in menu.winfo_children():
                if isinstance(submenu, tk.Menu):
                    submenu.configure(bg=app_state["colors"]["menu_bg"], fg=app_state["colors"]["menu_fg"])
    
    # Reapply styles
    apply_modern_style(app_state)
    
    # Update all tiles with smooth transition
    for widget in app_state["scrollable_frame"].winfo_children():
        if isinstance(widget, tk.Frame):
            # Reset hover state
            widget.configure(bg=app_state["colors"]["glass_bg"],
                           highlightbackground=app_state["colors"]["glass_border"])
            
            # Update all child widgets
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=app_state["colors"]["glass_bg"],
                                  fg=app_state["colors"]["text"])
                elif isinstance(child, ttk.Label):
                    child.configure(style="Modern.TLabel")
                elif isinstance(child, ttk.Frame):
                    child.configure(style="Modern.TFrame")
                    # Update temperature labels
                    for temp_label in child.winfo_children():
                        if isinstance(temp_label, ttk.Label):
                            temp_label.configure(style="Temp.TLabel")
    
    # Update see more button
    for widget in app_state["main_container"].winfo_children():
        if isinstance(widget, tk.Frame):
            # Reset hover state
            widget.configure(bg=app_state["colors"]["glass_bg"],
                           highlightbackground=app_state["colors"]["glass_border"])
            
            # Update button
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button):
                    child.configure(style="Modern.TButton")

def on_mousewheel(event, canvas):
    """Handle mouse wheel scrolling"""
    canvas.xview_scroll(int(-1*(event.delta/120)), "units")

def create_initial_tiles(app_state):
    """Create initial 7 weather tiles"""
    for i in range(7):
        date = app_state["current_date"] + timedelta(days=i)
        create_weather_tile(app_state["scrollable_frame"], date, i, theme=app_state["current_theme"], app_state=app_state)

def create_see_more_button(app_state):
    """Create see more button with glass-morphic effect"""
    # Create a frame that matches the height of weather tiles
    button_frame = create_glass_frame(app_state["main_container"], theme=app_state["current_theme"], app_state=app_state, padx=15, pady=15)
    button_frame.pack(side="right", padx=15, pady=15)
    
    # Create the button
    see_more = ttk.Button(button_frame,
                          text=f"See {app_state['remaining_days']} More Days →",
                          style="Modern.TButton",
                          command=lambda: show_remaining_days(app_state))
    see_more.pack(expand=True, fill="both", padx=10, pady=10)
    app_state["see_more"] = see_more

def show_remaining_days(app_state):
    """Show all remaining days of the month"""
    # Configure grid for all days
    app_state["scrollable_frame"].grid_columnconfigure(tuple(range(app_state["days_in_month"])), weight=1)
    
    # Create tiles for remaining days
    for i in range(7, app_state["days_in_month"]):
        date = app_state["current_date"] + timedelta(days=i)
        create_weather_tile(app_state["scrollable_frame"], date, i, theme=app_state["current_theme"], app_state=app_state)
    
    # Update button text
    app_state["see_more"].configure(text="All Days Shown")
    app_state["see_more"].configure(state="disabled")

def init_app():
    root = tk.Tk()
    root.title("Monthly Weather Forecast")
    
    app_state = {
        "root": root,
        "current_theme": "light",
        "colors": get_theme_colors("light"),
        "current_date": datetime.now(),
        "days_in_month": calendar.monthrange(datetime.now().year, datetime.now().month)[1],
        "remaining_days": calendar.monthrange(datetime.now().year, datetime.now().month)[1] - datetime.now().day + 1
    }
    
    root.configure(bg=app_state["colors"]["bg"])
    
    window_width = 1200
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    create_menu(root, app_state)
    apply_modern_style(app_state)
    
    app_state["main_container"] = ttk.Frame(root, style="Modern.TFrame")
    app_state["main_container"].pack(fill="both", expand=True)
    
    app_state["canvas"] = tk.Canvas(app_state["main_container"], 
                                  bg=app_state["colors"]["bg"],
                                  highlightthickness=0)
    app_state["canvas"].pack(side="left", fill="both", expand=True)
    
    app_state["scrollable_frame"] = ttk.Frame(app_state["canvas"], style="Modern.TFrame")
    app_state["scrollable_frame"].bind("<Configure>",
        lambda e: app_state["canvas"].configure(scrollregion=app_state["canvas"].bbox("all")))
    
    app_state["canvas"].create_window((0, 0),
                                    window=app_state["scrollable_frame"],
                                    anchor="nw")
    
    app_state["scrollable_frame"].grid_columnconfigure(tuple(range(7)), weight=1)
    app_state["scrollable_frame"].grid_rowconfigure(0, weight=1)
    
    create_initial_tiles(app_state)
    create_see_more_button(app_state)
    
    app_state["canvas"].bind_all("<MouseWheel>", lambda e: on_mousewheel(e, app_state["canvas"]))
    
    return root

def main():
    root = init_app()
    root.mainloop()

if __name__ == "__main__":
    main()
