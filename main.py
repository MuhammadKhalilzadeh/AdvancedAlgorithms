import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from weather_data import WEATHER_DATA, MONTHLY_WEATHER
import calendar
from PIL import Image, ImageTk
import os

# Theme color schemes
THEMES = {
    "light": {
        "bg": "#f8fafc",
        "tile_bg": "#ffffff",
        "text": "#334155",
        "accent": "#3b82f6",
        "secondary": "#0ea5e9",
        "warning": "#ef4444",
        "button": "#ffffff",
        "button_hover": "#f1f5f9",
        "shadow": "#e2e8f0",
        "border": "#e2e8f0",
        "menu_bg": "#ffffff",
        "menu_fg": "#334155",
        "gradient_start": "#f0f9ff",
        "gradient_end": "#e0f2fe",
        "glass_bg": "#ffffff",
        "glass_border": "#e2e8f0",
        "hover_glow": "#3b82f6"
    },
    "dark": {
        "bg": "#0f172a",
        "tile_bg": "#1e293b",
        "text": "#e2e8f0",
        "accent": "#38bdf8",
        "secondary": "#818cf8",
        "warning": "#f87171",
        "button": "#1e293b",
        "button_hover": "#334155",
        "shadow": "#0f172a",
        "border": "#334155",
        "menu_bg": "#1e293b",
        "menu_fg": "#e2e8f0",
        "gradient_start": "#1e293b",
        "gradient_end": "#0f172a",
        "glass_bg": "#1e293b",
        "glass_border": "#334155",
        "hover_glow": "#38bdf8"
    },
    "sunny": {
        "bg": "#fff7ed",
        "tile_bg": "#ffffff",
        "text": "#431407",
        "accent": "#ea580c",
        "secondary": "#f97316",
        "warning": "#ef4444",
        "button": "#ffffff",
        "button_hover": "#fff7ed",
        "shadow": "#fed7aa",
        "border": "#fdba74",
        "menu_bg": "#ffffff",
        "menu_fg": "#431407",
        "gradient_start": "#fff7ed",
        "gradient_end": "#ffedd5",
        "glass_bg": "#ffffff",
        "glass_border": "#fdba74",
        "hover_glow": "#ea580c"
    },
    "rainy": {
        "bg": "#f1f5f9",
        "tile_bg": "#ffffff",
        "text": "#1e293b",
        "accent": "#0ea5e9",
        "secondary": "#38bdf8",
        "warning": "#ef4444",
        "button": "#ffffff",
        "button_hover": "#f1f5f9",
        "shadow": "#e2e8f0",
        "border": "#cbd5e1",
        "menu_bg": "#ffffff",
        "menu_fg": "#1e293b",
        "gradient_start": "#f1f5f9",
        "gradient_end": "#e2e8f0",
        "glass_bg": "#ffffff",
        "glass_border": "#cbd5e1",
        "hover_glow": "#0ea5e9"
    },
    "stormy": {
        "bg": "#1e293b",
        "tile_bg": "#334155",
        "text": "#e2e8f0",
        "accent": "#38bdf8",
        "secondary": "#818cf8",
        "warning": "#f87171",
        "button": "#334155",
        "button_hover": "#475569",
        "shadow": "#0f172a",
        "border": "#475569",
        "menu_bg": "#334155",
        "menu_fg": "#e2e8f0",
        "gradient_start": "#1e293b",
        "gradient_end": "#0f172a",
        "glass_bg": "#334155",
        "glass_border": "#475569",
        "hover_glow": "#38bdf8"
    },
    "snowy": {
        "bg": "#f8fafc",
        "tile_bg": "#ffffff",
        "text": "#334155",
        "accent": "#94a3b8",
        "secondary": "#cbd5e1",
        "warning": "#ef4444",
        "button": "#ffffff",
        "button_hover": "#f1f5f9",
        "shadow": "#e2e8f0",
        "border": "#cbd5e1",
        "menu_bg": "#ffffff",
        "menu_fg": "#334155",
        "gradient_start": "#f8fafc",
        "gradient_end": "#f1f5f9",
        "glass_bg": "#ffffff",
        "glass_border": "#cbd5e1",
        "hover_glow": "#94a3b8"
    }
}

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

# Weather to theme mapping
WEATHER_THEMES = {
    "sunny": "sunny",
    "partly-cloudy": "light",
    "cloudy": "light",
    "rainy": "rainy",
    "stormy": "stormy",
    "snowy": "snowy",
    "foggy": "light"
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

def create_glass_frame(parent, theme="light", app_instance=None, **kwargs):
    """Create a frame with enhanced glass-morphic effect"""
    frame = tk.Frame(parent,
                    bg=THEMES[theme]["glass_bg"],
                    highlightbackground=THEMES[theme]["glass_border"],
                    highlightthickness=1,
                    **kwargs)
    
    # Add shadow effect
    frame.configure(relief="flat")
    frame.bind("<Map>", lambda e: frame.configure(relief="flat"))
    
    # Add hover effect
    def on_enter(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_instance.current_theme
            frame.configure(bg=THEMES[current_theme]["button_hover"])
            frame.configure(highlightbackground=THEMES[current_theme]["accent"])
            # Add a subtle glow effect
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=THEMES[current_theme]["accent"])
    
    def on_leave(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_instance.current_theme
            frame.configure(bg=THEMES[current_theme]["glass_bg"])
            frame.configure(highlightbackground=THEMES[current_theme]["glass_border"])
            # Restore original colors
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=THEMES[current_theme]["text"])
    
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    
    return frame

def get_weather_for_date(date):
    """Get weather data for a specific date from our static data"""
    day_index = date.day - 1
    weather_type = MONTHLY_WEATHER[day_index]
    return WEATHER_DATA[weather_type]

def create_weather_tile(parent, date, column, theme="light", app_instance=None):
    """Create a single weather tile with modern styling and improved image presentation"""
    frame = create_glass_frame(parent, theme=theme, app_instance=app_instance, padx=20, pady=20)
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
        bg=THEMES[theme]["tile_bg"],
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
        weather_type = weather["description"].lower()
        theme = WEATHER_THEMES.get(weather_type, "light")
        app_instance.change_theme(theme)

    frame.bind("<Button-1>", on_tile_click)
    # Also bind to all child widgets to ensure the click event is captured
    for child in frame.winfo_children():
        child.bind("<Button-1>", on_tile_click)

    return frame

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Weather Forecast")
        
        # Initialize with light theme
        self.current_theme = "light"
        self.colors = THEMES[self.current_theme]
        
        # Configure root window
        self.root.configure(bg=self.colors["bg"])
        
        # Set window size and position
        window_width = 1200
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position for center of screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create menu bar
        self.create_menu()
        
        # Apply modern styling
        self.apply_modern_style()
        
        # Create main container with gradient background
        self.main_container = ttk.Frame(root, style="Modern.TFrame")
        self.main_container.pack(fill="both", expand=True)
        
        # Create canvas for scrolling with gradient background
        self.canvas = tk.Canvas(self.main_container, 
                              bg=self.colors["bg"],
                              highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas, style="Modern.TFrame")
        self.scrollable_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create window in canvas
        self.canvas_frame = self.canvas.create_window((0, 0),
                                                    window=self.scrollable_frame,
                                                    anchor="nw")
        
        # Get current date and month info
        self.current_date = datetime.now()
        self.days_in_month = calendar.monthrange(self.current_date.year, 
                                               self.current_date.month)[1]
        self.remaining_days = self.days_in_month - self.current_date.day + 1
        
        # Configure grid for initial 7 days
        self.scrollable_frame.grid_columnconfigure(tuple(range(7)), weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        
        # Create initial weather tiles
        self.create_initial_tiles()
        
        # Add see more button
        self.create_see_more_button()
        
        # Bind mouse wheel for horizontal scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def apply_modern_style(self):
        """Apply modern styling to the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles with glass-morphic effects
        style.configure("Modern.TFrame",
                       background=self.colors["tile_bg"],
                       relief="flat",
                       borderwidth=0)
        
        style.configure("Modern.TLabel",
                       background=self.colors["tile_bg"],
                       foreground=self.colors["text"],
                       font=("Segoe UI", 10))
        
        style.configure("Date.TLabel",
                       background=self.colors["tile_bg"],
                       foreground=self.colors["accent"],
                       font=("Segoe UI", 12, "bold"))
        
        style.configure("Temp.TLabel",
                       background=self.colors["tile_bg"],
                       foreground=self.colors["text"],
                       font=("Segoe UI", 9))
        
        style.configure("Modern.TButton",
                       background=self.colors["button"],
                       foreground=self.colors["text"],
                       font=("Segoe UI", 10),
                       padding=10,
                       relief="flat",
                       borderwidth=0)
        
        style.map("Modern.TButton",
                  background=[("active", self.colors["button_hover"])],
                  foreground=[("active", self.colors["accent"])])
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root, bg=self.colors["menu_bg"], fg=self.colors["menu_fg"])
        self.root.config(menu=menubar)
        
        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["menu_bg"], fg=self.colors["menu_fg"])
        menubar.add_cascade(label="Theme", menu=theme_menu)
        
        # Add theme options
        theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))
        
        # Add separator
        theme_menu.add_separator()
        
        # Add exit option
        theme_menu.add_command(label="Exit", command=self.root.quit)
    
    def change_theme(self, theme):
        """Change the application theme with smooth transition"""
        if theme == self.current_theme:
            return

        self.current_theme = theme
        self.colors = THEMES[theme]
        
        # Update root window with smooth transition
        self.root.configure(bg=self.colors["bg"])
        
        # Update canvas with smooth transition
        self.canvas.configure(bg=self.colors["bg"])
        
        # Update menu colors
        for menu in self.root.winfo_children():
            if isinstance(menu, tk.Menu):
                menu.configure(bg=self.colors["menu_bg"], fg=self.colors["menu_fg"])
                for submenu in menu.winfo_children():
                    if isinstance(submenu, tk.Menu):
                        submenu.configure(bg=self.colors["menu_bg"], fg=self.colors["menu_fg"])
        
        # Reapply styles
        self.apply_modern_style()
        
        # Update all tiles with smooth transition
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                # Reset hover state
                widget.configure(bg=self.colors["glass_bg"],
                               highlightbackground=self.colors["glass_border"])
                
                # Update all child widgets
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=self.colors["tile_bg"],
                                      fg=self.colors["text"])
                    elif isinstance(child, ttk.Label):
                        child.configure(style="Modern.TLabel")
                    elif isinstance(child, ttk.Frame):
                        child.configure(style="Modern.TFrame")
                        # Update temperature labels
                        for temp_label in child.winfo_children():
                            if isinstance(temp_label, ttk.Label):
                                temp_label.configure(style="Temp.TLabel")
        
        # Update see more button
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame):
                # Reset hover state
                widget.configure(bg=self.colors["glass_bg"],
                               highlightbackground=self.colors["glass_border"])
                
                # Update button
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        child.configure(style="Modern.TButton")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_initial_tiles(self):
        """Create initial 7 weather tiles"""
        for i in range(7):
            date = self.current_date + timedelta(days=i)
            create_weather_tile(self.scrollable_frame, date, i, theme=self.current_theme, app_instance=self)
    
    def create_see_more_button(self):
        """Create see more button with glass-morphic effect"""
        # Create a frame that matches the height of weather tiles
        button_frame = create_glass_frame(self.main_container, theme=self.current_theme, app_instance=self, padx=15, pady=15)
        button_frame.pack(side="right", padx=15, pady=15)
        
        # Create the button
        self.see_more = ttk.Button(button_frame,
                                  text=f"See {self.remaining_days} More Days →",
                                  style="Modern.TButton",
                                  command=self.show_remaining_days)
        self.see_more.pack(expand=True, fill="both", padx=10, pady=10)
    
    def show_remaining_days(self):
        """Show all remaining days of the month"""
        # Configure grid for all days
        self.scrollable_frame.grid_columnconfigure(tuple(range(self.days_in_month)), weight=1)
        
        # Create tiles for remaining days
        for i in range(7, self.days_in_month):
            date = self.current_date + timedelta(days=i)
            create_weather_tile(self.scrollable_frame, date, i, theme=self.current_theme, app_instance=self)
        
        # Update button text
        self.see_more.configure(text="All Days Shown")
        self.see_more.configure(state="disabled")

def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
