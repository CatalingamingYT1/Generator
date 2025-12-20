import tkinter as tk
from tkinter import font
import math

class SimpleBRFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRF")
        self.root.geometry("500x250")
        self.root.configure(bg="#000000")
        
        # Fă fereastra mereu deasupra (opțional)
        self.root.attributes('-topmost', True)
        
        # Elimină bara de titlu pentru look curat
        self.root.overrideredirect(False)  # LASĂ BARA DE TITLU normală!
        
        # Frame principal
        self.main_frame = tk.Frame(root, bg="#000000")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crează textul
        self.create_text()
        
        # Centrează
        self.center_window()
        
        # Animație
        self.animate()
    
    def create_text(self):
        """Crează textul simplu și mare"""
        # TEXT PRINCIPAL "BRF" - FOARTE MARE
        self.brf_label = tk.Label(
            self.main_frame,
            text="BRF",
            font=("Arial", 64, "bold"),
            fg="#00FFAA",
            bg="#000000"
        )
        self.brf_label.pack(pady=(10, 0))
        
        # TEXT "BotRobloxFarm"
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="BotRobloxFarm",
            font=("Arial", 24),
            fg="#888888",
            bg="#000000"
        )
        self.subtitle_label.pack(pady=(5, 20))
        
        # TEXT "System online..."
        self.status_label = tk.Label(
            self.main_frame,
            text="▶ SYSTEM ONLINE",
            font=("Consolas", 16),
            fg="#00FF88",
            bg="#000000"
        )
        self.status_label.pack()
    
    def center_window(self):
        """Centrează fereastra"""
        self.root.update_idletasks()
        width = 500
        height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def animate(self):
        """Animație simplă de pulsare"""
        import time
        t = time.time()
        
        # Pulsare pentru "BRF"
        pulse = (math.sin(t * 2) + 1) / 2  # 0 to 1
        r = 0
        g = 255
        b = int(pulse * 100 + 155)
        color = f'#{r:02x}{g:02x}{b:02x}'
        self.brf_label.config(fg=color)
        
        # Animație puncte pentru "SYSTEM ONLINE"
        dots = ["   ", ".  ", ".. ", "..."]
        dot_index = int(t * 2) % 4
        self.status_label.config(text=f"▶ SYSTEM ONLINE{dots[dot_index]}")
        
        # Repetă
        self.root.after(100, self.animate)

def main():
    root = tk.Tk()
    app = SimpleBRFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
