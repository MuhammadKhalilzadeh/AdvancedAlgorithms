import tkinter as tk
from tkinter import ttk
from themes import get_theme_colors

def create_news_section(container, app_state):
    # Create a frame for news articles with horizontal scrolling
    news_frame = create_glass_frame(container, theme=app_state["current_theme"], app_state=app_state)
    news_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create a canvas for horizontal scrolling
    news_canvas = tk.Canvas(news_frame,
                           bg=app_state["colors"]["bg"],
                           highlightthickness=0,
                           height=400)  # Increased height
    news_canvas.pack(side="left", fill="both", expand=True)
    
    # Add horizontal scrollbar
    h_scrollbar = ttk.Scrollbar(news_frame, orient="horizontal", command=news_canvas.xview)
    h_scrollbar.pack(side="bottom", fill="x")
    
    # Configure canvas
    news_canvas.configure(xscrollcommand=h_scrollbar.set)
    
    # Create frame for news content
    news_content = ttk.Frame(news_canvas, style="Modern.TFrame")
    news_canvas.create_window((0, 0), window=news_content, anchor="nw")
    
    # Bind scrollbar to canvas
    news_content.bind("<Configure>",
        lambda e: news_canvas.configure(scrollregion=news_canvas.bbox("all")))
    
    # Bind mouse wheel for horizontal scrolling
    news_canvas.bind_all("<Shift-MouseWheel>", lambda e: news_canvas.xview_scroll(int(-1*(e.delta/120)), "units"))
    
    # Create a frame to hold all news cards horizontally
    news_cards_frame = ttk.Frame(news_content, style="Modern.TFrame")
    news_cards_frame.pack(fill="x", padx=10, pady=10)
    
    # Add news cards horizontally
    for news in get_sample_news():
        create_news_article(news_cards_frame, news, app_state)

def create_news_article(parent, news, app_state):
    # Create article frame with fixed width
    article_frame = create_glass_frame(parent, theme=app_state["current_theme"], app_state=app_state)
    article_frame.pack(side="left", fill="y", padx=10, pady=5)
    article_frame.configure(width=300)  # Fixed width for each card
    
    # Create header with image and category
    header_frame = ttk.Frame(article_frame, style="Modern.TFrame")
    header_frame.pack(fill="x", padx=10, pady=(10, 5))
    
    # Add emoji/image
    image_label = ttk.Label(
        header_frame,
        text=news["image"],
        style="NewsImage.TLabel",
        font=("Segoe UI", 24)
    )
    image_label.pack(side="left", padx=(0, 10))
    
    # Category and time
    meta_frame = ttk.Frame(header_frame, style="Modern.TFrame")
    meta_frame.pack(side="left", fill="x", expand=True)
    
    category = ttk.Label(
        meta_frame,
        text=news["category"],
        style="Category.TLabel",
        font=("Segoe UI", 9, "bold")
    )
    category.pack(anchor="w")
    
    time = ttk.Label(
        meta_frame,
        text=news["time"],
        style="Time.TLabel",
        font=("Segoe UI", 9)
    )
    time.pack(anchor="w")
    
    # Title
    title = ttk.Label(
        article_frame,
        text=news["title"],
        style="NewsTitle.TLabel",
        font=("Segoe UI", 12, "bold"),
        wraplength=280
    )
    title.pack(fill="x", padx=10, pady=(0, 5))
    
    # Summary
    summary = ttk.Label(
        article_frame,
        text=news["summary"],
        style="NewsSummary.TLabel",
        font=("Segoe UI", 10),
        wraplength=280
    )
    summary.pack(fill="x", padx=10, pady=(0, 10))
    
    # Source
    source_frame = ttk.Frame(article_frame, style="Modern.TFrame")
    source_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    source = ttk.Label(
        source_frame,
        text=f"Source: {news['source']}",
        style="Source.TLabel",
        font=("Segoe UI", 9, "italic")
    )
    source.pack(anchor="e")

def get_sample_news():
    return [
        {
            "title": "Breaking News: Major Weather Event",
            "summary": "A significant weather system is approaching the region, bringing heavy rainfall and strong winds. Authorities advise residents to prepare for potential flooding.",
            "category": "Weather",
            "time": "2 hours ago",
            "source": "Weather Service",
            "image": "🌧️"
        },
        {
            "title": "Technology Update: New Weather Forecasting System",
            "summary": "Scientists have developed a revolutionary AI-powered system for more accurate weather predictions, promising to improve forecast accuracy by up to 40%.",
            "category": "Technology",
            "time": "4 hours ago",
            "source": "Tech Daily",
            "image": "🤖"
        },
        {
            "title": "Environmental News: Climate Change Impact",
            "summary": "New study reveals the effects of climate change on local weather patterns, showing a 30% increase in extreme weather events over the past decade.",
            "category": "Environment",
            "time": "6 hours ago",
            "source": "Eco Watch",
            "image": "🌍"
        },
        {
            "title": "Emergency Alert: Severe Storm Warning",
            "summary": "Meteorologists issue severe storm warning for coastal regions. Residents are advised to seek shelter and stay informed through official channels.",
            "category": "Emergency",
            "time": "1 hour ago",
            "source": "Emergency Services",
            "image": "⚠️"
        },
        {
            "title": "Research: Weather Pattern Changes",
            "summary": "New research indicates significant changes in global weather patterns, with implications for agriculture and urban planning.",
            "category": "Research",
            "time": "8 hours ago",
            "source": "Science Daily",
            "image": "🔬"
        }
    ]

def create_glass_frame(parent, theme="light", app_state=None, **kwargs):
    colors = get_theme_colors(theme)
    frame = tk.Frame(parent,
                    bg=colors["bg"],
                    highlightbackground=colors["glass_border"],
                    highlightthickness=1,
                    **kwargs)
    
    frame.configure(relief="flat")
    frame.bind("<Map>", lambda e: frame.configure(relief="flat"))
    
    def on_enter(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_state["current_theme"]
            colors = get_theme_colors(current_theme)
            frame.configure(bg=colors["button_hover"])
            frame.configure(highlightbackground=colors["accent"])
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=colors["accent"])
    
    def on_leave(e):
        if not hasattr(frame, '_theme_changing'):
            current_theme = app_state["current_theme"]
            colors = get_theme_colors(current_theme)
            frame.configure(bg=colors["bg"])
            frame.configure(highlightbackground=colors["glass_border"])
            for child in frame.winfo_children():
                if isinstance(child, (tk.Label, ttk.Label)):
                    child.configure(foreground=colors["text"])
    
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    
    return frame