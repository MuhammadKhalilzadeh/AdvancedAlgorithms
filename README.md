# Modern Weather Forecast Application

A beautiful, modern weather forecast application built with Python and Tkinter, featuring a glass-morphic design and dynamic theme changes based on weather conditions.

## Features

- Full-screen modern UI with glass-morphic design
- Dynamic theme changes based on weather conditions
- Smooth transitions and hover effects
- 7-day weather forecast with expandable view
- Weather icons and temperature ranges
- Multiple theme support (Light and Dark themes)
- Responsive design with horizontal scrolling
- City-specific weather notes with SQLite database storage
- Detailed weather view for each day
- Weather parameters customization
- Support for multiple cities (Qazvin, Tehran, Karaj, Zanjan)
- Dynamic weather icons based on conditions
- Gradient backgrounds based on weather type

## Requirements

- Python 3.x
- Tkinter (included in Python standard library)
- Pillow (PIL) for image handling
- SQLite3 (included in Python standard library)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd weather-app
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Create necessary directories:

```bash
mkdir -p assets/images
mkdir -p assets/icons
```

## Project Structure

```
weather-app/
├── main.py              # Main application file
├── forcast_data.json    # Weather forecast data
├── news_data.json       # News data
├── weather_notes.db     # SQLite database for city notes
├── requirements.txt     # Python dependencies
├── assets/
│   ├── images/         # Weather icons
│   └── icons/          # Generated icons
└── README.md           # This file
```

## Usage

Run the application:

```bash
python main.py
```

### Controls

- Use the city selection radio buttons to switch between cities
- Check/uncheck weather parameters to customize the display
- Use the spinbox to adjust the number of forecast days (1-7)
- Click on any weather card to view detailed information
- Double-click on notes to delete them
- Use the Theme menu to switch between Light and Dark themes
- Use the Sections menu to switch between Today's view and Upcoming days

### Weather Parameters

The application displays the following weather parameters:

- Temperature (current, min, max)
- Atmospheric Pressure
- Humidity
- Precipitation (with probability)
- Wind (speed and direction)
- Cloud Cover
- UV Index (with risk level)
- Air Quality Index (AQI)

### Notes System

- Add city-specific notes using the notes section
- Notes are stored in a SQLite database
- Double-click to delete notes
- Notes are automatically updated when switching cities

### Theme System

The application features a sophisticated theme system with:

- Light and Dark base themes
- Weather-specific gradient backgrounds
- Glass-morphic effects with consistent styling
- Smooth transitions between themes
- Hover effects with accent colors

## Customization

### Adding New Cities

To add a new city, modify the `cities` list in `main.py`:

```python
cities = ["Qazvin", "Tehran", "Karaj", "Zanjan", "New City"]
```

### Modifying Weather Data

To modify weather data, edit the `forcast_data.json` file. The data structure should follow the format:

```json
{
  "cities": {
    "CityName": {
      "forecast": [
        {
          "date": "YYYY-MM-DD",
          "temperature": { "current": 20, "min": 15, "max": 25, "unit": "C" }
          // ... other weather parameters
        }
      ]
    }
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Weather icons are generated using PIL
- Color schemes are inspired by modern UI design principles
- Glass-morphic effects are implemented using Tkinter's styling capabilities
- SQLite database for persistent storage of city notes
