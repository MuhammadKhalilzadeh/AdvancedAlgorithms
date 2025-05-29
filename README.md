# Modern Weather Forecast Application

A beautiful, modern weather forecast application built with Python and Tkinter, featuring a glass-morphic design and dynamic theme changes based on weather conditions.

## Features

- Full-screen modern UI with glass-morphic design
- Dynamic theme changes based on weather conditions
- Smooth transitions and hover effects
- 7-day weather forecast with expandable view
- Weather icons and temperature ranges
- Multiple theme support (Light, Dark, and weather-specific themes)
- Responsive design with horizontal scrolling

## Requirements

- Python 3.x
- Tkinter (included in Python standard library)
- Pillow (PIL) for image handling

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
├── themes.py            # Theme definitions and color schemes
├── weather_data.py      # Static weather data
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

- Click on any weather tile to change the application theme based on the weather condition
- Use the mouse wheel to scroll horizontally through the forecast
- Click "See More Days" to expand the view to show the entire month
- Use the Theme menu to switch between Light and Dark themes

### Theme System

The application features a sophisticated theme system with:

- Light and Dark base themes
- Weather-specific themes (Sunny, Rainy, Stormy, Snowy)
- Glass-morphic effects with consistent styling
- Smooth transitions between themes
- Hover effects with accent colors

## Customization

### Adding New Themes

To add a new theme, modify the `THEMES` dictionary in `themes.py`:

```python
THEMES = {
    "new_theme": {
        "bg": "#color",
        "tile_bg": "#color",
        "text": "#color",
        # ... other color properties
    }
}
```

### Modifying Weather Data

To modify weather data, edit the `WEATHER_DATA` and `MONTHLY_WEATHER` dictionaries in `weather_data.py`.

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
