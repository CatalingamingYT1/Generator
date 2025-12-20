import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import customtkinter as ctk
import threading
import time
import os
import json
import random
import sys
import subprocess
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Set CustomTkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def install_requirements():
    """Instalează pachetele necesare dacă nu sunt deja instalate"""
    required_packages = [
        "selenium",
        "webdriver-manager",
        "colorama",
        "requests",
        "customtkinter"
    ]
    
    print(Fore.CYAN + "╔══════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║         CHECKING/INSTALLING REQUIREMENTS        ║")
    print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(Fore.GREEN + f"✅ {package} is already installed!")
        except ImportError:
            print(Fore.YELLOW + f"📦 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(Fore.GREEN + f"✅ {package} installed successfully!")
                time.sleep(1)
            except:
                print(Fore.RED + f"❌ Failed to install {package}")
    
    print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
    print(Fore.GREEN + "║         ✅ ALL REQUIREMENTS READY!            ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════╝")
    time.sleep(1)

class RobloxAccountCreator:
    def __init__(self, use_proxy=False, proxy=None):
        self.use_proxy = use_proxy
        self.proxy = proxy
        self.driver = None
        self.account_created = False
        self.token = None
        
        # Lista de nume pentru username-uri
        self.first_names = ["Alex", "Max", "Leo", "Sam", "Ryan", "Noah", "Liam", "Ethan", "Mason", "Logan"]
        self.second_names = ["Gamer", "Player", "Pro", "Master", "Legend", "Hero", "Star", "King", "Wolf", "Eagle"]
    
    def setup_driver(self):
        """Configurează și pornește browser-ul Chrome"""
        try:
            chrome_options = Options()
            
            # Setări pentru a evita detectarea bot-ului
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            
            # Adaugă proxy dacă este activat
            if self.use_proxy and self.proxy:
                chrome_options.add_argument(f'--proxy-server={self.proxy}')
            
            # Instalează driver-ul automat
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Ascunde automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
        except Exception as e:
            print(Fore.RED + f"❌ Error setting up driver: {e}")
            return False
    
    def generate_username(self):
        """Generează un username unic"""
        first = random.choice(self.first_names)
        second = random.choice(self.second_names)
        number = random.randint(100, 9999)
        return f"{first}{second}{number}"
    
    def generate_password(self):
        """Generează o parolă puternică"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(12))
    
    def create_account(self):
        """Creează un cont Roblox și extrage token-ul"""
        try:
            # Generează datele contului
            username = self.generate_username()
            password = self.generate_password()
            
            print(Fore.CYAN + f"🔄 Creating account: {username}")
            
            # Navighează la pagina de signup
            self.driver.get("https://www.roblox.com/")
            time.sleep(3)
            
            # Găsește și apasă butonul de signup
            try:
                signup_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='/signup']"))
                )
                signup_btn.click()
            except:
                self.driver.get("https://www.roblox.com/signup")
            
            time.sleep(2)
            
            # Completează data nașterii (peste 13 ani)
            try:
                # Month
                month_dropdown = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//select[@id='MonthDropdown']"))
                )
                month_dropdown.click()
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, "//option[text()='January']").click()
                
                # Day
                day_dropdown = self.driver.find_element(By.XPATH, "//select[@id='DayDropdown']")
                day_dropdown.click()
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, "//option[text()='15']").click()
                
                # Year
                year_dropdown = self.driver.find_element(By.XPATH, "//select[@id='YearDropdown']")
                year_dropdown.click()
                time.sleep(0.5)
                self.driver.find_element(By.XPATH, "//option[text()='2000']").click()
            except:
                pass
            
            time.sleep(1)
            
            # Completează username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='signup-username']"))
            )
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(0.05)
            
            time.sleep(1)
            
            # Completează password
            password_field = self.driver.find_element(By.XPATH, "//input[@id='signup-password']")
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(0.05)
            
            time.sleep(1)
            
            # Alege gen (opțional)
            try:
                gender_btn = self.driver.find_element(By.XPATH, "//input[@value='2']")
                gender_btn.click()
            except:
                pass
            
            time.sleep(1)
            
            # Apasă butonul de signup
            signup_btn = self.driver.find_element(By.XPATH, "//button[@id='signup-button']")
            signup_btn.click()
            
            print(Fore.YELLOW + "⏳ Waiting for account creation...")
            time.sleep(8)
            
            # Verifică dacă contul a fost creat
            if "home" in self.driver.current_url or "welcome" in self.driver.current_url:
                print(Fore.GREEN + "✅ Account created successfully!")
                
                # Extrage token-ul .ROBLOSECURITY
                self.token = self.extract_token()
                
                if self.token:
                    print(Fore.GREEN + "🔐 Token extracted!")
                    self.account_created = True
                    return {
                        "username": username,
                        "password": password,
                        "token": self.token,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                else:
                    print(Fore.RED + "❌ Failed to extract token")
            
            return None
            
        except Exception as e:
            print(Fore.RED + f"❌ Error creating account: {str(e)[:100]}")
            return None
    
    def extract_token(self):
        """Extrage token-ul .ROBLOSECURITY din cookies"""
        try:
            # Navighează pentru a seta cookie-urile
            self.driver.get("https://www.roblox.com/home")
            time.sleep(3)
            
            # Obține toate cookie-urile
            cookies = self.driver.get_cookies()
            
            # Caută token-ul .ROBLOSECURITY
            for cookie in cookies:
                if cookie['name'] == '.ROBLOSECURITY':
                    token = cookie['value']
                    if token.startswith('_|WARNING:-DO-NOT-SHARE-THIS.'):
                        return token
            
            return None
        except:
            return None
    
    def close(self):
        """Închide browser-ul"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

class BRFControlPanel:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🎮 BRF Ultimate Bot Manager v3.0")
        self.root.geometry("1300x750")
        
        # Variabile de stare
        self.farming_active = False
        self.accounts = []
        self.proxies = []
        self.tokens = []
        self.farm_thread = None
        self.total_created = 0
        self.successful_creations = 0
        self.start_time = None
        
        # Configurare layout
        self.setup_layout()
        
        # Încarcă date salvate
        self.load_saved_data()
        
        # Update statistici inițiale
        self.update_stats()
        
        # Centrează fereastra
        self.center_window()
        
        # Verifică și instalează requirements
        threading.Thread(target=self.check_requirements, daemon=True).start()
        
        self.root.mainloop()
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        width = 1300
        height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def check_requirements(self):
        """Verifică și instalează requirements"""
        install_requirements()
    
    def setup_layout(self):
        """Configurează layout-ul aplicației"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Meniu lateral (stânga)
        self.setup_sidebar(main_frame)
        
        # Zona principală (dreapta)
        self.setup_main_area(main_frame)
    
    def setup_sidebar(self, parent):
        """Creează meniul lateral"""
        sidebar = ctk.CTkFrame(parent, width=280, fg_color="#1A1A2E")
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Logo/Titlu
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="🤖",
            font=("Arial", 40)
        ).pack()
        
        ctk.CTkLabel(
            title_frame,
            text="BRF MANAGER",
            font=("Arial", 22, "bold"),
            text_color="#00FF88"
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            title_frame,
            text="Ultimate v3.0",
            font=("Arial", 12),
            text_color="#888888"
        ).pack()
        
        # Separator
        ctk.CTkFrame(sidebar, height=2, fg_color="#444444").pack(fill="x", padx=20, pady=20)
        
        # Butoane meniu
        menu_buttons = [
            ("🚀 MAIN PANEL", self.show_main_panel, "#00AA44"),
            ("🤖 START FARM BOTS", self.show_bots_panel, "#FFAA00"),
            ("🔌 PROXY SETTINGS", self.show_proxy_panel, "#4444AA"),
            ("👤 ACCOUNTS", self.show_accounts_panel, "#AA44AA"),
            ("🔑 TOKENS", self.show_tokens_panel, "#00AAAA"),
            ("📊 STATISTICS", self.show_stats_panel, "#FF4444"),
            ("⚙️ SETTINGS", self.show_settings_panel, "#888888")
        ]
        
        for text, command, color in menu_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 14, "bold"),
                height=45,
                fg_color=color,
                hover_color=color,
                text_color="white",
                anchor="center",
                command=command
            )
            btn.pack(fill="x", padx=15, pady=6)
        
        # Separator
        ctk.CTkFrame(sidebar, height=2, fg_color="#444444").pack(fill="x", padx=20, pady=20)
        
        # Status
        status_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="🟢 SYSTEM STATUS",
            font=("Arial", 12, "bold"),
            text_color="#00FF88"
        ).pack(anchor="w")
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to farm",
            font=("Arial", 11),
            text_color="#888888"
        )
        self.status_label.pack(anchor="w", pady=(5, 0))
        
        # Quick stats
        stats_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.sidebar_stats = ctk.CTkLabel(
            stats_frame,
            text="Accounts: 0 | Tokens: 0",
            font=("Arial", 10),
            text_color="#555555"
        )
        self.sidebar_stats.pack(anchor="w")
    
    def setup_main_area(self, parent):
        """Creează zona principală"""
        main_area = ctk.CTkFrame(parent)
        main_area.pack(side="right", fill="both", expand=True)
        
        # Header cu animație
        header = ctk.CTkFrame(main_area, height=70, fg_color="#0A0A1E")
        header.pack(fill="x", pady=(0, 10))
        
        # Titlu animat
        self.header_label = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 28, "bold"),
            text_color="#00FF88"
        )
        self.header_label.pack(side="left", padx=30, pady=20)
        
        # Quick actions în header
        quick_frame = ctk.CTkFrame(header, fg_color="transparent")
        quick_frame.pack(side="right", padx=20, pady=20)
        
        self.start_stop_btn = ctk.CTkButton(
            quick_frame,
            text="▶ START FARMING",
            font=("Arial", 14, "bold"),
            width=180,
            height=40,
            fg_color="#00AA44",
            hover_color="#00CC66",
            command=self.toggle_farming
        )
        self.start_stop_btn.pack(side="left", padx=5)
        
        # Live stats în header
        live_stats = ctk.CTkFrame(header, fg_color="transparent")
        live_stats.pack(side="right", padx=20)
        
        self.live_stats_label = ctk.CTkLabel(
            live_stats,
            text="🔄 0 Created | ⏱️ 00:00:00",
            font=("Arial", 12),
            text_color="#FFAA00"
        )
        self.live_stats_label.pack()
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_area)
        self.content_frame.pack(fill="both", expand=True)
        
        # Inițializează cu Main Panel
        self.show_main_panel()
    
    def clear_content_frame(self):
        """Șterge conținutul din frame-ul principal"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def animate_header(self, text):
        """Animație pentru header"""
        self.header_label.configure(text="")
        full_text = text
        delay = 100
        
        def type_effect(index=0):
            if index < len(full_text):
                current_text = self.header_label.cget("text") + full_text[index]
                self.header_label.configure(text=current_text)
                self.root.after(delay, lambda: type_effect(index + 1))
        
        type_effect()
    
    def show_main_panel(self):
        """Afișează panoul principal cu farm infinit"""
        self.clear_content_frame()
        self.animate_header("⚡ ULTIMATE FARMING PANEL")
        
        # Farm control panel
        control_frame = ctk.CTkFrame(self.content_frame, fg_color="#1A1A2E")
        control_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Farm settings
        settings_frame = ctk.CTkFrame(control_frame)
        settings_frame.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(
            settings_frame,
            text="⚙️ FARMING SETTINGS",
            font=("Arial", 22, "bold"),
            text_color="#00FF88"
        ).pack(anchor="w", pady=(0, 20))
        
        # Proxy selection
        proxy_frame = ctk.CTkFrame(settings_frame)
        proxy_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            proxy_frame,
            text="Proxy Mode:",
            font=("Arial", 14),
            text_color="white"
        ).pack(side="left", padx=10)
        
        self.proxy_mode = tk.StringVar(value="none")
        
        ctk.CTkRadioButton(
            proxy_frame,
            text="No Proxy",
            variable=self.proxy_mode,
            value="none",
            font=("Arial", 13)
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            proxy_frame,
            text="Use Proxy",
            variable=self.proxy_mode,
            value="use",
            font=("Arial", 13)
        ).pack(side="left", padx=20)
        
        # Delay settings
        delay_frame = ctk.CTkFrame(settings_frame)
        delay_frame.pack(fill="x", pady=15)
        
        ctk.CTkLabel(
            delay_frame,
            text="Delay between accounts (seconds):",
            font=("Arial", 14),
            text_color="white"
        ).pack(side="left", padx=10)
        
        self.delay_var = tk.StringVar(value="10")
        delay_slider = ctk.CTkSlider(
            delay_frame,
            from_=5,
            to=60,
            number_of_steps=55,
            variable=self.delay_var,
            width=300
        )
        delay_slider.pack(side="left", padx=20)
        
        self.delay_label = ctk.CTkLabel(
            delay_frame,
            text="10s",
            font=("Arial", 14, "bold"),
            text_color="#FFAA00"
        )
        self.delay_label.pack(side="left", padx=10)
        
        delay_slider.configure(command=self.update_delay_label)
        
        # Bot count (pentru test în panoul Bots)
        bot_frame = ctk.CTkFrame(settings_frame)
        bot_frame.pack(fill="x", pady=15)
        
        ctk.CTkLabel(
            bot_frame,
            text="Test accounts to create (in Bots panel):",
            font=("Arial", 14),
            text_color="white"
        ).pack(side="left", padx=10)
        
        self.test_count_var = tk.StringVar(value="3")
        test_entry = ctk.CTkEntry(
            bot_frame,
            textvariable=self.test_count_var,
            width=100
        )
        test_entry.pack(side="left", padx=20)
        
        # Start/Stop farm buttons
        button_frame = ctk.CTkFrame(settings_frame)
        button_frame.pack(fill="x", pady=30)
        
        self.main_start_btn = ctk.CTkButton(
            button_frame,
            text="🚀 START INFINITE FARMING",
            font=("Arial", 18, "bold"),
            height=60,
            fg_color="#00AA44",
            hover_color="#00CC66",
            command=self.start_infinite_farm
        )
        self.main_start_btn.pack(side="left", expand=True, padx=10)
        
        self.main_stop_btn = ctk.CTkButton(
            button_frame,
            text="🛑 STOP FARMING",
            font=("Arial", 18, "bold"),
            height=60,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.stop_farming,
            state="disabled"
        )
        self.main_stop_btn.pack(side="left", expand=True, padx=10)
        
        # Live farm statistics
        stats_frame = ctk.CTkFrame(control_frame)
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        # Grid de statistici
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(fill="both", expand=True, pady=10)
        
        stats_data = [
            ("🤖 Active Farming", "NO", "#FF4444"),
            ("👤 Total Created", str(self.total_created), "#00FF88"),
            ("✅ Successful", str(self.successful_creations), "#00AA44"),
            ("⏱️ Runtime", "00:00:00", "#FFAA00"),
            ("📈 Success Rate", "0%", "#8844FF"),
            ("⚡ Speed", "0 acc/h", "#00AAAA")
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_card = ctk.CTkFrame(stats_grid, width=180, height=100)
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            stat_card.grid_propagate(False)
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Arial", 12),
                text_color="#888888"
            ).pack(pady=(15, 5))
            
            label_var = tk.StringVar(value=value)
            stat_value = ctk.CTkLabel(
                stat_card,
                textvariable=label_var,
                font=("Arial", 22, "bold"),
                text_color=color
            )
            stat_value.pack()
            
            # Salvează referința pentru actualizare
            if label == "🤖 Active Farming":
                self.active_farm_label = stat_value
                self.active_farm_var = label_var
            elif label == "👤 Total Created":
                self.total_created_label = stat_value
                self.total_created_var = label_var
            elif label == "✅ Successful":
                self.successful_label = stat_value
                self.successful_var = label_var
            elif label == "⏱️ Runtime":
                self.runtime_label = stat_value
                self.runtime_var = label_var
            elif label == "📈 Success Rate":
                self.rate_label = stat_value
                self.rate_var = label_var
            elif label == "⚡ Speed":
                self.speed_label = stat_value
                self.speed_var = label_var
        
        # Configure grid
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1)
        for i in range(2):
            stats_grid.rowconfigure(i, weight=1)
        
        # Farm log
        log_frame = ctk.CTkFrame(control_frame)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        ctk.CTkLabel(
            log_frame,
            text="📝 FARMING LOG",
            font=("Arial", 16, "bold"),
            text_color="#00FF88"
        ).pack(anchor="w", padx=10, pady=10)
        
        self.farm_log = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            bg="#0A0A1E",
            fg="#00FF88",
            font=("Consolas", 10),
            insertbackground="white",
            wrap="word"
        )
        self.farm_log.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adaugă mesaj inițial
        self.log_message("🤖 BRF Farming System Ready!")
        self.log_message(f"📊 Loaded {len(self.accounts)} accounts and {len(self.tokens)} tokens")
        self.log_message("⚡ Set your preferences and click START FARMING")
    
    def show_bots_panel(self):
        """Afișează panoul pentru testarea botilor"""
        self.clear_content_frame()
        self.animate_header("🤖 TEST BOTS PANEL")
        
        test_frame = ctk.CTkFrame(self.content_frame)
        test_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info panel
        info_frame = ctk.CTkFrame(test_frame, fg_color="#1A1A2E")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="🧪 TEST MODE - CREATE A FEW ACCOUNTS",
            font=("Arial", 18, "bold"),
            text_color="#FFAA00"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="This panel creates a limited number of accounts to test your settings.\nUse Main Panel for infinite farming.",
            font=("Arial", 13),
            text_color="#888888",
            justify="center"
        ).pack(pady=10)
        
        # Test controls
        control_frame = ctk.CTkFrame(test_frame)
        control_frame.pack(fill="x", padx=30, pady=20)
        
        # Number of test accounts
        count_frame = ctk.CTkFrame(control_frame)
        count_frame.pack(pady=10)
        
        ctk.CTkLabel(
            count_frame,
            text="Number of test accounts:",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        
        self.test_count_var_bots = tk.StringVar(value="3")
        count_entry = ctk.CTkEntry(
            count_frame,
            textvariable=self.test_count_var_bots,
            width=80
        )
        count_entry.pack(side="left", padx=10)
        
        # Test buttons
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 TEST WITHOUT PROXY",
            font=("Arial", 14, "bold"),
            height=45,
            width=200,
            fg_color="#4444AA",
            hover_color="#6666CC",
            command=lambda: self.start_test_farm(use_proxy=False)
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="🌐 TEST WITH PROXY",
            font=("Arial", 14, "bold"),
            height=45,
            width=200,
            fg_color="#AA44AA",
            hover_color="#CC66CC",
            command=lambda: self.start_test_farm(use_proxy=True)
        ).pack(side="left", padx=10)
        
        # Test log
        log_frame = ctk.CTkFrame(test_frame)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        ctk.CTkLabel(
            log_frame,
            text="📝 TEST LOG",
            font=("Arial", 16, "bold"),
            text_color="#00FF88"
        ).pack(anchor="w", padx=10, pady=10)
        
        self.test_log = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            bg="#0A0A1E",
            fg="#00FF88",
            font=("Consolas", 10),
            insertbackground="white"
        )
        self.test_log.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_proxy_panel(self):
        """Afișează panoul pentru proxy"""
        self.clear_content_frame()
        self.animate_header("🔌 PROXY MANAGEMENT")
        
        proxy_frame = ctk.CTkFrame(self.content_frame)
        proxy_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Proxy controls
        control_frame = ctk.CTkFrame(proxy_frame)
        control_frame.pack(fill="x", padx=30, pady=20)
        
        # Add proxy
        add_frame = ctk.CTkFrame(control_frame)
        add_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            add_frame,
            text="Add Proxy (ip:port or ip:port:user:pass):",
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        
        self.proxy_entry = ctk.CTkEntry(add_frame, width=300)
        self.proxy_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(
            add_frame,
            text="➕ Add",
            width=80,
            command=self.add_proxy_from_entry
        ).pack(side="left", padx=10)
        
        # Proxy list
        list_frame = ctk.CTkFrame(proxy_frame)
        list_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Listbox cu scrollbar
        list_container = ctk.CTkFrame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        self.proxy_listbox = tk.Listbox(
            list_container,
            bg="#1A1A1A",
            fg="#FFFFFF",
            selectbackground="#00AA44",
            font=("Consolas", 11),
            height=12
        )
        
        scrollbar = tk.Scrollbar(list_container)
        self.proxy_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.proxy_listbox.yview)
        
        self.proxy_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Adaugă proxy existente în listă
        for proxy in self.proxies:
            self.proxy_listbox.insert(tk.END, proxy)
        
        # Action buttons
        action_frame = ctk.CTkFrame(proxy_frame)
        action_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="📁 Import from File",
            width=150,
            command=self.import_proxies
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🗑️ Delete Selected",
            width=150,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.delete_selected_proxy
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🧹 Clear All",
            width=150,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.clear_proxies
        ).pack(side="left", padx=10)
        
        # Proxy statistics
        stats_frame = ctk.CTkFrame(proxy_frame)
        stats_frame.pack(fill="x", padx=30, pady=10)
        
        self.proxy_stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"📊 Total Proxies: {len(self.proxies)}",
            font=("Arial", 14, "bold"),
            text_color="#00FF88"
        )
        self.proxy_stats_label.pack()
    
    def show_accounts_panel(self):
        """Afișează panoul pentru conturi"""
        self.clear_content_frame()
        self.animate_header("👤 ACCOUNTS DATABASE")
        
        accounts_frame = ctk.CTkFrame(self.content_frame)
        accounts_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Action buttons
        action_frame = ctk.CTkFrame(accounts_frame)
        action_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="📁 Import Accounts",
            width=150,
            command=self.import_accounts
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="💾 Export Accounts",
            width=150,
            command=self.export_accounts
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🧹 Clear All",
            width=150,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.clear_accounts
        ).pack(side="left", padx=10)
        
        # Accounts table
        table_frame = ctk.CTkFrame(accounts_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Create treeview
        self.accounts_tree = ttk.Treeview(
            table_frame,
            columns=("#", "Username", "Password", "Token", "Created"),
            show="headings",
            height=15
        )
        
        # Style treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                       background="#1A1A1A",
                       foreground="white",
                       fieldbackground="#1A1A1A",
                       rowheight=25)
        style.map('Treeview', background=[('selected', '#00AA44')])
        
        # Configure columns
        columns = [("#", 50), ("Username", 150), ("Password", 120), ("Token", 250), ("Created", 150)]
        
        for col, width in columns:
            self.accounts_tree.heading(col, text=col)
            self.accounts_tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.accounts_tree.yview)
        self.accounts_tree.configure(yscrollcommand=scrollbar.set)
        
        self.accounts_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load accounts
        self.load_accounts_to_table()
        
        # Statistics
        stats_frame = ctk.CTkFrame(accounts_frame)
        stats_frame.pack(fill="x", padx=30, pady=10)
        
        self.accounts_stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"📊 Total Accounts: {len(self.accounts)}",
            font=("Arial", 14, "bold"),
            text_color="#00FF88"
        )
        self.accounts_stats_label.pack()
    
    def show_tokens_panel(self):
        """Afișează panoul pentru tokenuri"""
        self.clear_content_frame()
        self.animate_header("🔑 TOKENS MANAGER")
        
        tokens_frame = ctk.CTkFrame(self.content_frame)
        tokens_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Token display
        display_frame = ctk.CTkFrame(tokens_frame)
        display_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.tokens_text = scrolledtext.ScrolledText(
            display_frame,
            height=20,
            bg="#0A0A1E",
            fg="#00FF88",
            font=("Consolas", 10),
            insertbackground="white",
            wrap="word"
        )
        self.tokens_text.pack(fill="both", expand=True)
        
        # Update tokens display
        self.update_tokens_display()
        
        # Action buttons
        action_frame = ctk.CTkFrame(tokens_frame)
        action_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkButton(
            action_frame,
            text="📁 Import Tokens",
            width=150,
            command=self.import_tokens
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="💾 Export Tokens",
            width=150,
            command=self.export_tokens
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🔍 Check Validity",
            width=150,
            command=self.check_tokens
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🧹 Clear All",
            width=150,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.clear_tokens
        ).pack(side="left", padx=10)
    
    def show_stats_panel(self):
        """Afișează panoul cu statistici"""
        self.clear_content_frame()
        self.animate_header("📊 SYSTEM STATISTICS")
        
        self.show_stats_panel_content()
    
    def show_stats_panel_content(self):
        """Conținutul panoului de statistici"""
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Grid de statistici
        grid_frame = ctk.CTkFrame(stats_frame)
        grid_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        stats_data = [
            ("🤖 Total Accounts Created", str(self.total_created), "#00FF88"),
            ("✅ Successful Creations", str(self.successful_creations), "#00AA44"),
            ("❌ Failed Attempts", str(self.total_created - self.successful_creations), "#FF4444"),
            ("📈 Success Rate", f"{(self.successful_creations/self.total_created*100 if self.total_created > 0 else 0):.1f}%", "#8844FF"),
            ("👤 Accounts in DB", str(len(self.accounts)), "#FFAA00"),
            ("🔑 Tokens in DB", str(len(self.tokens)), "#00AAAA"),
            ("🔌 Available Proxies", str(len(self.proxies)), "#AA44AA"),
            ("⚡ Average Speed", "Calculating...", "#00FF88")
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            row = i // 4
            col = i % 4
            
            stat_card = ctk.CTkFrame(grid_frame, width=200, height=120)
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            stat_card.grid_propagate(False)
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Arial", 12),
                text_color="#888888"
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Arial", 24, "bold"),
                text_color=color
            ).pack()
        
        # Configure grid
        for i in range(4):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(2):
            grid_frame.rowconfigure(i, weight=1)
    
    def show_settings_panel(self):
        """Afișează panoul cu setări"""
        self.clear_content_frame()
        self.animate_header("⚙️ SYSTEM SETTINGS")
        
        settings_frame = ctk.CTkFrame(self.content_frame)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Settings content
        content_frame = ctk.CTkFrame(settings_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            content_frame,
            text="BRF Ultimate Bot Manager v3.0",
            font=("Arial", 24, "bold"),
            text_color="#00FF88"
        ).pack(pady=20)
        
        info_text = """
        🤖 Advanced Roblox Account Creator
        
        Features:
        • Infinite account farming
        • Proxy support (rotating proxies)
        • Token extraction (.ROBLOSECURITY)
        • Auto-save accounts & tokens
        • Real-time statistics
        • Test mode with/without proxy
        
        Requirements auto-installed:
        • Selenium WebDriver
        • Chrome WebDriver
        • Required Python packages
        
        ⚠️ Use responsibly and follow Roblox ToS
        """
        
        ctk.CTkLabel(
            content_frame,
            text=info_text,
            font=("Arial", 13),
            text_color="#888888",
            justify="left"
        ).pack(pady=20)
        
        # Buttons
        button_frame = ctk.CTkFrame(content_frame)
        button_frame.pack(pady=30)
        
        ctk.CTkButton(
            button_frame,
            text="🔄 Check Requirements",
            width=200,
            command=self.check_requirements_gui
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="💾 Backup Data",
            width=200,
            command=self.backup_data
        ).pack(side="left", padx=10)
    
    def update_delay_label(self, value):
        """Actualizează label-ul pentru delay"""
        self.delay_label.configure(text=f"{int(float(value))}s")
    
    def toggle_farming(self):
        """Comută între start și stop farming"""
        if not self.farming_active:
            self.start_infinite_farm()
        else:
            self.stop_farming()
    
    def start_infinite_farm(self):
        """Pornește farm-ul infinit în Main Panel"""
        if not self.farming_active:
            self.farming_active = True
            self.start_time = time.time()
            
            # Update UI
            self.start_stop_btn.configure(text="🛑 STOP FARMING", fg_color="#AA4444", hover_color="#CC6666")
            self.main_start_btn.configure(state="disabled")
            self.main_stop_btn.configure(state="normal")
            self.active_farm_var.set("YES")
            self.active_farm_label.configure(text_color="#00FF88")
            self.status_label.configure(text="Farming accounts...")
            
            # Pornește thread-ul de farm
            self.farm_thread = threading.Thread(target=self.infinite_farm_worker, daemon=True)
            self.farm_thread.start()
            
            # Pornește timer-ul pentru statistici
            self.start_stats_timer()
            
            self.log_message("🚀 INFINITE FARMING STARTED!")
            self.log_message(f"⚙️ Mode: {'With Proxy' if self.proxy_mode.get() == 'use' else 'No Proxy'}")
            self.log_message(f"⏱️ Delay: {self.delay_var.get()} seconds")
    
    def start_test_farm(self, use_proxy=False):
        """Pornește farm-ul de test în Bots Panel"""
        try:
            count = int(self.test_count_var_bots.get())
            if count <= 0:
                messagebox.showwarning("Warning", "Please enter a positive number")
                return
            
            # Clear test log
            self.test_log.delete(1.0, tk.END)
            self.test_log.insert(tk.END, f"🧪 STARTING TEST: {count} accounts {'with proxy' if use_proxy else 'without proxy'}\n")
            self.test_log.insert(tk.END, "="*50 + "\n")
            
            # Pornește testul într-un thread separat
            test_thread = threading.Thread(
                target=self.test_farm_worker,
                args=(count, use_proxy),
                daemon=True
            )
            test_thread.start()
            
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number")
    
    def infinite_farm_worker(self):
        """Worker pentru farm infinit"""
        consecutive_errors = 0
        
        while self.farming_active:
            try:
                # Alege un proxy dacă este activat
                proxy = None
                if self.proxy_mode.get() == "use" and self.proxies:
                    proxy = random.choice(self.proxies)
                
                # Creează cont
                creator = RobloxAccountCreator(
                    use_proxy=(proxy is not None),
                    proxy=proxy
                )
                
                if creator.setup_driver():
                    result = creator.create_account()
                    
                    if result and result["token"]:
                        # Salvează contul
                        self.accounts.append({
                            "username": result["username"],
                            "password": result["password"],
                            "token": result["token"],
                            "created": result["created"]
                        })
                        
                        # Salvează token separat
                        if result["token"] not in self.tokens:
                            self.tokens.append(result["token"])
                        
                        self.total_created += 1
                        self.successful_creations += 1
                        
                        # Update statistici
                        self.update_stats()
                        
                        # Log success
                        log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Account #{self.total_created}: {result['username']}"
                        if proxy:
                            log_msg += f" (Proxy: {proxy.split(':')[0]})"
                        self.log_message(log_msg)
                        
                        consecutive_errors = 0
                    else:
                        self.total_created += 1
                        log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Failed attempt #{self.total_created}"
                        if proxy:
                            log_msg += f" (Proxy: {proxy.split(':')[0] if ':' in proxy else proxy})"
                        self.log_message(log_msg)
                        consecutive_errors += 1
                    
                    creator.close()
                    
                    # Pauză între conturi
                    delay = int(float(self.delay_var.get()))
                    for remaining in range(delay, 0, -1):
                        if not self.farming_active:
                            break
                        time.sleep(1)
                    
                    # Pauză mai lungă după erori consecutive
                    if consecutive_errors >= 3:
                        extra_delay = consecutive_errors * 5
                        self.log_message(f"⚠️ {consecutive_errors} consecutive errors, waiting {extra_delay}s...")
                        time.sleep(extra_delay)
                
                else:
                    self.log_message("❌ Failed to setup browser")
                    time.sleep(10)
                    
            except Exception as e:
                self.log_message(f"💥 Error: {str(e)[:100]}")
                time.sleep(5)
    
    def test_farm_worker(self, count, use_proxy):
        """Worker pentru farm de test"""
        successful = 0
        proxy = None
        
        if use_proxy and self.proxies:
            proxy = random.choice(self.proxies)
        
        for i in range(count):
            if not self.farming_active:  # Dacă farm-ul infinit s-a oprit
                break
            
            try:
                creator = RobloxAccountCreator(
                    use_proxy=(proxy is not None),
                    proxy=proxy
                )
                
                self.test_log_insert(f"🔧 Setting up browser {i+1}/{count}...")
                
                if creator.setup_driver():
                    self.test_log_insert(f"🔄 Creating account {i+1}/{count}...")
                    result = creator.create_account()
                    
                    if result and result["token"]:
                        successful += 1
                        
                        # Salvează contul
                        self.accounts.append({
                            "username": result["username"],
                            "password": result["password"],
                            "token": result["token"],
                            "created": result["created"]
                        })
                        
                        if result["token"] not in self.tokens:
                            self.tokens.append(result["token"])
                        
                        self.total_created += 1
                        self.successful_creations += 1
                        
                        self.test_log_insert(f"✅ SUCCESS: {result['username']}")
                        if proxy:
                            self.test_log_insert(f"   Proxy used: {proxy.split(':')[0]}")
                    else:
                        self.test_log_insert(f"❌ FAILED: Could not create account")
                    
                    creator.close()
                    
                else:
                    self.test_log_insert(f"❌ FAILED: Browser setup")
                
                # Pauză între teste
                if i < count - 1:
                    time.sleep(5)
                
            except Exception as e:
                self.test_log_insert(f"💥 ERROR: {str(e)[:80]}")
            
            self.update_stats()
        
        # Final test report
        self.test_log_insert("\n" + "="*50)
        self.test_log_insert(f"📊 TEST COMPLETE: {successful}/{count} successful")
        self.test_log_insert(f"   Mode: {'With Proxy' if use_proxy else 'No Proxy'}")
        if proxy and use_proxy:
            self.test_log_insert(f"   Test proxy: {proxy}")
        
        # Salvează datele
        self.save_accounts()
        self.save_tokens()
    
    def stop_farming(self):
        """Oprește farm-ul"""
        if self.farming_active:
            self.farming_active = False
            
            # Update UI
            self.start_stop_btn.configure(text="▶ START FARMING", fg_color="#00AA44", hover_color="#00CC66")
            self.main_start_btn.configure(state="normal")
            self.main_stop_btn.configure(state="disabled")
            self.active_farm_var.set("NO")
            self.active_farm_label.configure(text_color="#FF4444")
            self.status_label.configure(text="Farming stopped")
            
            # Salvează datele
            self.save_accounts()
            self.save_tokens()
            
            # Calculează timpul total
            if self.start_time:
                elapsed = time.time() - self.start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                
                self.log_message(f"\n🛑 FARMING STOPPED!")
                self.log_message(f"⏱️ Total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
                self.log_message(f"📊 Final stats: {self.successful_creations}/{self.total_created} successful")
                
                if elapsed > 0 and self.successful_creations > 0:
                    rate = (self.successful_creations / self.total_created) * 100
                    speed = (self.successful_creations / elapsed) * 3600
                    self.log_message(f"📈 Success rate: {rate:.1f}%")
                    self.log_message(f"⚡ Average speed: {speed:.1f} accounts/hour")
            
            self.log_message("💾 All data saved to files")
    
    def start_stats_timer(self):
        """Pornește timer-ul pentru statistici în timp real"""
        if self.farming_active:
            # Calculează timpul scurs
            if self.start_time:
                elapsed = time.time() - self.start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                
                self.runtime_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                
                # Calculează rata de succes
                if self.total_created > 0:
                    rate = (self.successful_creations / self.total_created) * 100
                    self.rate_var.set(f"{rate:.1f}%")
                    
                    # Calculează viteza
                    if elapsed > 0:
                        speed = (self.successful_creations / elapsed) * 3600
                        self.speed_var.set(f"{speed:.1f} acc/h")
            
            # Update live stats
            self.total_created_var.set(str(self.total_created))
            self.successful_var.set(str(self.successful_creations))
            self.live_stats_label.configure(text=f"🔄 {self.total_created} Created | ✅ {self.successful_creations} Success")
            
            # Re-programează timer-ul
            self.root.after(1000, self.start_stats_timer)
    
    def log_message(self, message):
        """Adaugă mesaj în farm log"""
        self.farm_log.insert(tk.END, message + "\n")
        self.farm_log.see(tk.END)
        self.root.update()
    
    def test_log_insert(self, message):
        """Adaugă mesaj în test log"""
        self.test_log.insert(tk.END, message + "\n")
        self.test_log.see(tk.END)
        self.root.update()
    
    def update_stats(self):
        """Actualizează toate statisticile"""
        # Update sidebar
        self.sidebar_stats.configure(text=f"Accounts: {len(self.accounts)} | Tokens: {len(self.tokens)}")
        
        # Update live stats dacă farm-ul rulează
        if self.farming_active:
            self.total_created_var.set(str(self.total_created))
            self.successful_var.set(str(self.successful_creations))
    
    def add_proxy_from_entry(self):
        """Adaugă proxy din entry"""
        proxy = self.proxy_entry.get().strip()
        if proxy:
            self.proxies.append(proxy)
            self.proxy_listbox.insert(tk.END, proxy)
            self.proxy_entry.delete(0, tk.END)
            self.update_proxy_stats()
            self.save_proxies()
    
    def import_proxies(self):
        """Importă proxy din fișier"""
        file_path = filedialog.askopenfilename(
            title="Select proxies file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    new_proxies = [line.strip() for line in f if line.strip()]
                
                self.proxies.extend(new_proxies)
                self.proxy_listbox.delete(0, tk.END)
                
                for proxy in self.proxies:
                    self.proxy_listbox.insert(tk.END, proxy)
                
                self.update_proxy_stats()
                self.save_proxies()
                
                messagebox.showinfo("Success", f"Imported {len(new_proxies)} proxies!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")
    
    def delete_selected_proxy(self):
        """Șterge proxy selectat"""
        selection = self.proxy_listbox.curselection()
        if selection:
            index = selection[0]
            self.proxies.pop(index)
            self.proxy_listbox.delete(index)
            self.update_proxy_stats()
            self.save_proxies()
    
    def clear_proxies(self):
        """Șterge toate proxy-urile"""
        if messagebox.askyesno("Confirm", "Delete all proxies?"):
            self.proxies.clear()
            self.proxy_listbox.delete(0, tk.END)
            self.update_proxy_stats()
            self.save_proxies()
    
    def update_proxy_stats(self):
        """Actualizează statisticile proxy"""
        self.proxy_stats_label.configure(text=f"📊 Total Proxies: {len(self.proxies)}")
    
    def load_accounts_to_table(self):
        """Încarcă conturile în tabel"""
        # Clear table
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        
        # Add accounts
        for i, account in enumerate(self.accounts):
            token_display = account.get("token", "")[:30] + "..." if len(account.get("token", "")) > 30 else account.get("token", "")
            self.accounts_tree.insert("", "end", values=(
                i+1,
                account.get("username", ""),
                account.get("password", ""),
                token_display,
                account.get("created", "")
            ))
        
        # Update statistics
        self.accounts_stats_label.configure(text=f"📊 Total Accounts: {len(self.accounts)}")
    
    def import_accounts(self):
        """Importă conturi din fișier"""
        file_path = filedialog.askopenfilename(
            title="Select accounts file",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'r') as f:
                        new_accounts = json.load(f)
                else:
                    new_accounts = []
                    with open(file_path, 'r') as f:
                        for line in f:
                            if ':' in line:
                                parts = line.strip().split(':', 3)
                                if len(parts) >= 2:
                                    account = {
                                        "username": parts[0].strip(),
                                        "password": parts[1].strip(),
                                        "token": parts[2].strip() if len(parts) > 2 else "",
                                        "created": parts[3].strip() if len(parts) > 3 else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                                    new_accounts.append(account)
                
                self.accounts.extend(new_accounts)
                self.save_accounts()
                self.load_accounts_to_table()
                self.update_stats()
                
                messagebox.showinfo("Success", f"Imported {len(new_accounts)} accounts!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")
    
    def export_accounts(self):
        """Exportă conturi în fișier"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Save accounts"
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump(self.accounts, f, indent=2)
                else:
                    with open(file_path, 'w') as f:
                        for account in self.accounts:
                            f.write(f"{account['username']}:{account['password']}:{account.get('token', '')}:{account.get('created', '')}\n")
                
                messagebox.showinfo("Success", f"Exported {len(self.accounts)} accounts!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def clear_accounts(self):
        """Șterge toate conturile"""
        if messagebox.askyesno("Confirm", "Delete ALL accounts? This cannot be undone!"):
            self.accounts.clear()
            self.save_accounts()
            self.load_accounts_to_table()
            self.update_stats()
    
    def update_tokens_display(self):
        """Actualizează afișajul tokenurilor"""
        self.tokens_text.delete(1.0, tk.END)
        
        if self.tokens:
            for i, token in enumerate(self.tokens):
                self.tokens_text.insert(tk.END, f"[{i+1}] {token}\n")
                self.tokens_text.insert(tk.END, "-"*80 + "\n")
        else:
            self.tokens_text.insert(tk.END, "No tokens available. Start farming to collect tokens!\n")
    
    def import_tokens(self):
        """Importă tokenuri din fișier"""
        file_path = filedialog.askopenfilename(
            title="Select tokens file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    new_tokens = [line.strip() for line in f if line.strip() and '_|WARNING' in line]
                
                self.tokens.extend(new_tokens)
                self.save_tokens()
                self.update_tokens_display()
                
                messagebox.showinfo("Success", f"Imported {len(new_tokens)} tokens!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")
    
    def export_tokens(self):
        """Exportă tokenuri în fișier"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save tokens"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for token in self.tokens:
                        f.write(f"{token}\n")
                
                messagebox.showinfo("Success", f"Exported {len(self.tokens)} tokens!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def check_tokens(self):
        """Verifică validitatea tokenurilor (demo)"""
        messagebox.showinfo("Token Check", f"Found {len(self.tokens)} tokens.\n\nNote: Full validation requires Roblox API calls which are not implemented in this demo version.")
    
    def clear_tokens(self):
        """Șterge toate tokenurile"""
        if messagebox.askyesno("Confirm", "Delete ALL tokens?"):
            self.tokens.clear()
            self.save_tokens()
            self.update_tokens_display()
    
    def check_requirements_gui(self):
        """Verifică requirements din GUI"""
        threading.Thread(target=install_requirements, daemon=True).start()
        messagebox.showinfo("Requirements", "Checking and installing requirements in background. Check console for details.")
    
    def backup_data(self):
        """Face backup la toate datele"""
        try:
            # Creează folder de backup
            backup_dir = "BRF_Backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Salvează toate fișierele
            with open(os.path.join(backup_dir, "accounts.json"), 'w') as f:
                json.dump(self.accounts, f, indent=2)
            
            with open(os.path.join(backup_dir, "tokens.txt"), 'w') as f:
                for token in self.tokens:
                    f.write(f"{token}\n")
            
            with open(os.path.join(backup_dir, "proxies.txt"), 'w') as f:
                for proxy in self.proxies:
                    f.write(f"{proxy}\n")
            
            with open(os.path.join(backup_dir, "stats.txt"), 'w') as f:
                f.write(f"BRF Backup - {datetime.now()}\n")
                f.write(f"Total Created: {self.total_created}\n")
                f.write(f"Successful: {self.successful_creations}\n")
                f.write(f"Accounts in DB: {len(self.accounts)}\n")
                f.write(f"Tokens in DB: {len(self.tokens)}\n")
                f.write(f"Proxies: {len(self.proxies)}\n")
            
            messagebox.showinfo("Backup", f"Backup created in folder:\n{backup_dir}")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {e}")
    
    def load_saved_data(self):
        """Încarcă datele salvate"""
        try:
            # Load accounts
            if os.path.exists('accounts.json'):
                with open('accounts.json', 'r') as f:
                    self.accounts = json.load(f)
            
            # Load tokens
            if os.path.exists('tokens.txt'):
                with open('tokens.txt', 'r') as f:
                    self.tokens = [line.strip() for line in f if line.strip() and '_|WARNING' in line]
            
            # Load proxies
            if os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
        except:
            # Dacă există erori, începe cu liste goale
            pass
    
    def save_accounts(self):
        """Salvează conturile"""
        try:
            with open('accounts.json', 'w') as f:
                json.dump(self.accounts, f, indent=2)
        except:
            pass
    
    def save_tokens(self):
        """Salvează tokenurile"""
        try:
            with open('tokens.txt', 'w') as f:
                for token in self.tokens:
                    f.write(f"{token}\n")
        except:
            pass
    
    def save_proxies(self):
        """Salvează proxy-urile"""
        try:
            with open('proxies.txt', 'w') as f:
                for proxy in self.proxies:
                    f.write(f"{proxy}\n")
        except:
            pass

# Punctul de intrare principal
if __name__ == "__main__":
    # Afișează banner
    print(Fore.CYAN + "╔══════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║        BRF ULTIMATE BOT MANAGER v3.0            ║")
    print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
    print(Fore.GREEN + "║      🤖 Advanced Roblox Account Creator        ║")
    print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
    print(Fore.YELLOW + "║     ⚠️  Use responsibly and follow ToS         ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════╝")
    print()
    
    # Instalează requirements
    install_requirements()
    
    # Pornește aplicația
    app = BRFControlPanel()
