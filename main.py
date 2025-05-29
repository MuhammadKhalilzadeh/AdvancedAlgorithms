import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from weather_data import WEATHER_DATA, MONTHLY_WEATHER
import calendar

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
        "glass_border": "#e2e8f0"
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
        "glass_border": "#334155"
    }
}

def create_glass_frame(parent, theme="light", **kwargs):
    """Create a frame with glass-morphic effect"""
    frame = tk.Frame(parent,
                    bg=THEMES[theme]["glass_bg"],
                    highlightbackground=THEMES[theme]["glass_border"],
                    highlightthickness=1,
                    **kwargs)
    
    # Add shadow effect
    frame.configure(relief="flat")
    frame.bind("<Map>", lambda e: frame.configure(relief="flat"))
    
    return frame

def get_weather_for_date(date):
    """Get weather data for a specific date from our static data"""
    day_index = date.day - 1
    weather_type = MONTHLY_WEATHER[day_index]
    return WEATHER_DATA[weather_type]

def create_weather_tile(parent, date, column, theme="light"):
    """Create a single weather tile with modern styling"""
    frame = create_glass_frame(parent, theme=theme, padx=15, pady=15)
    frame.grid(row=0, column=column, padx=15, pady=15, sticky="nsew")
    
    # Add date label with accent color
    date_label = ttk.Label(frame, 
                          text=date.strftime("%a\n%d %b"),
                          style="Date.TLabel")
    date_label.pack(pady=10)
    
    # Get weather data
    weather = get_weather_for_date(date)
    
    # Add weather icon with larger size
    weather_icon = ttk.Label(frame, 
                            text=weather["icon"],
                            style="Icon.TLabel")
    weather_icon.pack(pady=10)
    
    # Add weather description
    desc_label = ttk.Label(frame, 
                          text=weather["description"],
                          style="Modern.TLabel")
    desc_label.pack(pady=5)
    
    # Add temperature labels with modern styling
    temp_frame = ttk.Frame(frame, style="Modern.TFrame")
    temp_frame.pack(pady=10)
    
    min_temp = ttk.Label(temp_frame, 
                        text=f"Min: {weather['temp_range']['min']}°C",
                        style="Temp.TLabel")
    avg_temp = ttk.Label(temp_frame, 
                        text=f"Avg: {weather['temp_range']['avg']}°C",
                        style="Temp.TLabel")
    max_temp = ttk.Label(temp_frame, 
                        text=f"Max: {weather['temp_range']['max']}°C",
                        style="Temp.TLabel")
    
    min_temp.pack(pady=2)
    avg_temp.pack(pady=2)
    max_temp.pack(pady=2)
    
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
        
        # Create canvas for scrolling
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
        
        # Configure styles
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
        
        style.configure("Icon.TLabel",
                       background=self.colors["tile_bg"],
                       foreground=self.colors["secondary"],
                       font=("Segoe UI", 24))
        
        style.configure("Temp.TLabel",
                       background=self.colors["tile_bg"],
                       foreground=self.colors["text"],
                       font=("Segoe UI", 9))
        
        style.configure("Modern.TButton",
                       background=self.colors["button"],
                       foreground=self.colors["text"],
                       font=("Segoe UI", 10),
                       padding=10)
        
        style.map("Modern.TButton",
                  background=[("active", self.colors["button_hover"])])
    
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
        """Change the application theme"""
        self.current_theme = theme
        self.colors = THEMES[theme]
        
        # Update root window
        self.root.configure(bg=self.colors["bg"])
        
        # Update canvas
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
        
        # Recreate all tiles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_initial_tiles()
        
        # Recreate see more button
        for widget in self.main_container.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        self.create_see_more_button()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_initial_tiles(self):
        """Create initial 7 weather tiles"""
        for i in range(7):
            date = self.current_date + timedelta(days=i)
            create_weather_tile(self.scrollable_frame, date, i, theme=self.current_theme)
    
    def create_see_more_button(self):
        """Create see more button"""
        # Create a frame that matches the height of weather tiles
        button_frame = create_glass_frame(self.main_container, theme=self.current_theme, padx=15, pady=15)
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
            create_weather_tile(self.scrollable_frame, date, i, theme=self.current_theme)
        
        # Update button text
        self.see_more.configure(text="All Days Shown")
        self.see_more.configure(state="disabled")

def main():
    root = tk.Tk()
    WeatherApp(root)  # Removed unused variable
    root.mainloop()

if __name__ == "__main__":
    main()
