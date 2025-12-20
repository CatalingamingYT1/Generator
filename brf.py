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
        
        # Permite redimensionarea și face să funcționeze bine minimize/maximize
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
        
        # Frame principal care se extinde
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0A0A1E")
        self.main_frame.pack(fill="both", expand=True)
        
        # Canvas pentru fundal și text
        self.canvas = ctk.CTkCanvas(
            self.main_frame,
            bg="#0A0A1E",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Creare text inițial
        self.create_text()
        
        # Centrare inițială
        self.center_window()
        
        # Pornește animațiile
        self.root.after(100, self.animate_background)
        self.root.after(2000, self.animate_colors)
        
        # Bind pentru redimensionare și minimize/restore
        self.root.bind("<Configure>", self.on_resize)
        
        # Track pentru minimize/maximize
        self.last_state = "normal"
        
        # Rulează aplicația
        self.root.mainloop()
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        width = 800
        height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_text(self):
        """Creează sau re-creează textul"""
        # Șterge textul vechi dacă există
        if hasattr(self, 'text_shadow'):
            self.canvas.delete(self.text_shadow)
        if hasattr(self, 'text_main'):
            self.canvas.delete(self.text_main)
        
        # Dimensiuni canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Dacă canvas-ul nu are încă dimensiuni, folosește default
        if width <= 1:
            width = 800
        if height <= 1:
            height = 400
        
        # Calculează dimensiunea fontului
        font_size = self.calculate_font_size(width, height)
        
        # Text principal cu umbră
        self.text_shadow = self.canvas.create_text(
            width // 2 + 3,
            height // 2 + 3,
            text="BotRobloxFarm(BRF)",
            font=("Arial", font_size, "bold"),
            fill="#000000",
            anchor="center"
        )
        
        # Text principal
        self.text_main = self.canvas.create_text(
            width // 2,
            height // 2,
            text="BotRobloxFarm(BRF)",
            font=("Arial", font_size, "bold"),
            fill=self.colors[self.color_index],
            anchor="center"
        )
    
    def calculate_font_size(self, width, height):
        """Calculează dimensiunea optimă a fontului"""
        min_font = 12  # Minimum când fereastra e foarte mică
        max_font = 72  # Maximum când fereastra e foarte mare
        
        # Folosește dimensiunea mai mică pentru a se potrivi
        min_dimension = min(width, height)
        
        # Formula pentru scalare: între 12 și 72 bazat pe dimensiune
        if min_dimension <= 200:
            return min_font
        elif min_dimension >= 1000:
            return max_font
        else:
            # Scalare lineară între 200 și 1000
            scale = (min_dimension - 200) / (1000 - 200)
            return int(min_font + scale * (max_font - min_font))
    
    def animate_background(self):
        """Animează fundalul cu efect de particule"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Verifică dacă fereastra este vizibilă (nu minimizată)
        if self.root.state() != "iconic" and width > 10 and height > 10:
            # Adaugă puncte strălucitoare random
            for _ in range(3):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, 2)
                
                # Punct strălucitor
                self.canvas.create_oval(
                    x, y, x + size, y + size,
                    fill="#FFFFFF",
                    outline="",
                    tags="particle"
                )
            
            # Șterge particulele vechi
            old_particles = self.canvas.find_withtag("old_particle")
            for particle in old_particles:
                self.canvas.delete(particle)
            
            # Marchează particulele curente ca vechi
            particles = self.canvas.find_withtag("particle")
            for particle in particles:
                self.canvas.addtag_withtag("old_particle", particle)
        
        # Repetă animația
        self.root.after(150, self.animate_background)
    
    def animate_colors(self):
        """Animează schimbarea culorii textului"""
        # Doar dacă fereastra nu e minimizată
        if self.root.state() != "iconic":
            self.color_index = (self.color_index + 1) % len(self.colors)
            
            # Schimbă culoarea textului principal
            self.canvas.itemconfig(self.text_main, fill=self.colors[self.color_index])
            
            # Schimbă și umbra ușor
            shadow_color = self.darken_color(self.colors[self.color_index], 50)
            self.canvas.itemconfig(self.text_shadow, fill=shadow_color)
        
        # Repetă animația
        self.root.after(2000, self.animate_colors)
    
    def darken_color(self, hex_color, amount):
        """Întunecă o culoare HEX"""
        hex_color = hex_color.lstrip('#')
        r = max(0, int(hex_color[0:2], 16) - amount)
        g = max(0, int(hex_color[2:4], 16) - amount)
        b = max(0, int(hex_color[4:6], 16) - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_resize(self, event):
        """Reactualizează textul la redimensionare sau minimize/restore"""
        if event.widget == self.root:
            current_state = self.root.state()
            
            # Dacă s-a schimbat starea (minimize/restore/maximize)
            if current_state != self.last_state:
                self.last_state = current_state
                
                # Dacă s-a restaurat din minimize, re-crează textul
                if current_state == "normal":
                    self.root.after(100, self.update_text)
            
            # Pentru redimensionare normală
            elif current_state == "normal":
                self.update_text()
    
    def update_text(self):
        """Actualizează textul"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width > 10 and height > 10:  # Doar dacă e vizibil
            # Calculează dimensiunea fontului
            font_size = self.calculate_font_size(width, height)
            
            # Actualizează poziția textului
            self.canvas.coords(self.text_shadow, width // 2 + 3, height // 2 + 3)
            self.canvas.coords(self.text_main, width // 2, height // 2)
            
            # Actualizează dimensiunea fontului
            self.canvas.itemconfig(self.text_shadow, font=("Arial", font_size, "bold"))
            self.canvas.itemconfig(self.text_main, font=("Arial", font_size, "bold"))

# Rulează aplicația
if __name__ == "__main__":
    app = BRFApp()
