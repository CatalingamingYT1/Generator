import tkinter as tk
from tkinter import font

class SimpleBRFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BRF")
        self.root.geometry("400x200")
        
        # Permite orice mărime
        self.root.resizable(True, True)
        
        # Crează canvas pentru fundal simplu
        self.canvas = tk.Canvas(
            self.root,
            bg="#1a1a1a",  # Fundal gri închis simplu
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Crează textul
        self.create_text()
        
        # Centrare inițială
        self.center_window()
        
        # Bind pentru redimensionare
        self.root.bind("<Configure>", self.on_resize)
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        width = 400
        height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_text(self):
        """Crează textul simplu"""
        # Font simplu
        self.main_font = font.Font(
            family="Arial",
            size=36,
            weight="bold"
        )
        
        # Text simplu
        self.main_text = self.canvas.create_text(
            200, 100,
            text="BotRobloxFarm(BRF)",
            font=self.main_font,
            fill="#ffffff",  # Alb simplu
            anchor="center"
        )
    
    def on_resize(self, event):
        """Actualizează poziția textului la redimensionare"""
        if event.widget == self.root:
            width = event.width
            height = event.height
            
            # Actualizează poziția textului (centru)
            self.canvas.coords(self.main_text, width // 2, height // 2)
            
            # Ajustează dimensiunea fontului în funcție de mărime
            if width > 0 and height > 0:
                # Calculează dimensiunea fontului bazată pe cea mai mică dimensiune
                min_dimension = min(width, height)
                font_size = max(12, min_dimension // 12)  # Min 12px, max în funcție de dimensiune
                font_size = min(font_size, 72)  # Max 72px
                
                self.main_font.configure(size=font_size)

def main():
    root = tk.Tk()
    app = SimpleBRFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
