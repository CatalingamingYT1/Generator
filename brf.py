import customtkinter as ctk
import random
import math

class ChristmasBRFApp:
    def __init__(self):
        # Configurare CustomTkinter
        ctk.set_appearance_mode("dark")
        
        # Creare fereastră
        self.root = ctk.CTk()
        self.root.title("🎄 BRF Christmas Edition 🎄")
        self.root.geometry("900x500")
        
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
        
        # Variabile pentru animație
        self.color_index = 0
        self.snowflakes = []
        self.lights = []
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0A1F0A")  # Verde închis de Crăciun
        self.main_frame.pack(fill="both", expand=True)
        
        # Canvas pentru fundal și animații
        self.canvas = ctk.CTkCanvas(
            self.main_frame,
            bg="#0A1F0A",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Creare design de Crăciun
        self.create_christmas_design()
        
        # Creare text
        self.create_text()
        
        # Centrare fereastră
        self.center_window()
        
        # Pornește animațiile
        self.root.after(50, self.animate_snow)
        self.root.after(100, self.animate_lights)
        self.root.after(2000, self.animate_text_colors)
        
        # Bind pentru redimensionare
        self.root.bind("<Configure>", self.on_resize)
        
        # Rulează aplicația
        self.root.mainloop()
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        width = 900
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_christmas_design(self):
        """Creează designul de Crăciun"""
        # Adaugă stele pe fundal
        self.create_stars()
        
        # Adaugă luminioare decorative
        self.create_christmas_lights()
        
        # Adaugă fulgi de zăpadă inițiali
        self.create_initial_snowflakes()
    
    def create_stars(self):
        """Creează stele sclipitoare pe fundal"""
        width = self.canvas.winfo_width() or 900
        height = self.canvas.winfo_height() or 500
        
        for _ in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            brightness = random.randint(150, 255)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            
            star = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline="",
                tags="star"
            )
    
    def create_christmas_lights(self):
        """Creează luminioare de Crăciun"""
        width = self.canvas.winfo_width() or 900
        
        # Creează șir de luminioare
        num_lights = 20
        spacing = width / num_lights
        
        for i in range(num_lights):
            x = i * spacing + spacing / 2
            y = 30
            
            light = self.canvas.create_oval(
                x - 8, y - 8, x + 8, y + 8,
                fill=random.choice(self.christmas_colors),
                outline="gold",
                width=2,
                tags="light"
            )
            
            # Linie între luminioare
            if i > 0:
                self.canvas.create_line(
                    x - spacing, y, x, y,
                    fill="gold",
                    width=2,
                    tags="light_wire"
                )
            
            self.lights.append({
                "id": light,
                "x": x,
                "y": y,
                "color_index": random.randint(0, len(self.christmas_colors)-1),
                "pulse_direction": 1
            })
    
    def create_initial_snowflakes(self):
        """Creează fulgi de zăpadă inițiali"""
        width = self.canvas.winfo_width() or 900
        height = self.canvas.winfo_height() or 500
        
        for _ in range(50):
            self.add_snowflake(width, height)
    
    def add_snowflake(self, width, height):
        """Adaugă un fulg de zăpadă"""
        x = random.randint(0, width)
        y = random.randint(-50, 0)  # Încep de deasupra ecranului
        size = random.randint(2, 6)
        
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
            "speed": random.uniform(0.5, 2.0),
            "sway": random.uniform(-1, 1)  # Mișcare laterală
        })
    
    def create_text(self):
        """Creează textul principal"""
        width = self.canvas.winfo_width() or 900
        height = self.canvas.winfo_height() or 500
        
        # Dimensiune font bazată pe dimensiunea ferestrei
        font_size = self.calculate_font_size(width, height)
        
        # Efect de umbră pentru text
        shadow_offset = max(3, font_size // 20)
        
        # Text cu umbră roșie de Crăciun
        self.text_shadow = self.canvas.create_text(
            width // 2 + shadow_offset,
            height // 2 + shadow_offset,
            text="BotRobloxFarm(BRF)",
            font=("Arial", font_size, "bold"),
            fill="#8B0000",  # Roșu închis
            anchor="center"
        )
        
        # Text principal cu efect de strălucire
        self.text_main = self.canvas.create_text(
            width // 2,
            height // 2,
            text="BotRobloxFarm(BRF)",
            font=("Arial", font_size, "bold"),
            fill=self.christmas_colors[0],
            anchor="center"
        )
        
        # Subtitlu festiv
        self.subtitle = self.canvas.create_text(
            width // 2,
            height // 2 + font_size,
            text="🎅 Merry Christmas! 🎁",
            font=("Arial", font_size // 3, "bold"),
            fill="#FFD700",  # Auriu
            anchor="center"
        )
    
    def calculate_font_size(self, width, height):
        """Calculează dimensiunea fontului"""
        min_dimension = min(width, height)
        return max(24, min(72, min_dimension // 12))
    
    def animate_snow(self):
        """Animează fulgii de zăpadă"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width > 10 and height > 10:
            # Mișcă fulgii existenți
            for snowflake in self.snowflakes[:]:
                snowflake["y"] += snowflake["speed"]
                snowflake["x"] += snowflake["sway"] * 0.5
                
                # Dacă fulgul a ieșit din ecran, îl reinițializează
                if snowflake["y"] > height or snowflake["x"] < 0 or snowflake["x"] > width:
                    self.canvas.delete(snowflake["id"])
                    self.snowflakes.remove(snowflake)
                    self.add_snowflake(width, height)
                else:
                    # Actualizează poziția
                    self.canvas.coords(
                        snowflake["id"],
                        snowflake["x"], snowflake["y"],
                        snowflake["x"] + snowflake["size"], snowflake["y"] + snowflake["size"]
                    )
            
            # Adaugă fulgi noi ocazional
            if len(self.snowflakes) < 100 and random.random() < 0.3:
                self.add_snowflake(width, height)
        
        # Repetă animația
        self.root.after(30, self.animate_snow)
    
    def animate_lights(self):
        """Animează luminioarele de Crăciun"""
        for light in self.lights:
            # Pulsare culori
            light["color_index"] = (light["color_index"] + 1) % len(self.christmas_colors)
            
            # Schimbă culoarea
            self.canvas.itemconfig(
                light["id"],
                fill=self.christmas_colors[light["color_index"]]
            )
            
            # Efect de pulsare (mărire/micșorare)
            current_coords = self.canvas.coords(light["id"])
            if len(current_coords) == 4:
                current_size = current_coords[2] - current_coords[0]
                
                if current_size > 12:
                    light["pulse_direction"] = -1
                elif current_size < 8:
                    light["pulse_direction"] = 1
                
                new_size = current_size + light["pulse_direction"] * 0.2
                x_center = light["x"]
                y_center = light["y"]
                
                self.canvas.coords(
                    light["id"],
                    x_center - new_size/2, y_center - new_size/2,
                    x_center + new_size/2, y_center + new_size/2
                )
        
        # Repetă animația
        self.root.after(500, self.animate_lights)
    
    def animate_text_colors(self):
        """Animează schimbarea culorii textului"""
        self.color_index = (self.color_index + 1) % len(self.christmas_colors)
        
        # Schimbă culoarea textului principal
        self.canvas.itemconfig(
            self.text_main,
            fill=self.christmas_colors[self.color_index]
        )
        
        # Schimbă și umbra
        shadow_color = self.darken_color(self.christmas_colors[self.color_index], 80)
        self.canvas.itemconfig(self.text_shadow, fill=shadow_color)
        
        # Repetă animația
        self.root.after(1500, self.animate_text_colors)
    
    def darken_color(self, hex_color, amount):
        """Întunecă o culoare HEX"""
        hex_color = hex_color.lstrip('#')
        r = max(0, int(hex_color[0:2], 16) - amount)
        g = max(0, int(hex_color[2:4], 16) - amount)
        b = max(0, int(hex_color[4:6], 16) - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_resize(self, event):
        """Reactualizează totul la redimensionare"""
        if event.widget == self.root and self.root.state() == "normal":
            # Re-crează tot designul
            self.recreate_design()
    
    def recreate_design(self):
        """Re-crează întregul design pentru noua dimensiune"""
        # Șterge tot
        self.canvas.delete("all")
        self.snowflakes.clear()
        self.lights.clear()
        
        # Re-crează totul
        self.create_christmas_design()
        self.create_text()
        
        # Restart animații
        self.root.after(100, self.animate_lights)

# Rulează aplicația
if __name__ == "__main__":
    app = ChristmasBRFApp()
