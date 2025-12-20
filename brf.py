import customtkinter as ctk
import random
import math

class ChristmasBRFApp:
    def __init__(self):
        # Configurare CustomTkinter
        ctk.set_appearance_mode("dark")
        
        # Creare fereastră
        self.root = ctk.CTk()
        self.root.title("🎄 BRF Christmas 🎄")
        self.root.geometry("800x400")
        
        # Permite redimensionarea
        self.root.resizable(True, True)
        
        # Culori de Crăciun
        self.christmas_colors = [
            "#FF0000",  # Roșu
            "#00FF00",  # Verde
            "#FFFFFF",  # Alb
            "#FFD700",  # Auriu
            "#1E90FF",  # Albastru deschis
        ]
        
        # Variabile
        self.color_index = 0
        self.snowflakes = []
        self.text_objects = []
        
        # Frame principal care se extinde
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0A1F0A")
        self.main_frame.pack(fill="both", expand=True)
        
        # Canvas pentru animații
        self.canvas = ctk.CTkCanvas(
            self.main_frame,
            bg="#0A1F0A",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Centrare fereastră
        self.center_window()
        
        # Creează designul inițial
        self.create_christmas_design()
        
        # Creează textul
        self.create_centered_text()
        
        # Pornește animațiile
        self.root.after(50, self.animate_snow)
        self.root.after(2000, self.animate_text_colors)
        
        # Bind pentru toate evenimentele de redimensionare
        self.root.bind("<Configure>", self.on_window_change)
        
        # Track starea ferestrei
        self.last_state = "normal"
        self.last_size = (800, 400)
        
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
    
    def create_christmas_design(self):
        """Creează designul de Crăciun"""
        # Adaugă stele
        self.create_stars()
        
        # Adaugă fulgi inițiali
        self.create_initial_snowflakes()
    
    def create_stars(self):
        """Creează stele pe fundal"""
        width = self.canvas.winfo_width() or 800
        height = self.canvas.winfo_height() or 400
        
        for _ in range(25):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            brightness = random.randint(100, 200)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            
            self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline="",
                tags="star"
            )
    
    def create_initial_snowflakes(self):
        """Creează fulgi de zăpadă inițiali"""
        width = self.canvas.winfo_width() or 800
        height = self.canvas.winfo_height() or 400
        
        for _ in range(40):
            self.add_snowflake(width, height)
    
    def add_snowflake(self, width, height):
        """Adaugă un fulg de zăpadă"""
        x = random.randint(0, width)
        y = random.randint(-50, 0)
        size = random.randint(2, 5)
        
        snowflake = self.canvas.create_oval(
            x, y, x + size, y + size,
            fill="#FFFFFF",
            outline="",
            tags="snowflake"
        )
        
        self.snowflakes.append({
            "id": snowflake,
            "x": x,
            "y": y,
            "size": size,
            "speed": random.uniform(0.5, 1.5),
            "sway": random.uniform(-0.5, 0.5)
        })
    
    def create_centered_text(self):
        """Creează textul PERFECT centrat"""
        # Șterge textul vechi dacă există
        for obj in self.text_objects:
            self.canvas.delete(obj)
        self.text_objects.clear()
        
        # Obține dimensiunile canvas-ului
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Dacă canvas-ul nu are încă dimensiuni, folosește default
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 800
            canvas_height = 400
        
        # Calculează dimensiunea fontului bazată pe cea mai mică dimensiune
        min_dimension = min(canvas_width, canvas_height)
        font_size = max(20, min(60, min_dimension // 15))
        shadow_offset = max(2, font_size // 25)
        
        # Coordonatele exacte ale centrului
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Text cu umbră (primul strat - fundal)
        shadow_text = self.canvas.create_text(
            center_x + shadow_offset,
            center_y + shadow_offset,
            text="BotRobloxFarm(BRF)",
            font=("Arial", font_size, "bold"),
            fill="#8B0000",  # Roșu închis
            anchor="center"
        )
        self.text_objects.append(shadow_text)
        
        # Text principal (al doilea strat)
        main_text = self.canvas.create_text(
            center_x,
            center_y,
            text="BotRobloxFarm(BRF)",
            font=("Arial", font_size, "bold"),
            fill=self.christmas_colors[self.color_index],
            anchor="center"
        )
        self.text_objects.append(main_text)
        
        # Subtitlu de Crăciun (al treilea strat)
        subtitle_font = max(12, font_size // 3)
        subtitle = self.canvas.create_text(
            center_x,
            center_y + font_size + 10,
            text="🎄 Merry Christmas! 🎅",
            font=("Arial", subtitle_font, "bold"),
            fill="#FFD700",
            anchor="center"
        )
        self.text_objects.append(subtitle)
    
    def animate_snow(self):
        """Animează fulgii de zăpadă"""
        # Doar dacă fereastra este vizibilă
        if self.root.state() != "iconic":
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 10 and canvas_height > 10:
                # Mișcă fulgii existenți
                for snowflake in self.snowflakes[:]:
                    snowflake["y"] += snowflake["speed"]
                    snowflake["x"] += snowflake["sway"]
                    
                    # Dacă fulgul a ieșit din ecran
                    if (snowflake["y"] > canvas_height or 
                        snowflake["x"] < 0 or 
                        snowflake["x"] > canvas_width):
                        
                        self.canvas.delete(snowflake["id"])
                        self.snowflakes.remove(snowflake)
                        self.add_snowflake(canvas_width, canvas_height)
                    else:
                        # Actualizează poziția
                        self.canvas.coords(
                            snowflake["id"],
                            snowflake["x"], snowflake["y"],
                            snowflake["x"] + snowflake["size"], 
                            snowflake["y"] + snowflake["size"]
                        )
                
                # Adaugă fulgi noi dacă sunt prea puțini
                if len(self.snowflakes) < 50 and random.random() < 0.2:
                    self.add_snowflake(canvas_width, canvas_height)
        
        # Repetă animația
        self.root.after(40, self.animate_snow)
    
    def animate_text_colors(self):
        """Animează schimbarea culorii textului"""
        if self.root.state() != "iconic":
            self.color_index = (self.color_index + 1) % len(self.christmas_colors)
            
            # Actualizează textul principal (al doilea obiect)
            if len(self.text_objects) >= 2:
                self.canvas.itemconfig(
                    self.text_objects[1],  # Textul principal
                    fill=self.christmas_colors[self.color_index]
                )
        
        # Repetă animația
        self.root.after(1500, self.animate_text_colors)
    
    def on_window_change(self, event):
        """Gestionează TOATE schimbările ferestrei"""
        if event.widget == self.root:
            current_state = self.root.state()
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            
            # Dacă dimensiunea s-a schimbat semnificativ sau starea
            size_changed = (
                abs(current_width - self.last_size[0]) > 5 or
                abs(current_height - self.last_size[1]) > 5
            )
            
            state_changed = current_state != self.last_state
            
            if size_changed or state_changed:
                # Actualizează starea și dimensiunea
                self.last_state = current_state
                self.last_size = (current_width, current_height)
                
                # Dacă fereastra este vizibilă (nu minimizată)
                if current_state == "normal" or current_state == "zoomed":
                    # Re-crează textul centrat după o scurtă întârziere
                    self.root.after(10, self.recenter_text)
    
    def recenter_text(self):
        """Re-centrează textul în mijloc"""
        # Forțează canvas-ul să se actualizeze
        self.canvas.update_idletasks()
        
        # Re-crează textul centrat
        self.create_centered_text()
        
        # Re-crează stelele dacă canvas-ul s-a schimbat mult
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 10 and canvas_height > 10:
            # Șterge stelele vechi
            self.canvas.delete("star")
            
            # Adaugă stele noi pentru noua dimensiune
            for _ in range(25):
                x = random.randint(0, canvas_width)
                y = random.randint(0, canvas_height)
                size = random.randint(1, 3)
                brightness = random.randint(100, 200)
                color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
                
                self.canvas.create_oval(
                    x, y, x + size, y + size,
                    fill=color,
                    outline="",
                    tags="star"
                )

# Rulează aplicația
if __name__ == "__main__":
    app = ChristmasBRFApp()
