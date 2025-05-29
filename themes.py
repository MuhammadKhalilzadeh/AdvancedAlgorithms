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

def get_theme_colors(theme):
    """Get colors for a specific theme"""
    return THEMES.get(theme, THEMES["light"])

def get_weather_theme(weather_type):
    """Get theme name for a specific weather type"""
    return WEATHER_THEMES.get(weather_type.lower(), "light") 