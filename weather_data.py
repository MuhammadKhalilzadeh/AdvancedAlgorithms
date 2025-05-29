# Static weather data for demonstration
WEATHER_DATA = {
    "sunny": {
        "icon": "☀️",
        "description": "Sunny",
        "temp_range": {"min": 15, "avg": 22, "max": 28}
    },
    "partly_cloudy": {
        "icon": "⛅",
        "description": "Partly Cloudy",
        "temp_range": {"min": 12, "avg": 18, "max": 24}
    },
    "cloudy": {
        "icon": "☁️",
        "description": "Cloudy",
        "temp_range": {"min": 10, "avg": 15, "max": 20}
    },
    "rainy": {
        "icon": "🌧️",
        "description": "Rainy",
        "temp_range": {"min": 8, "avg": 13, "max": 18}
    },
    "stormy": {
        "icon": "⛈️",
        "description": "Stormy",
        "temp_range": {"min": 5, "avg": 10, "max": 15}
    }
}

# Predefined weather patterns for a month
MONTHLY_WEATHER = [
    "sunny", "sunny", "partly_cloudy", "cloudy", "rainy",
    "partly_cloudy", "sunny", "sunny", "cloudy", "rainy",
    "stormy", "rainy", "cloudy", "partly_cloudy", "sunny",
    "sunny", "partly_cloudy", "cloudy", "rainy", "stormy",
    "rainy", "cloudy", "partly_cloudy", "sunny", "sunny",
    "partly_cloudy", "cloudy", "rainy", "stormy", "rainy",
    "cloudy"
] 