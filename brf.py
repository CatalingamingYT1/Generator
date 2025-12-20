import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import customtkinter as ctk
import threading
import time
import os
import json
import random
from datetime import datetime

# Set CustomTkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BRFControlPanel:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("BRF Bot Manager v2.0")
        self.root.geometry("1200x700")
        
        # Variabile de stare
        self.bots_running = False
        self.accounts = []
        self.proxies = []
        self.tokens = []
        self.bot_thread = None
        
        # Configurare layout
        self.setup_layout()
        
        # Încarcă date salvate
        self.load_saved_data()
        
        # Centrează fereastra
        self.center_window()
        
        self.root.mainloop()
    
    def center_window(self):
        """Centrează fereastra pe ecran"""
        self.root.update_idletasks()
        width = 1200
        height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
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
        sidebar = ctk.CTkFrame(parent, width=250)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Titlu meniu
        title_label = ctk.CTkLabel(
            sidebar,
            text="BRF MENU",
            font=("Arial", 24, "bold"),
            text_color="#00FF88"
        )
        title_label.pack(pady=(20, 30))
        
        # Butoane meniu
        menu_buttons = [
            ("🏠 Main Panel", self.show_main_panel),
            ("🤖 Start/Stop Bots", self.show_bots_panel),
            ("🔌 Proxy Settings", self.show_proxy_panel),
            ("👤 Accounts", self.show_accounts_panel),
            ("🔑 Tokens", self.show_tokens_panel),
            ("📊 Statistics", self.show_stats_panel),
            ("⚙️ Settings", self.show_settings_panel)
        ]
        
        for text, command in menu_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 14),
                height=40,
                fg_color="transparent",
                hover_color="#2A2A2A",
                text_color="white",
                anchor="w",
                command=command
            )
            btn.pack(fill="x", padx=10, pady=5)
        
        # Separator
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#444444")
        separator.pack(fill="x", padx=20, pady=20)
        
        # Status bar în meniu
        self.status_label = ctk.CTkLabel(
            sidebar,
            text="Status: Ready",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.status_label.pack(side="bottom", pady=10)
        
        # Version
        version_label = ctk.CTkLabel(
            sidebar,
            text="v2.0 © BRF 2024",
            font=("Arial", 10),
            text_color="#555555"
        )
        version_label.pack(side="bottom", pady=5)
    
    def setup_main_area(self, parent):
        """Creează zona principală"""
        main_area = ctk.CTkFrame(parent)
        main_area.pack(side="right", fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(main_area, height=60)
        header.pack(fill="x", pady=(0, 10))
        
        self.header_label = ctk.CTkLabel(
            header,
            text="BRF CONTROL PANEL",
            font=("Arial", 28, "bold"),
            text_color="#00FF88"
        )
        self.header_label.pack(side="left", padx=20, pady=10)
        
        # Quick stats
        stats_frame = ctk.CTkFrame(header)
        stats_frame.pack(side="right", padx=20, pady=10)
        
        self.bots_label = ctk.CTkLabel(
            stats_frame,
            text="Bots: 0",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.bots_label.pack(side="left", padx=10)
        
        self.accounts_label = ctk.CTkLabel(
            stats_frame,
            text="Accounts: 0",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.accounts_label.pack(side="left", padx=10)
        
        self.tokens_label = ctk.CTkLabel(
            stats_frame,
            text="Tokens: 0",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.tokens_label.pack(side="left", padx=10)
        
        # Content area (se va schimba în funcție de meniu)
        self.content_frame = ctk.CTkFrame(main_area)
        self.content_frame.pack(fill="both", expand=True)
        
        # Inițializează cu Main Panel
        self.show_main_panel()
    
    def clear_content_frame(self):
        """Șterge conținutul din frame-ul principal"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_main_panel(self):
        """Afișează panoul principal"""
        self.clear_content_frame()
        self.header_label.configure(text="MAIN CONTROL PANEL")
        
        # Welcome message
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.pack(fill="x", padx=20, pady=20)
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="🤖 WELCOME TO BRF BOT MANAGER",
            font=("Arial", 22, "bold"),
            text_color="#FFFFFF"
        )
        welcome_label.pack(pady=10)
        
        desc_label = ctk.CTkLabel(
            welcome_frame,
            text="Manage your Roblox bots, accounts, proxies and tokens from one place.",
            font=("Arial", 14),
            text_color="#888888",
            wraplength=800
        )
        desc_label.pack(pady=10)
        
        # Quick actions
        actions_frame = ctk.CTkFrame(self.content_frame)
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        action_buttons = [
            ("🚀 START ALL BOTS", "#00AA44", self.start_all_bots),
            ("🛑 STOP ALL BOTS", "#AA4444", self.stop_all_bots),
            ("📊 VIEW STATISTICS", "#4444AA", self.show_stats_panel),
            ("⚡ QUICK SETUP", "#AA44AA", self.quick_setup)
        ]
        
        for text, color, command in action_buttons:
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                font=("Arial", 14, "bold"),
                height=50,
                fg_color=color,
                hover_color=color,
                command=command
            )
            btn.pack(side="left", expand=True, padx=10, pady=10)
        
        # Dashboard widgets
        self.create_dashboard_widgets()
    
    def show_bots_panel(self):
        """Afișează panoul pentru boti"""
        self.clear_content_frame()
        self.header_label.configure(text="BOTS CONTROL PANEL")
        
        # Control buttons
        control_frame = ctk.CTkFrame(self.content_frame)
        control_frame.pack(fill="x", padx=20, pady=20)
        
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶ START BOTS FARMING",
            font=("Arial", 16, "bold"),
            height=50,
            fg_color="#00AA44",
            hover_color="#00CC66",
            command=self.start_bots_farming
        )
        self.start_btn.pack(side="left", padx=10, pady=10)
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹ STOP BOTS FARMING",
            font=("Arial", 16, "bold"),
            height=50,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.stop_bots_farming,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10, pady=10)
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self.content_frame)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # Number of bots
        ctk.CTkLabel(
            settings_frame,
            text="Number of Bots:",
            font=("Arial", 14)
        ).pack(side="left", padx=10, pady=10)
        
        self.bot_count_var = tk.StringVar(value="5")
        bot_count_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.bot_count_var,
            width=100
        )
        bot_count_entry.pack(side="left", padx=10, pady=10)
        
        # Delay between actions
        ctk.CTkLabel(
            settings_frame,
            text="Delay (seconds):",
            font=("Arial", 14)
        ).pack(side="left", padx=10, pady=10)
        
        self.delay_var = tk.StringVar(value="2")
        delay_entry = ctk.CTkEntry(
            settings_frame,
            textvariable=self.delay_var,
            width=100
        )
        delay_entry.pack(side="left", padx=10, pady=10)
        
        # Log area
        log_frame = ctk.CTkFrame(self.content_frame)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            log_frame,
            text="Bots Activity Log:",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.bot_log = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            bg="#1A1A1A",
            fg="#00FF88",
            font=("Consolas", 10),
            insertbackground="white"
        )
        self.bot_log.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_proxy_panel(self):
        """Afișează panoul pentru proxy"""
        self.clear_content_frame()
        self.header_label.configure(text="PROXY SETTINGS")
        
        # Enable/Disable proxy
        toggle_frame = ctk.CTkFrame(self.content_frame)
        toggle_frame.pack(fill="x", padx=20, pady=20)
        
        self.proxy_enabled = tk.BooleanVar(value=False)
        proxy_toggle = ctk.CTkSwitch(
            toggle_frame,
            text="Enable Proxy Support",
            variable=self.proxy_enabled,
            font=("Arial", 14),
            command=self.toggle_proxy_support
        )
        proxy_toggle.pack(side="left", padx=20, pady=10)
        
        # Proxy list frame
        list_frame = ctk.CTkFrame(self.content_frame)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Butoane pentru proxy
        proxy_buttons_frame = ctk.CTkFrame(list_frame)
        proxy_buttons_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            proxy_buttons_frame,
            text="➕ Add Proxy",
            width=120,
            command=self.add_proxy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            proxy_buttons_frame,
            text="📁 Import from File",
            width=120,
            command=self.import_proxies
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            proxy_buttons_frame,
            text="🗑️ Clear All",
            width=120,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.clear_proxies
        ).pack(side="left", padx=5)
        
        # Lista proxy
        self.proxy_listbox = tk.Listbox(
            list_frame,
            bg="#1A1A1A",
            fg="#FFFFFF",
            selectbackground="#00AA44",
            font=("Consolas", 11),
            height=12
        )
        self.proxy_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adaugă proxy existente în listă
        for proxy in self.proxies:
            self.proxy_listbox.insert(tk.END, proxy)
        
        # Proxy info
        info_frame = ctk.CTkFrame(self.content_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Format: ip:port:username:password  or  ip:port",
            font=("Arial", 12),
            text_color="#888888"
        )
        info_label.pack(pady=5)
        
        self.proxy_count_label = ctk.CTkLabel(
            info_frame,
            text=f"Total Proxies: {len(self.proxies)}",
            font=("Arial", 12),
            text_color="#00FF88"
        )
        self.proxy_count_label.pack(pady=5)
    
    def show_accounts_panel(self):
        """Afișează panoul pentru conturi"""
        self.clear_content_frame()
        self.header_label.configure(text="ACCOUNTS MANAGEMENT")
        
        # Butoane pentru conturi
        buttons_frame = ctk.CTkFrame(self.content_frame)
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="➕ Add Account",
            width=140,
            command=self.add_account_dialog
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="📁 Import Accounts",
            width=140,
            command=self.import_accounts
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Generate Random",
            width=140,
            command=self.generate_random_accounts
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="💾 Export Accounts",
            width=140,
            command=self.export_accounts
        ).pack(side="left", padx=5)
        
        # Tabel pentru conturi
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview
        self.accounts_tree = ttk.Treeview(
            table_frame,
            columns=("Username", "Password", "Status", "Created"),
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
        self.accounts_tree.heading("Username", text="Username")
        self.accounts_tree.heading("Password", text="Password")
        self.accounts_tree.heading("Status", text="Status")
        self.accounts_tree.heading("Created", text="Created")
        
        self.accounts_tree.column("Username", width=200)
        self.accounts_tree.column("Password", width=150)
        self.accounts_tree.column("Status", width=100)
        self.accounts_tree.column("Created", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.accounts_tree.yview)
        self.accounts_tree.configure(yscrollcommand=scrollbar.set)
        
        self.accounts_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Încarcă conturile în tabel
        self.load_accounts_to_table()
        
        # Statistics frame
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.accounts_stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"Total Accounts: {len(self.accounts)}",
            font=("Arial", 14, "bold"),
            text_color="#00FF88"
        )
        self.accounts_stats_label.pack(side="left", padx=20)
        
        ctk.CTkButton(
            stats_frame,
            text="🗑️ Delete Selected",
            width=120,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.delete_selected_account
        ).pack(side="right", padx=20)
    
    def show_tokens_panel(self):
        """Afișează panoul pentru tokenuri"""
        self.clear_content_frame()
        self.header_label.configure(text="TOKENS MANAGEMENT")
        
        # Token statistics
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        token_stats = [
            ("Total Tokens:", f"{len(self.tokens)}"),
            ("Valid Tokens:", f"{self.count_valid_tokens()}"),
            ("Invalid Tokens:", f"{len(self.tokens) - self.count_valid_tokens()}"),
            ("Last Update:", datetime.now().strftime("%H:%M:%S"))
        ]
        
        for label, value in token_stats:
            stat_frame = ctk.CTkFrame(stats_frame)
            stat_frame.pack(side="left", expand=True, padx=10)
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=("Arial", 12),
                text_color="#888888"
            ).pack()
            
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=("Arial", 16, "bold"),
                text_color="#00FF88"
            ).pack()
        
        # Butoane pentru tokenuri
        buttons_frame = ctk.CTkFrame(self.content_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="📁 Import Tokens",
            width=140,
            command=self.import_tokens
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔍 Check Validity",
            width=140,
            command=self.check_tokens_validity
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="💾 Export Tokens",
            width=140,
            command=self.export_tokens
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear All",
            width=140,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.clear_tokens
        ).pack(side="left", padx=5)
        
        # Lista tokenuri
        token_frame = ctk.CTkFrame(self.content_frame)
        token_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tokens_listbox = tk.Listbox(
            token_frame,
            bg="#1A1A1A",
            fg="#FFFFFF",
            selectbackground="#00AA44",
            font=("Consolas", 10),
            height=15
        )
        self.tokens_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adaugă tokenuri în listă
        for token in self.tokens:
            display_token = token[:50] + "..." if len(token) > 50 else token
            status = "✅" if self.is_valid_token(token) else "❌"
            self.tokens_listbox.insert(tk.END, f"{status} {display_token}")
    
    def show_stats_panel(self):
        """Afișează panoul cu statistici"""
        self.clear_content_frame()
        self.header_label.configure(text="STATISTICS & ANALYTICS")
        
        # Statistici principale
        main_stats_frame = ctk.CTkFrame(self.content_frame)
        main_stats_frame.pack(fill="x", padx=20, pady=20)
        
        stats_data = [
            ("🤖 Active Bots", "0", "#00AA44"),
            ("👤 Total Accounts", str(len(self.accounts)), "#4444AA"),
            ("🔑 Valid Tokens", str(self.count_valid_tokens()), "#FFAA00"),
            ("🔌 Proxies", str(len(self.proxies)), "#AA44AA"),
            ("⏱️ Runtime", "00:00:00", "#00AAAA"),
            ("🎯 Success Rate", "0%", "#00FF88")
        ]
        
        for label, value, color in stats_data:
            stat_card = ctk.CTkFrame(main_stats_frame, width=180, height=120)
            stat_card.pack_propagate(False)
            stat_card.pack(side="left", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Arial", 14),
                text_color="#888888"
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Arial", 28, "bold"),
                text_color=color
            ).pack()
        
        # Grafic (simulat)
        chart_frame = ctk.CTkFrame(self.content_frame)
        chart_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            chart_frame,
            text="📈 Activity Overview",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=10)
        
        # Simulare grafic
        chart_canvas = ctk.CTkCanvas(
            chart_frame,
            bg="#1A1A1A",
            highlightthickness=0,
            height=200
        )
        chart_canvas.pack(fill="x", padx=20, pady=10)
        
        # Desenează un grafic simplu
        width = 800
        height = 150
        chart_canvas.config(width=width, height=height)
        
        # Linii de fundal
        for i in range(0, height, 30):
            chart_canvas.create_line(0, i, width, i, fill="#333333", width=1)
        
        # Date simulate
        data_points = [random.randint(20, 100) for _ in range(10)]
        
        # Desenează graficul
        x_step = width / (len(data_points) + 1)
        points = []
        
        for i, value in enumerate(data_points):
            x = (i + 1) * x_step
            y = height - (value / 100 * height)
            points.extend([x, y])
            
            # Punct
            chart_canvas.create_oval(x-3, y-3, x+3, y+3, fill="#00FF88", outline="")
            
            # Etichetă
            chart_canvas.create_text(x, height - 10, text=f"{value}%", fill="#888888", font=("Arial", 10))
        
        # Linie între puncte
        if points:
            chart_canvas.create_line(points, fill="#00FF88", width=2, smooth=True)
    
    def show_settings_panel(self):
        """Afișează panoul cu setări"""
        self.clear_content_frame()
        self.header_label.configure(text="SETTINGS & CONFIGURATION")
        
        settings_frame = ctk.CTkFrame(self.content_frame)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configurații generale
        general_frame = ctk.CTkFrame(settings_frame)
        general_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            general_frame,
            text="⚙️ General Settings",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        # Auto-save
        self.auto_save_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            general_frame,
            text="Auto-save data",
            variable=self.auto_save_var,
            font=("Arial", 14)
        ).pack(anchor="w", padx=20, pady=5)
        
        # Auto-start
        self.auto_start_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            general_frame,
            text="Auto-start on launch",
            variable=self.auto_start_var,
            font=("Arial", 14)
        ).pack(anchor="w", padx=20, pady=5)
        
        # Theme
        theme_frame = ctk.CTkFrame(general_frame)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="Theme:",
            font=("Arial", 14)
        ).pack(side="left", padx=5)
        
        self.theme_var = tk.StringVar(value="Dark")
        theme_combo = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "Blue"],
            variable=self.theme_var,
            width=100
        )
        theme_combo.pack(side="left", padx=5)
        
        # Butoane acțiune
        action_frame = ctk.CTkFrame(settings_frame)
        action_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="💾 Save Settings",
            width=140,
            command=self.save_settings
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🔄 Reset to Default",
            width=140,
            command=self.reset_settings
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            action_frame,
            text="🗑️ Clear All Data",
            width=140,
            fg_color="#AA4444",
            hover_color="#CC6666",
            command=self.clear_all_data
        ).pack(side="left", padx=10)
        
        # Info
        info_frame = ctk.CTkFrame(settings_frame)
        info_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Application Information",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        info_text = """
        • Version: 2.0.0
        • Developer: BRF Team
        • Last Update: December 2024
        • Status: Stable
        • Support: brf-support@example.com
        """
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Consolas", 12),
            text_color="#888888",
            justify="left"
        ).pack(anchor="w", padx=20, pady=10)
    
    def create_dashboard_widgets(self):
        """Creează widget-uri pentru dashboard"""
        # Recent activity
        activity_frame = ctk.CTkFrame(self.content_frame)
        activity_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            activity_frame,
            text="📋 Recent Activity",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        
        # Simulate activity log
        activity_log = tk.Text(
            activity_frame,
            height=10,
            bg="#1A1A1A",
            fg="#00FF88",
            font=("Consolas", 10),
            wrap="word"
        )
        activity_log.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add some sample activity
        activities = [
            f"[{datetime.now().strftime('%H:%M:%S')}] System started",
            f"[{datetime.now().strftime('%H:%M:%S')}] Loaded {len(self.accounts)} accounts",
            f"[{datetime.now().strftime('%H:%M:%S')}] Loaded {len(self.tokens)} tokens",
            f"[{datetime.now().strftime('%H:%M:%S')}] Ready for operation"
        ]
        
        for activity in activities:
            activity_log.insert(tk.END, activity + "\n")
        
        activity_log.config(state="disabled")
    
    def start_bots_farming(self):
        """Pornește botii de farming"""
        if not self.bots_running:
            self.bots_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_label.configure(text="Status: Bots Running")
            
            # Pornește thread-ul botului
            self.bot_thread = threading.Thread(target=self.bot_worker, daemon=True)
            self.bot_thread.start()
            
            self.log_message("🤖 Bots farming started!")
    
    def stop_bots_farming(self):
        """Oprește botii de farming"""
        if self.bots_running:
            self.bots_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.status_label.configure(text="Status: Stopped")
            
            self.log_message("🛑 Bots farming stopped!")
    
    def bot_worker(self):
        """Funcția principală a botului"""
        while self.bots_running:
            # Simulează activitatea botului
            time.sleep(float(self.delay_var.get()))
            
            # Generează un mesaj random
            messages = [
                "Creating new account...",
                "Extracting security token...",
                "Verifying account...",
                "Saving data to file...",
                "Account created successfully!"
            ]
            
            message = random.choice(messages)
            self.log_message(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            
            # Update statistici
            self.update_dashboard_stats()
    
    def log_message(self, message):
        """Adaugă mesaj în log"""
        self.bot_log.insert(tk.END, message + "\n")
        self.bot_log.see(tk.END)
        self.root.update()
    
    def update_dashboard_stats(self):
        """Actualizează statisticile din dashboard"""
        self.bots_label.configure(text=f"Bots: {1 if self.bots_running else 0}")
        self.accounts_label.configure(text=f"Accounts: {len(self.accounts)}")
        self.tokens_label.configure(text=f"Tokens: {len(self.tokens)}")
    
    def add_proxy(self):
        """Adaugă un proxy nou"""
        dialog = ctk.CTkInputDialog(
            text="Enter proxy (format: ip:port:user:pass or ip:port):",
            title="Add Proxy"
        )
        
        proxy = dialog.get_input()
        if proxy and proxy.strip():
            self.proxies.append(proxy.strip())
            self.proxy_listbox.insert(tk.END, proxy.strip())
            self.proxy_count_label.configure(text=f"Total Proxies: {len(self.proxies)}")
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
                
                self.proxy_count_label.configure(text=f"Total Proxies: {len(self.proxies)}")
                self.save_proxies()
                
                messagebox.showinfo("Success", f"Imported {len(new_proxies)} proxies!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import proxies: {e}")
    
    def clear_proxies(self):
        """Șterge toate proxy-urile"""
        if messagebox.askyesno("Confirm", "Delete all proxies?"):
            self.proxies.clear()
            self.proxy_listbox.delete(0, tk.END)
            self.proxy_count_label.configure(text="Total Proxies: 0")
            self.save_proxies()
    
    def add_account_dialog(self):
        """Dialog pentru adăugare cont"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Account")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Form fields
        ctk.CTkLabel(dialog, text="Username:", font=("Arial", 14)).pack(pady=10)
        username_entry = ctk.CTkEntry(dialog, width=300)
        username_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Password:", font=("Arial", 14)).pack(pady=10)
        password_entry = ctk.CTkEntry(dialog, width=300, show="*")
        password_entry.pack(pady=5)
        
        def save_account():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if username and password:
                account = {
                    "username": username,
                    "password": password,
                    "status": "Active",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.accounts.append(account)
                self.save_accounts()
                self.load_accounts_to_table()
                dialog.destroy()
                messagebox.showinfo("Success", "Account added successfully!")
            else:
                messagebox.showwarning("Warning", "Please fill all fields!")
        
        ctk.CTkButton(
            dialog,
            text="💾 Save Account",
            command=save_account,
            width=150,
            height=40
        ).pack(pady=20)
    
    def load_accounts_to_table(self):
        """Încarcă conturile în tabel"""
        # Clear table
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        
        # Add accounts
        for account in self.accounts:
            self.accounts_tree.insert("", "end", values=(
                account.get("username", ""),
                account.get("password", ""),
                account.get("status", "Active"),
                account.get("created", "")
            ))
        
        # Update statistics
        self.accounts_stats_label.configure(text=f"Total Accounts: {len(self.accounts)}")
        self.update_dashboard_stats()
    
    def import_accounts(self):
        """Importă conturi din fișier"""
        file_path = filedialog.askopenfilename(
            title="Select accounts file",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'r') as f:
                        new_accounts = json.load(f)
                else:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        new_accounts = []
                        
                        for line in lines:
                            if ':' in line:
                                username, password = line.strip().split(':', 1)
                                new_accounts.append({
                                    "username": username.strip(),
                                    "password": password.strip(),
                                    "status": "Active",
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                
                self.accounts.extend(new_accounts)
                self.save_accounts()
                self.load_accounts_to_table()
                
                messagebox.showinfo("Success", f"Imported {len(new_accounts)} accounts!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import accounts: {e}")
    
    def generate_random_accounts(self):
        """Generează conturi random"""
        try:
            count = int(ctk.CTkInputDialog(
                text="How many accounts to generate?",
                title="Generate Accounts"
            ).get_input() or "10")
            
            first_names = ["Alex", "Max", "Leo", "Sam", "Ryan", "Noah", "Liam", "Ethan"]
            second_names = ["Gamer", "Player", "Pro", "Master", "Legend", "Hero", "Star"]
            
            for _ in range(count):
                username = f"{random.choice(first_names)}{random.choice(second_names)}{random.randint(100, 9999)}"
                password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))
                
                self.accounts.append({
                    "username": username,
                    "password": password,
                    "status": "Active",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            self.save_accounts()
            self.load_accounts_to_table()
            messagebox.showinfo("Success", f"Generated {count} random accounts!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate accounts: {e}")
    
    def export_accounts(self):
        """Exportă conturi în fișier"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")],
            title="Save accounts to file"
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as f:
                        json.dump(self.accounts, f, indent=2)
                else:
                    with open(file_path, 'w') as f:
                        for account in self.accounts:
                            f.write(f"{account['username']}:{account['password']}\n")
                
                messagebox.showinfo("Success", f"Accounts exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export accounts: {e}")
    
    def delete_selected_account(self):
        """Șterge contul selectat"""
        selection = self.accounts_tree.selection()
        if selection:
            if messagebox.askyesno("Confirm", "Delete selected account?"):
                for item in selection:
                    index = self.accounts_tree.index(item)
                    if index < len(self.accounts):
                        del self.accounts[index]
                
                self.save_accounts()
                self.load_accounts_to_table()
        else:
            messagebox.showwarning("Warning", "Please select an account first!")
    
    def import_tokens(self):
        """Importă tokenuri din fișier"""
        file_path = filedialog.askopenfilename(
            title="Select tokens file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    new_tokens = [line.strip() for line in f if line.strip()]
                
                self.tokens.extend(new_tokens)
                self.save_tokens()
                self.show_tokens_panel()
                
                messagebox.showinfo("Success", f"Imported {len(new_tokens)} tokens!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import tokens: {e}")
    
    def check_tokens_validity(self):
        """Verifică validitatea tokenurilor"""
        messagebox.showinfo("Info", "Token validation would require API calls to Roblox.\nThis is a demo function.")
    
    def export_tokens(self):
        """Exportă tokenuri în fișier"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save tokens to file"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for token in self.tokens:
                        f.write(f"{token}\n")
                
                messagebox.showinfo("Success", f"Tokens exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export tokens: {e}")
    
    def clear_tokens(self):
        """Șterge toate tokenurile"""
        if messagebox.askyesno("Confirm", "Delete all tokens?"):
            self.tokens.clear()
            self.save_tokens()
            self.show_tokens_panel()
    
    def count_valid_tokens(self):
        """Numără tokenurile valide"""
        # În demo, considerăm toate tokenurile ca valide
        return len(self.tokens)
    
    def is_valid_token(self, token):
        """Verifică dacă un token este valid"""
        # În demo, considerăm toate tokenurile ca valide
        return True
    
    def toggle_proxy_support(self):
        """Comută suportul pentru proxy"""
        if self.proxy_enabled.get():
            self.status_label.configure(text="Status: Proxy Enabled")
        else:
            self.status_label.configure(text="Status: Proxy Disabled")
    
    def start_all_bots(self):
        """Pornește toți botii"""
        messagebox.showinfo("Info", "Starting all bots...")
        self.start_bots_farming()
    
    def stop_all_bots(self):
        """Oprește toți botii"""
        messagebox.showinfo("Info", "Stopping all bots...")
        self.stop_bots_farming()
    
    def quick_setup(self):
        """Configurare rapidă"""
        messagebox.showinfo("Quick Setup", "Quick setup would configure optimal settings.\nThis is a demo function.")
    
    def save_settings(self):
        """Salvează setările"""
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def reset_settings(self):
        """Resetează setările"""
        if messagebox.askyesno("Confirm", "Reset all settings to default?"):
            messagebox.showinfo("Settings", "Settings reset to default!")
    
    def clear_all_data(self):
        """Șterge toate datele"""
        if messagebox.askyesno("Confirm", "Clear ALL data? This cannot be undone!"):
            self.accounts.clear()
            self.proxies.clear()
            self.tokens.clear()
            self.save_accounts()
            self.save_proxies()
            self.save_tokens()
            messagebox.showinfo("Info", "All data cleared!")
            self.load_accounts_to_table()
            self.show_main_panel()
    
    def save_accounts(self):
        """Salvează conturile în fișier"""
        try:
            with open('accounts.json', 'w') as f:
                json.dump(self.accounts, f, indent=2)
        except:
            pass
    
    def save_proxies(self):
        """Salvează proxy-urile în fișier"""
        try:
            with open('proxies.txt', 'w') as f:
                for proxy in self.proxies:
                    f.write(f"{proxy}\n")
        except:
            pass
    
    def save_tokens(self):
        """Salvează tokenurile în fișier"""
        try:
            with open('tokens.txt', 'w') as f:
                for token in self.tokens:
                    f.write(f"{token}\n")
        except:
            pass
    
    def load_saved_data(self):
        """Încarcă datele salvate"""
        try:
            # Load accounts
            if os.path.exists('accounts.json'):
                with open('accounts.json', 'r') as f:
                    self.accounts = json.load(f)
            
            # Load proxies
            if os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
            
            # Load tokens
            if os.path.exists('tokens.txt'):
                with open('tokens.txt', 'r') as f:
                    self.tokens = [line.strip() for line in f if line.strip()]
        except:
            pass

# Rulează aplicația
if __name__ == "__main__":
    app = BRFControlPanel()
