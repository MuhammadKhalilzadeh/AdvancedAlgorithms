from tkinter import ttk

def apply_modern_style(app_state):
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure base styles
    style.configure("Modern.TFrame",
                   background=app_state["colors"]["bg"],
                   relief="flat",
                   borderwidth=0)
    
    style.configure("Modern.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 10))
    
    style.configure("Date.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["accent"],
                   font=("Segoe UI", 12, "bold"))
    
    style.configure("Temp.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 9))
    
    style.configure("Modern.TButton",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 10),
                   padding=10,
                   relief="flat",
                   borderwidth=0)
    
    # News section styles
    style.configure("Title.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["accent"],
                   font=("Segoe UI", 16, "bold"))
    
    style.configure("Category.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["accent"],
                   font=("Segoe UI", 9, "bold"))
    
    style.configure("Time.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 9))
    
    style.configure("NewsTitle.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 12, "bold"))
    
    style.configure("NewsSummary.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 10))
    
    style.configure("Source.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["accent"],
                   font=("Segoe UI", 9, "italic"))
    
    style.configure("NewsImage.TLabel",
                   background=app_state["colors"]["bg"],
                   foreground=app_state["colors"]["text"],
                   font=("Segoe UI", 24))
    
    style.map("Modern.TButton",
              background=[("active", app_state["colors"]["button_hover"])],
              foreground=[("active", app_state["colors"]["accent"])])