import customtkinter as ctk
import random

class BRFApp:
    def __init__(self):
        # Configurare CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Creare fereastră
        self.root = ctk.CTk()
        self.root.title("BRF")
        self.root.geometry("800x400")
        
        # Permite redimensionarea
        self.root.resizable(True, True)
        
        # Variabile pentru animație
        self.color_index = 0
        self.colors = [
            "#00FF88",  # Verde strălucitor
            "#00AAFF",  # Albastru deschis
            "#FF8800",  # Portocaliu
            "#FF44AA",  # Roz
            "#8844FF"   # Violet
        ]
        
        # Fundal animat
        self.canvas = ctk.CTkCanvas(
            self.root,
            bg="#0A0A1E",  # Albastru închis
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Creare text
        self.create_text()
        
        # Centrare inițială
        self.center_window()
        
        # Pornește animațiile
        self.root.after(100, self.animate_background)
        self.root.after(2000, self.animate_colors)
        
        # Bind pentru redimensionare
        self.root.bind("<Configure>", self.on_resize)
        
        # Rulează aplicația
        self.root.mainloop()
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_text(self):
        """Creează textul animat"""
        # Coordonate centru
        width = self.canvas.winfo_width() or 800
        height = self.canvas.winfo_height() or 400
        
        # Text principal cu umbră
        self.text_shadow = self.canvas.create_text(
            width // 2 + 4,
            height // 2 + 4,
            text="BotRobloxFarm(BRF)",
            font=("Arial", 48, "bold"),
            fill="#000000"
        )
        
        # Text principal
        self.text_main = self.canvas.create_text(
            width // 2,
            height // 2,
            text="BotRobloxFarm(BRF)",
            font=("Arial", 48, "bold"),
            fill=self.colors[0]
        )
    
    def animate_background(self):
        """Animează fundalul cu efect de particule"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width > 0 and height > 0:
            # Adaugă puncte strălucitoare random
            for _ in range(5):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, 3)
                
                # Punct strălucitor
                self.canvas.create_oval(
                    x, y, x + size, y + size,
                    fill="#FFFFFF",
                    outline="",
                    tags="particle"
                )
            
            # Șterge particulele vechi
            self.canvas.delete("old_particle")
            
            # Marchează particulele curente ca vechi
            particles = self.canvas.find_withtag("particle")
            for particle in particles:
                self.canvas.addtag_withtag("old_particle", particle)
        
        # Repetă animația
        self.root.after(100, self.animate_background)
    
    def animate_colors(self):
        """Animează schimbarea culorii textului"""
        self.color_index = (self.color_index + 1) % len(self.colors)
        
        # Schimbă culoarea textului principal
        self.canvas.itemconfig(self.text_main, fill=self.colors[self.color_index])
        
        # Schimbă și umbra ușor
        shadow_color = f"#{max(0, int(self.colors[self.color_index][1:3], 16) - 50):02x}" \
                      f"{max(0, int(self.colors[self.color_index][3:5], 16) - 50):02x}" \
                      f"{max(0, int(self.colors[self.color_index][5:7], 16) - 50):02x}"
        self.canvas.itemconfig(self.text_shadow, fill=shadow_color)
        
        # Repetă animația
        self.root.after(2000, self.animate_colors)
    
    def on_resize(self, event):
        """Reactualizează textul la redimensionare"""
        if event.widget == self.root:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            if width > 0 and height > 0:
                # Actualizează poziția textului
                self.canvas.coords(self.text_shadow, width // 2 + 4, height // 2 + 4)
                self.canvas.coords(self.text_main, width // 2, height // 2)
                
                # Ajustează dimensiunea fontului
                font_size = min(72, max(24, min(width, height) // 15))
                self.canvas.itemconfig(self.text_shadow, font=("Arial", font_size, "bold"))
                self.canvas.itemconfig(self.text_main, font=("Arial", font_size, "bold"))

# Rulează aplicația
if __name__ == "__main__":
    app = BRFApp()
