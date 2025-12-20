import tkinter as tk
from tkinter import font
import math

class BRFMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BRF")
        
        # Setări fereastră transparentă
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.95)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#000000')
        
        # Dimensiuni
        self.width, self.height = 450, 300
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Canvas pentru fundal și animații
        self.canvas = tk.Canvas(
            self.root,
            bg='#000000',
            highlightthickness=0,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crează conținutul
        self.create_background()
        self.create_text()
        self.create_buttons()
        
        # Centrează fereastra
        self.center_window()
        
        # Variabile animație
        self.angle = 0
        self.time = 0
        
        # Pornește animațiile
        self.animate()
        
        # Evenimente mouse
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        
        self.root.mainloop()
    
    def create_background(self):
        """Creează fundalul cu gradient și efecte"""
        # Gradient fundal
        self.bg_gradient = self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="#0a0a1a",
            outline=""
        )
        
        # Linii decorative animatate
        self.lines = []
        colors = ["#00ffaa20", "#00aaff20", "#aa00ff20"]
        for i in range(3):
            line = self.canvas.create_line(
                0, 50 + i*30, self.width, 50 + i*30,
                fill=colors[i],
                width=1
            )
            self.lines.append(line)
    
    def create_text(self):
        """Creează textul BRF și BotRobloxFarm"""
        # BRF text - MARE și centrat
        self.brf_font = font.Font(family="Segoe UI", size=64, weight="bold")
        self.brf_text = self.canvas.create_text(
            self.width//2, self.height//2 - 30,
            text="BRF",
            font=self.brf_font,
            fill="#00ffaa",
            anchor="center"
        )
        
        # BotRobloxFarm text
        self.sub_font = font.Font(family="Segoe UI", size=22, weight="normal")
        self.sub_text = self.canvas.create_text(
            self.width//2, self.height//2 + 30,
            text="BotRobloxFarm",
            font=self.sub_font,
            fill="#88ffcc",
            anchor="center"
        )
        
        # Linie subțire sub text
        self.canvas.create_line(
            self.width//2 - 100, self.height//2 + 60,
            self.width//2 + 100, self.height//2 + 60,
            fill="#00ffaa40",
            width=1
        )
    
    def create_buttons(self):
        """Creează butoanele X și -"""
        # Frame pentru butoane (transparent)
        self.button_frame = tk.Frame(self.canvas, bg='#00000000')
        self.button_frame.place(x=self.width-80, y=10, width=70, height=30)
        
        # Buton Minimize (-)
        self.min_btn = tk.Button(
            self.button_frame,
            text="–",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#4488ff",
            activebackground="#66aaff",
            activeforeground="white",
            bd=0,
            width=2,
            height=1,
            command=self.root.iconify
        )
        self.min_btn.pack(side=tk.LEFT, padx=2)
        
        # Buton Close (X)
        self.close_btn = tk.Button(
            self.button_frame,
            text="×",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#ff4444",
            activebackground="#ff6666",
            activeforeground="white",
            bd=0,
            width=2,
            height=1,
            command=self.root.destroy
        )
        self.close_btn.pack(side=tk.LEFT, padx=2)
        
        # Text mic în colț
        self.canvas.create_text(
            10, self.height - 10,
            text="v2.0",
            font=("Arial", 8),
            fill="#444444",
            anchor="sw"
        )
    
    def center_window(self):
        """Centrează fereastra"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def start_move(self, event):
        """Începe glisarea"""
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        """Glisează fereastra"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def animate(self):
        """Animații continue"""
        self.time += 0.05
        
        # 1. Pulsare text BRF
        pulse = (math.sin(self.time * 1.5) + 1) / 2
        r = int(pulse * 50)
        g = 255
        b = int(170 + pulse * 85)
        brf_color = f'#{r:02x}{g:02x}{b:02x}'
        self.canvas.itemconfig(self.brf_text, fill=brf_color)
        
        # 2. Animație linii fundal
        for i, line in enumerate(self.lines):
            offset = math.sin(self.time + i) * 10
            y_pos = 50 + i*30 + offset
            self.canvas.coords(line, 0, y_pos, self.width, y_pos)
        
        # 3. Gradient animat
        gradient_phase = math.sin(self.time * 0.3) * 0.1 + 0.5
        dark = int(10 * gradient_phase)
        gradient_color = f'#{dark:02x}0a{int(26*gradient_phase):02x}'
        self.canvas.itemconfig(self.bg_gradient, fill=gradient_color)
        
        # 4. Efect de "glow" pe text
        glow_size = abs(math.sin(self.time)) * 3
        self.canvas.itemconfig(self.brf_text, font=("Segoe UI", 64 + int(glow_size), "bold"))
        
        # Continuă animația
        self.root.after(50, self.animate)

# Rulează aplicația
if __name__ == "__main__":
    app = BRFMenu()
