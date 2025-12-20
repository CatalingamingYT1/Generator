import tkinter as tk
from tkinter import font
import math
import random

class CoolBRFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRF App")
        self.root.geometry("600x400")
        self.root.configure(bg="#0a0a0a")
        
        # Stochează culorile
        self.colors = {
            "bg": "#0a0a0a",
            "neon": "#00ffaa",
            "gray": "#888888",
            "accent": "#00ff88"
        }
        
        # Crează bara de titlu personalizată
        self.create_title_bar()
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root,
            bg=self.colors["bg"],
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crează conținutul
        self.create_content()
        
        # Variabile pentru animații
        self.angle = 0
        self.pulse_phase = 0
        self.glow_phase = 0
        
        # Centrează fereastra
        self.center_window()
        
        # Pornește animațiile
        self.animate()
    
    def create_title_bar(self):
        """Creează bara de titlu personalizată"""
        title_frame = tk.Frame(
            self.root,
            bg="#1a1a1a",
            height=35
        )
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        # Buton de închidere (X) - ROȘU
        close_btn = tk.Button(
            title_frame,
            text="×",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#ff4444",  # Roșu
            activebackground="#ff6666",
            activeforeground="white",
            bd=0,
            padx=12,
            command=self.root.destroy
        )
        close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Buton maximize/restore - GALBEN
        self.maximized = False
        self.max_btn = tk.Button(
            title_frame,
            text="□",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#ffaa00",  # Galben
            activebackground="#ffcc44",
            activeforeground="white",
            bd=0,
            padx=12,
            command=self.toggle_maximize
        )
        self.max_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Buton minimize - ALBASTRU
        min_btn = tk.Button(
            title_frame,
            text="–",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#4488ff",  # Albastru
            activebackground="#66aaff",
            activeforeground="white",
            bd=0,
            padx=12,
            command=self.root.iconify
        )
        min_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Titlu aplicație
        title_label = tk.Label(
            title_frame,
            text="BRF Application",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Permite glisarea ferestrei
        title_frame.bind("<Button-1>", self.start_move)
        title_frame.bind("<B1-Motion>", self.on_move)
        title_label.bind("<Button-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.on_move)
    
    def create_content(self):
        """Creează conținutul principal al aplicației"""
        # Text principal - FOARTE MARE
        self.main_font = font.Font(
            family="Segoe UI",
            size=72,  # FOARTE MARE
            weight="bold"
        )
        
        self.main_text = self.canvas.create_text(
            300, 130,  # Poziție mai sus pentru text mare
            text="BRF",
            font=self.main_font,
            fill=self.colors["neon"],
            anchor="center"
        )
        
        # Subtitlu
        self.sub_font = font.Font(
            family="Segoe UI",
            size=28,
            weight="normal"
        )
        
        self.sub_text = self.canvas.create_text(
            300, 200,
            text="BotRobloxFarm",
            font=self.sub_font,
            fill=self.colors["gray"],
            anchor="center"
        )
        
        # Linie decorativă
        self.line = self.canvas.create_line(
            150, 250, 450, 250,
            fill=self.colors["neon"],
            width=3
        )
        
        # Text status
        self.status_font = font.Font(
            family="Consolas",
            size=18,
            weight="normal"
        )
        
        self.status_text = self.canvas.create_text(
            300, 290,
            text="▶ SYSTEM ACTIVE",
            font=self.status_font,
            fill=self.colors["accent"],
            anchor="center"
        )
        
        # Informații versiune
        info_font = font.Font(
            family="Segoe UI",
            size=10,
            weight="normal"
        )
        
        self.canvas.create_text(
            300, 350,
            text="Version 2.0 | © 2024 BRF Team",
            font=info_font,
            fill="#555555",
            anchor="center"
        )
    
    def start_move(self, event):
        self.x = event.x_root
        self.y = event.y_root
    
    def on_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{self.root.winfo_x() + x}+{self.root.winfo_y() + y}")
        self.x = event.x_root
        self.y = event.y_root
    
    def toggle_maximize(self):
        """Comută între maximizat și normal"""
        if not self.maximized:
            self.root.state('zoomed')
            self.max_btn.config(text="❐")
            self.maximized = True
        else:
            self.root.state('normal')
            self.max_btn.config(text="□")
            self.maximized = True
            self.center_window()
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        if not self.maximized:
            width = 600
            height = 400
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def animate(self):
        """Rulează animațiile"""
        # Animație pulsare text principal
        self.pulse_phase += 0.08
        pulse_value = (math.sin(self.pulse_phase) + 1) / 2
        
        # Animație schimbare culoare
        self.glow_phase += 0.03
        r = int(math.sin(self.glow_phase) * 30)
        g = 255
        b = int(math.cos(self.glow_phase) * 50 + 155)
        color = f'#{max(0, r):02x}{g:02x}{b:02x}'
        
        # Aplică animația textului principal
        self.canvas.itemconfig(self.main_text, fill=color)
        
        # Animație text status
        dots = ["   ", ".  ", ".. ", "..."]
        dot_index = int(self.pulse_phase * 1.5) % 4
        status_text = f"▶ SYSTEM ACTIVE{dots[dot_index]}"
        self.canvas.itemconfig(self.status_text, text=status_text)
        
        # Animație linie (pulsare)
        line_width = int(pulse_value * 2) + 2
        self.canvas.itemconfig(self.line, width=line_width)
        
        # Programează următorul frame de animație
        self.root.after(60, self.animate)
    
    def run(self):
        """Rulează aplicația"""
        self.root.mainloop()

def main():
    # Creează fereastra principală
    root = tk.Tk()
    
    # Icon pentru fereastră (opțional)
    try:
        root.iconbitmap(default='icon.ico')  # Dacă ai un fișier .ico
    except:
        pass
    
    # Creează aplicația
    app = CoolBRFApp(root)
    
    # Rulează aplicația
    app.run()

if __name__ == "__main__":
    main()
