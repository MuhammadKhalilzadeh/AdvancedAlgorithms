import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from weather_data import WEATHER_DATA, MONTHLY_WEATHER
import calendar

# Modern color scheme
COLORS = {
    "bg": "#1a1a1a",
    "tile_bg": "#2d2d2d",
    "text": "#ffffff",
    "accent": "#00ff9d",
    "secondary": "#00b8ff",
    "warning": "#ff3e3e",
    "button": "#3d3d3d",
    "button_hover": "#4d4d4d"
}

def apply_modern_style():
    """Apply modern styling to the application"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles
    style.configure("Modern.TFrame",
                   background=COLORS["tile_bg"],
                   relief="flat",
                   borderwidth=0)
    
    style.configure("Modern.TLabel",
                   background=COLORS["tile_bg"],
                   foreground=COLORS["text"],
                   font=("Segoe UI", 10))
    
    style.configure("Date.TLabel",
                   background=COLORS["tile_bg"],
                   foreground=COLORS["accent"],
                   font=("Segoe UI", 12, "bold"))
    
    style.configure("Icon.TLabel",
                   background=COLORS["tile_bg"],
                   foreground=COLORS["secondary"],
                   font=("Segoe UI", 24))
    
    style.configure("Temp.TLabel",
                   background=COLORS["tile_bg"],
                   foreground=COLORS["text"],
                   font=("Segoe UI", 9))
    
    style.configure("Modern.TButton",
                   background=COLORS["button"],
                   foreground=COLORS["text"],
                   font=("Segoe UI", 10),
                   padding=10)
    
    style.map("Modern.TButton",
              background=[("active", COLORS["button_hover"])])

def get_weather_for_date(date):
    """Get weather data for a specific date from our static data"""
    day_index = date.day - 1
    weather_type = MONTHLY_WEATHER[day_index]
    return WEATHER_DATA[weather_type]

def create_weather_tile(parent, date, column):
    """Create a single weather tile with modern styling"""
    frame = ttk.Frame(parent, style="Modern.TFrame", padding="15")
    frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
    
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
        self.root.configure(bg=COLORS["bg"])
        self.root.attributes('-fullscreen', True)
        
        # Apply modern styling
        apply_modern_style()
        
        # Create main container
        self.main_container = ttk.Frame(root, style="Modern.TFrame")
        self.main_container.pack(fill="both", expand=True)
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(self.main_container, 
                              bg=COLORS["bg"],
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
        
        # Bind escape key
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Bind mouse wheel for horizontal scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_initial_tiles(self):
        """Create initial 7 weather tiles"""
        for i in range(7):
            date = self.current_date + timedelta(days=i)
            create_weather_tile(self.scrollable_frame, date, i)
    
    def create_see_more_button(self):
        """Create see more button"""
        button_frame = ttk.Frame(self.main_container, style="Modern.TFrame")
        button_frame.pack(side="right", padx=20)
        
        self.see_more = ttk.Button(button_frame,
                                  text=f"See {self.remaining_days} More Days →",
                                  style="Modern.TButton",
                                  command=self.show_remaining_days)
        self.see_more.pack(pady=20)
    
    def show_remaining_days(self):
        """Show all remaining days of the month"""
        # Configure grid for all days
        self.scrollable_frame.grid_columnconfigure(tuple(range(self.days_in_month)), weight=1)
        
        # Create tiles for remaining days
        for i in range(7, self.days_in_month):
            date = self.current_date + timedelta(days=i)
            create_weather_tile(self.scrollable_frame, date, i)
        
        # Update button text
        self.see_more.configure(text="All Days Shown")
        self.see_more.configure(state="disabled")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
