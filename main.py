import tkinter as tk
import json
import os
from tkinter import PhotoImage

# Load forecast data
with open('forcast_data.json', 'r') as f:
    forecast_data = json.load(f)

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
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollbar and canvas
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

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
sections_menu.add_command(label="Today")
sections_menu.add_command(label="Upcoming days")
sections_menu.add_command(label="News")

# Create a container frame for side-by-side layout
container_frame = tk.Frame(scrollable_frame)
container_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Create a frame for city selection
city_frame = tk.LabelFrame(container_frame, text="Select City", padx=10, pady=10)
city_frame.pack(side="left", padx=(0, 10), fill="both", expand=True)

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

# Keep references to PhotoImage to avoid garbage collection
image_cache = {}

def get_avatar_image(filename):
    if filename not in image_cache:
        path = os.path.join("images", filename)
        if os.path.exists(path):
            image_cache[filename] = PhotoImage(file=path)
        else:
            image_cache[filename] = None
    return image_cache[filename]

def update_cards():
    # Clear previous cards
    for widget in cards_frame.winfo_children():
        widget.destroy()
    city = selected_city.get()
    params = [p for p in weather_params if weather_vars[p].get()]
    days = forecast_data["cities"][city]["forecast"]
    for day in days:
        card = tk.Frame(cards_frame, bd=2, relief="groove", padx=10, pady=10)
        card.pack(fill="x", pady=5)
        # Avatar
        avatar_img = get_avatar_image(day.get("avatar", ""))
        if avatar_img:
            tk.Label(card, image=avatar_img).pack(side="left", padx=10)
        # Info
        info_frame = tk.Frame(card)
        info_frame.pack(side="left", fill="x", expand=True)
        tk.Label(info_frame, text=day["date"], font=("Arial", 10, "bold")).pack(anchor="w")
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
            tk.Label(info_frame, text=text, anchor="w").pack(anchor="w")

# Initial population of cards
update_cards()

# Start the main event loop
root.mainloop()
