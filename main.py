import tkinter as tk
import json
import os
from tkinter import PhotoImage, ttk
import time
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# --- Weather to image mapping logic ---
def weather_to_image(day):
    # Use precipitation, cloud_cover, and optionally other fields
    precip = day["precipitation"]["probability"]
    cloud = day["cloud_cover"]["value"]
    if precip >= 60:
        return "rainy.png"
    elif precip >= 20:
        return "cloudy.png"
    elif cloud >= 80:
        return "stormy.png"
    elif cloud >= 50:
        return "cloudy.png"
    elif cloud >= 20:
        return "foggy.png"
    elif day.get("temperature", {}).get("current", 20) <= 0:
        return "snowy.png"
    else:
        return "sunny.png"

# Load forecast data
with open('forcast_data.json', 'r', encoding='utf-8') as f:
    forecast_data = json.load(f)

# Update dates and avatars in forecast data to start from today
_today = datetime.now()
for city_data in forecast_data["cities"].values():
    for idx, day in enumerate(city_data["forecast"]):
        day["date"] = (_today + timedelta(days=idx)).strftime("%Y-%m-%d")
        day["avatar"] = weather_to_image(day)

# Create the main window
root = tk.Tk()

# Set window title
root.title("Weather's by Mohammad Khalilzadeh")

# Set window size to 600x400
root.geometry("600x400")

# Create main frame with scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create canvas and scrollbar
canvas = tk.Canvas(main_frame)
scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollbar and canvas
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Bind canvas resize to update scrollable frame width
def on_canvas_resize(event):
    canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
canvas.bind("<Configure>", on_canvas_resize)

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create Controls menu
controls_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Controls", menu=controls_menu)

# Add theme submenu
theme_menu = tk.Menu(controls_menu, tearoff=0)
controls_menu.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light")
theme_menu.add_command(label="Dark")

# Add exit option
controls_menu.add_separator()
controls_menu.add_command(label="Exit", command=root.quit)

# Create Sections menu
sections_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Sections", menu=sections_menu)
sections_menu.add_command(label="Today", command=lambda: show_today_view())
sections_menu.add_command(label="Upcoming days", command=lambda: show_upcoming_days())
sections_menu.add_command(label="News")

# Create a container frame for side-by-side layout
container_frame = tk.Frame(scrollable_frame)
container_frame.pack(padx=20, pady=20, fill="x", expand=False)

# Create a frame for city selection
city_frame = tk.LabelFrame(container_frame, text="Select City", padx=10, pady=10)
city_frame.pack(side="left", padx=(0, 10), fill="y", expand=False)

# Variable to store the selected city
selected_city = tk.StringVar(value="Tehran")  # Default selection

# Create radio buttons for each city
cities = ["Qazvin", "Tehran", "Karaj", "Zanjan"]
for city in cities:
    tk.Radiobutton(
        city_frame,
        text=city,
        variable=selected_city,
        value=city,
        padx=10,
        pady=5,
        command=lambda: update_cards()
    ).pack(anchor="w")

# Create a frame for weather parameters
weather_frame = tk.LabelFrame(container_frame, text="Weather Parameters", padx=10, pady=10)
weather_frame.pack(side="left", fill="both", expand=True)

# Dictionary to store checkbox variables
weather_vars = {}

# Create checkboxes for each weather parameter
weather_params = [
    "Temperature",
    "Atmospheric Pressure",
    "Humidity",
    "Precipitation",
    "Wind",
    "Cloud Cover",
    "UV Index",
    "Air Quality Index (AQI)"
]

# Create two columns for checkboxes
left_column = tk.Frame(weather_frame)
left_column.pack(side="left", fill="both", expand=True)
right_column = tk.Frame(weather_frame)
right_column.pack(side="left", fill="both", expand=True)

# Distribute checkboxes between columns
def on_param_change():
    update_cards()

for i, param in enumerate(weather_params):
    weather_vars[param] = tk.BooleanVar(value=True)
    column = left_column if i < len(weather_params) // 2 else right_column
    tk.Checkbutton(
        column,
        text=param,
        variable=weather_vars[param],
        padx=10,
        pady=5,
        command=on_param_change
    ).pack(anchor="w")

# --- Cards Section ---
cards_frame = tk.Frame(scrollable_frame)
cards_frame.pack(fill="x", padx=20, pady=(0, 20))

# Create a frame for the grid layout
grid_frame = tk.Frame(cards_frame)
grid_frame.pack(fill="x", expand=False)

# Keep references to PhotoImage to avoid garbage collection
image_cache = {}

def get_avatar_image(filename):
    if not filename:
        return None
    if filename not in image_cache:
        path = os.path.join("assets", "images", filename)
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((128, 128), Image.LANCZOS)
            image_cache[filename] = ImageTk.PhotoImage(img)
        else:
            image_cache[filename] = None
    return image_cache[filename]

def show_detailed_view(city, day_data):
    # Create a new window
    detail_window = tk.Toplevel(root)
    detail_window.title(f"Weather Details - {city} - {day_data['date']}")
    detail_window.geometry("400x600")

    # Create main frame with canvas and vertical scrollbar
    main_frame = ttk.Frame(detail_window, padding="0")
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Inner frame for padding and alignment ---
    inner = ttk.Frame(scrollable_frame, padding="20")
    inner.pack(fill=tk.BOTH, expand=True)

    # Add date header
    ttk.Label(inner, text=day_data['date'], font=("Arial", 16, "bold")).pack(pady=(0, 20))

    # Create a frame for the avatar
    avatar_frame = ttk.Frame(inner)
    avatar_frame.pack(fill="x", pady=(0, 20))

    # Add avatar if available
    avatar_img = get_avatar_image(day_data.get("avatar", ""))
    if avatar_img:
        ttk.Label(avatar_frame, image=avatar_img).pack()

    # Create a frame for weather details
    details_frame = ttk.Frame(inner)
    details_frame.pack(fill="both", expand=True)

    # Add all weather parameters with better formatting
    weather_details = [
        ("Temperature", f"{day_data['temperature']['current']}°{day_data['temperature']['unit']} (Min: {day_data['temperature']['min']}°, Max: {day_data['temperature']['max']}°)"),
        ("Atmospheric Pressure", f"{day_data['atmospheric_pressure']['value']} {day_data['atmospheric_pressure']['unit']}"),
        ("Humidity", f"{day_data['humidity']['value']}{day_data['humidity']['unit']}"),
        ("Precipitation", f"{day_data['precipitation']['value']} {day_data['precipitation']['unit']} (Probability: {day_data['precipitation']['probability']}%)"),
        ("Wind", f"{day_data['wind']['speed']} {day_data['wind']['unit']} {day_data['wind']['direction']}"),
        ("Cloud Cover", f"{day_data['cloud_cover']['value']}{day_data['cloud_cover']['unit']}"),
        ("UV Index", f"{day_data['uv_index']['value']} ({day_data['uv_index']['risk_level']})"),
        ("Air Quality", f"AQI: {day_data['air_quality']['aqi']} ({day_data['air_quality']['level']})")
    ]

    for label, value in weather_details:
        param_frame = ttk.Frame(details_frame)
        param_frame.pack(fill="x", pady=5)
        ttk.Label(param_frame, text=label, font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(param_frame, text=value).pack(anchor="w")

    # Add close button
    ttk.Button(inner, text="Close", command=detail_window.destroy).pack(pady=20)

def update_cards():
    # Clear previous cards
    for widget in grid_frame.winfo_children():
        widget.destroy()
    
    city = selected_city.get()
    params = [p for p in weather_params if weather_vars[p].get()]
    days = forecast_data["cities"][city]["forecast"]
    
    # Calculate number of columns based on window width
    # Each card will be approximately 300 pixels wide
    window_width = root.winfo_width() - 40  # Account for padding
    num_columns = min(3, max(1, window_width // 300))
    
    for i, day in enumerate(days):
        row = i // num_columns
        col = i % num_columns
        
        card = tk.Frame(grid_frame, bd=2, relief="groove", padx=10, pady=10)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Left side: Avatar
        left_frame = tk.Frame(card)
        left_frame.pack(side="left", padx=10)
        avatar_img = get_avatar_image(day.get("avatar", ""))
        if avatar_img:
            tk.Label(left_frame, image=avatar_img).pack()
        
        # Middle: Info
        info_frame = tk.Frame(card)
        info_frame.pack(side="left", fill="both", expand=True)
        tk.Label(info_frame, text=day["date"], font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Create a frame for parameters to allow wrapping
        params_frame = tk.Frame(info_frame)
        params_frame.pack(fill="both", expand=True)
        
        for param in params:
            key = param.lower().replace(" ", "_").replace("(aqi)", "air_quality")
            value = day
            # Map param to correct key in JSON
            if param == "Temperature":
                v = value["temperature"]
                text = f"Temperature: {v['current']}°{v['unit']} (min: {v['min']}, max: {v['max']})"
            elif param == "Atmospheric Pressure":
                v = value["atmospheric_pressure"]
                text = f"Pressure: {v['value']} {v['unit']}"
            elif param == "Humidity":
                v = value["humidity"]
                text = f"Humidity: {v['value']}{v['unit']}"
            elif param == "Precipitation":
                v = value["precipitation"]
                text = f"Precipitation: {v['value']} {v['unit']} (prob: {v['probability']}%)"
            elif param == "Wind":
                v = value["wind"]
                text = f"Wind: {v['speed']} {v['unit']} {v['direction']}"
            elif param == "Cloud Cover":
                v = value["cloud_cover"]
                text = f"Cloud Cover: {v['value']}{v['unit']}"
            elif param == "UV Index":
                v = value["uv_index"]
                text = f"UV Index: {v['value']} ({v['risk_level']})"
            elif param == "Air Quality Index (AQI)":
                v = value["air_quality"]
                text = f"AQI: {v['aqi']} ({v['level']})"
            else:
                text = param
            tk.Label(params_frame, text=text, anchor="w", wraplength=200).pack(anchor="w")
        
        # Button at the bottom of the card
        button_frame = tk.Frame(card)
        button_frame.pack(side="bottom", fill="x", pady=(10, 0))
        tk.Button(
            button_frame,
            text="See More Details",
            command=lambda c=city, d=day: show_detailed_view(c, d)
        ).pack(pady=5)
    
    # Configure grid weights to make cards expand properly
    for i in range(num_columns):
        grid_frame.grid_columnconfigure(i, weight=1)

# Add window resize handler to update card layout
last_resize_time = 0
resize_delay = 0.2  # 200ms delay

def on_window_resize(event):
    global last_resize_time
    current_time = time.time()
    
    # Only update if enough time has passed since last resize
    if current_time - last_resize_time > resize_delay:
        last_resize_time = current_time
        # Only update if the window width has changed significantly
        if hasattr(root, '_last_width') and abs(root.winfo_width() - root._last_width) > 50:
            root._last_width = root.winfo_width()
            update_cards()
        elif not hasattr(root, '_last_width'):
            root._last_width = root.winfo_width()

root.bind("<Configure>", on_window_resize)

# Initial population of cards
update_cards()

# Add a global variable to track the today_frame
_today_frame = None

def show_upcoming_days():
    global _today_frame
    # Destroy today_frame if it exists
    if _today_frame is not None:
        _today_frame.destroy()
        _today_frame = None
    # Show the main window with all cards
    main_frame.pack(fill=tk.BOTH, expand=True)
    cards_frame.pack(fill="x", padx=20, pady=(0, 20))
    update_cards()

def show_today_view():
    global _today_frame
    # Hide the main window with cards
    main_frame.pack_forget()
    cards_frame.pack_forget()
    # Destroy any previous today_frame
    if _today_frame is not None:
        _today_frame.destroy()
    # Create a new modern UI for today's weather
    today_frame = tk.Frame(root)
    today_frame.pack(fill=tk.BOTH, expand=True)
    _today_frame = today_frame

    # Get today's weather data
    city = selected_city.get()
    today_data = forecast_data["cities"][city]["forecast"][0]

    # Create a gradient background based on weather
    weather_type = today_data.get("avatar", "sunny.png").replace(".png", "")
    bg_colors = {
        "sunny": ("#FFD700", "#FFA500"),  # Gold to Orange
        "cloudy": ("#B0C4DE", "#778899"),  # Light Steel Blue to Slate Gray
        "rainy": ("#4682B4", "#1E90FF"),  # Steel Blue to Dodger Blue
        "stormy": ("#2F4F4F", "#696969"),  # Dark Slate Gray to Dim Gray
        "foggy": ("#D3D3D3", "#A9A9A9"),  # Light Gray to Dark Gray
        "snowy": ("#F0F8FF", "#E0FFFF")   # Alice Blue to Light Cyan
    }
    start_color, end_color = bg_colors.get(weather_type, ("#FFFFFF", "#F0F0F0"))

    # Create gradient background
    canvas = tk.Canvas(today_frame, highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    def create_gradient():
        canvas.delete("gradient")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        for i in range(height):
            r1, g1, b1 = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
            r2, g2, b2 = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)
            r = r1 + (r2 - r1) * i // height
            g = g1 + (g2 - g1) * i // height
            b = b1 + (b2 - b1) * i // height
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    canvas.bind('<Configure>', lambda e: [create_gradient(), update_content_position()])

    # Centered content frame
    content_frame = tk.Frame(canvas, bg='')
    content_window = canvas.create_window((0, 0), window=content_frame, anchor='center')

    def update_content_position():
        w = min(420, canvas.winfo_width() - 40)
        h = min(520, canvas.winfo_height() - 40)
        x = canvas.winfo_width() // 2
        y = canvas.winfo_height() // 2
        canvas.coords(content_window, x, y)
        content_frame.config(width=w, height=h)

    # Card frame (white, rounded, shadow)
    card_frame = tk.Frame(content_frame, bg='white', bd=0, highlightthickness=0)
    card_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
    # Shadow effect (simulate with a lower frame)
    shadow = tk.Frame(content_frame, bg='#e0e0e0', bd=0, highlightthickness=0)
    shadow.place(relx=0.5, rely=0.5, anchor='center', width=410, height=510, x=6, y=6)
    card_frame.lift()

    # City and date
    tk.Label(card_frame, text=city, font=('Helvetica', 22, 'bold'), bg='white', fg='#222').pack(pady=(28, 0))
    tk.Label(card_frame, text=today_data['date'], font=('Helvetica', 12), bg='white', fg='#888').pack(pady=(0, 10))

    # Weather icon and temperature
    if get_avatar_image(today_data.get("avatar", "")):
        tk.Label(card_frame, image=get_avatar_image(today_data.get("avatar", "")), bg='white').pack(pady=(0, 8))
    temp = today_data['temperature']['current']
    unit = today_data['temperature']['unit']
    tk.Label(card_frame, text=f"{temp}°{unit}", font=('Helvetica', 44, 'bold'), bg='white', fg='#222').pack()
    tk.Label(card_frame, text=f"Min: {today_data['temperature']['min']}° | Max: {today_data['temperature']['max']}°", 
             font=('Helvetica', 11), bg='white', fg='#888').pack(pady=(0, 12))

    # Weather details in a modern grid
    details = [
        ("Humidity", f"{today_data['humidity']['value']}{today_data['humidity']['unit']}"),
        ("Wind", f"{today_data['wind']['speed']} {today_data['wind']['unit']} {today_data['wind']['direction']}"),
        ("Pressure", f"{today_data['atmospheric_pressure']['value']} {today_data['atmospheric_pressure']['unit']}"),
        ("Precipitation", f"{today_data['precipitation']['value']} {today_data['precipitation']['unit']}"),
        ("Cloud Cover", f"{today_data['cloud_cover']['value']}{today_data['cloud_cover']['unit']}"),
        ("UV Index", f"{today_data['uv_index']['value']} ({today_data['uv_index']['risk_level']})"),
        ("Air Quality", f"AQI: {today_data['air_quality']['aqi']} ({today_data['air_quality']['level']})")
    ]
    details_frame = tk.Frame(card_frame, bg='white')
    details_frame.pack(pady=(8, 16), padx=24, fill='x')
    for i, (label, value) in enumerate(details):
        row = i // 2
        col = i % 2
        cell = tk.Frame(details_frame, bg='white')
        cell.grid(row=row, column=col, sticky='w', padx=8, pady=6)
        tk.Label(cell, text=label, font=('Helvetica', 10, 'bold'), bg='white', fg='#555').pack(anchor='w')
        tk.Label(cell, text=value, font=('Helvetica', 12), bg='white', fg='#222').pack(anchor='w')
    # Add subtle dividers
    for r in range(1, (len(details)+1)//2):
        divider = tk.Frame(details_frame, bg='#eee', height=1)
        divider.grid(row=r, column=0, columnspan=2, sticky='ew', pady=(0,0))

    # Add Back to Main button at the bottom of the card
    def back_to_main():
        if _today_frame is not None:
            _today_frame.destroy()
        show_upcoming_days()
    back_button = tk.Button(card_frame, text="Back to Main", 
                          command=back_to_main,
                          font=('Helvetica', 12, 'bold'),
                          bg='#FFD700',
                          fg='#222',
                          activebackground='#FFA500',
                          activeforeground='white',
                          relief='flat',
                          bd=0,
                          padx=18,
                          pady=8,
                          cursor='hand2')
    back_button.pack(pady=(10, 18))

    # Initial position update
    today_frame.after(100, update_content_position)

# Start the main event loop
root.mainloop()
