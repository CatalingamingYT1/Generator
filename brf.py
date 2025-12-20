import tkinter as tk
from tkinter import font
import math

class CoolBRFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRF")
        self.root.geometry("500x300")
        self.root.configure(bg="#0a0a0a")
        
        # Elimină bordurile ferestrei pentru un look modern
        self.root.overrideredirect(True)
        
        # Pentru a putea muta fereastra fără borduri
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)
        self.root.bind("<Button-3>", lambda e: self.root.destroy())  # Right-click to close
        
        # Variabile pentru animații
        self.angle = 0
        self.pulse_phase = 0
        self.glow_phase = 0
        
        # Canvas pentru efecte
        self.canvas = tk.Canvas(
            self.root,
            bg="#0a0a0a",
            highlightthickness=0,
            width=500,
            height=300
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crează elemente grafice
        self.create_background()
        self.create_text()
        self.create_subtitle()
        
        # Centrează fereastra
        self.center_window()
        
        # Porneste animațiile
        self.animate()
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def center_window(self):
        self.root.update_idletasks()
        width = 500
        height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_background(self):
        # Efect de particule simple
        self.particles = []
        for _ in range(20):
            x = tk.Frame(self.root, width=2, height=2, bg="#00ffaa")
            x.place(x=tk._random.randint(0, 500), y=tk._random.randint(0, 300))
            self.particles.append(x)
    
    def create_text(self):
        # Font modern și mare
        self.main_font = font.Font(
            family="Segoe UI",
            size=48,
            weight="bold"
        )
        
        # Text principal cu efect de umbră
        self.main_text = self.canvas.create_text(
            250, 100,
            text="BRF",
            font=self.main_font,
            fill="#00ffaa",  # Cyan neon
            anchor="center"
        )
        
        # Text secundar mai mic
        self.sub_font = font.Font(
            family="Segoe UI",
            size=18,
            weight="normal"
        )
        
        self.sub_text = self.canvas.create_text(
            250, 150,
            text="BotRobloxFarm",
            font=self.sub_font,
            fill="#888888",
            anchor="center"
        )
    
    def create_subtitle(self):
        # Linie decorativă
        self.canvas.create_line(150, 180, 350, 180, fill="#00ffaa", width=2)
        
        # Text status animat
        self.status_font = font.Font(
            family="Consolas",
            size=14,
            weight="normal"
        )
        
        self.status_text = self.canvas.create_text(
            250, 210,
            text="▶ SYSTEM ONLINE",
            font=self.status_font,
            fill="#00ff88",
            anchor="center"
        )
    
    def animate(self):
        # Animație text principal (pulsare)
        self.pulse_phase += 0.1
        pulse = abs(math.sin(self.pulse_phase)) * 0.2 + 0.8
        
        # Animație glow (schimbare culoare)
        self.glow_phase += 0.05
        r = int(abs(math.sin(self.glow_phase)) * 100 + 155)
        g = 255
        b = int(abs(math.sin(self.glow_phase + 1)) * 100 + 155)
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        # Aplică efectele
        self.canvas.itemconfig(self.main_text, fill=color)
        
        # Animație status text
        dots = ["   ", ".  ", ".. ", "..."]
        dot_index = int(self.pulse_phase * 2) % 4
        status_base = "SYSTEM ONLINE"
        self.canvas.itemconfig(self.status_text, text=f"▶ {status_base}{dots[dot_index]}")
        
        # Animație particule
        for i, particle in enumerate(self.particles):
            x = particle.winfo_x()
            y = particle.winfo_y() + 1
            if y > 300:
                y = 0
                x = tk._random.randint(0, 500)
            particle.place(x=x, y=y)
            
            # Efect de transparență
            alpha = abs(math.sin(self.pulse_phase + i * 0.3))
            color = f'#{int(alpha*100):02x}ff{int(alpha*200):02x}'
            particle.configure(bg=color)
        
        # Continuă animația
        self.root.after(50, self.animate)

def main():
    root = tk.Tk()
    
    # Setări pentru transparență (opțional)
    root.attributes('-alpha', 0.95)  # Ușor transparent
    
    app = CoolBRFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
