import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
from datetime import datetime

class RobloxUltimateGenerator:
    def __init__(self):
        self.driver = None
        self.accounts_created = 0
        self.animation_chars = "▓▒░█★✦✧✩☆♡♥♦♣♠♪♫☼►◄▲▼◆◇■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯☀☁☂☃☄☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☸☹☺☻☼☽☾☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿⚀⚁⚂⚃⚄⚅⚆⚇⚈⚉⚊⚋⚌⚍⚎⚏⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛⚜⚝⚞⚟⚠⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯⚰⚱⚲⚳⚴⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿⛀⛁⛂⛃⛄⛅⛆⛇⛈⛉⛊⛋⛌⛍⛎⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡⛢⛣⛤⛥⛦⛧⛨⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿"
        
    def animate_text(self, text, delay=0.02):
        """Afișează text cu animație cool"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def loading_animation(self, duration=3, text="Se încarcă"):
        """Animație de loading"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            frame = frames[i % len(frames)]
            print(f"\r{text} {frame}", end="", flush=True)
            time.sleep(0.1)
            i += 1
        print("\r" + " " * (len(text) + 2) + "\r", end="")

    def setup_new_browser(self):
        """Configurează un browser nou de fiecare dată"""
        self.animate_text("🔄 Pornesc browser nou...", 0.03)
        self.loading_animation(2)
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--start-maximized")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.animate_text("✅ Browser nou pornit! 🎮", 0.02)
            return True
        except Exception as e:
            self.animate_text(f"❌ Eroare browser: {e}", 0.02)
            return False
    
    def generate_unique_username(self):
        """Generează username-uri 100% unice"""
        prefixes = ["Shadow", "Quantum", "Neon", "Cyber", "Alpha", "Beta", "Gamma", "Omega", 
                   "Stealth", "Phantom", "Ghost", "Wolf", "Eagle", "Tiger", "Dragon", "Falcon"]
        suffixes = ["Warrior", "Hunter", "Slayer", "Master", "Legend", "Killer", "Destroyer", "Pro",
                   "God", "King", "Queen", "Lord", "Sniper", "Assassin", "Ninja", "Samurai"]
        
        while True:
            username = f"{random.choice(prefixes)}{random.choice(suffixes)}{random.randint(1000, 9999)}"
            if not self.check_existing_account(username):
                return username
    
    def generate_strong_password(self):
        """Generează parole foarte puternice"""
        length = 14
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%&*"
        
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        all_chars = lowercase + uppercase + digits + symbols
        password += [random.choice(all_chars) for _ in range(length - 4)]
        
        random.shuffle(password)
        return ''.join(password)
    
    def select_month_correctly(self, month_number):
        """Selectează luna corectă cu numele în loc de număr"""
        self.animate_text(f"📅 Selectez luna pentru {month_number}...", 0.02)
        
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April", 
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        
        month_name = month_names[month_number]
        
        methods = [
            self._select_month_by_visible_text,
            self._select_month_by_value,
            self._select_month_by_index,
            self._select_month_by_javascript
        ]
        
        for method in methods:
            try:
                if method(month_name, month_number):
                    self.animate_text(f"✅ Luna '{month_name}' selectată! 🌙", 0.02)
                    return True
            except Exception as e:
                continue
        
        self.animate_text("❌ Nici o metodă nu a funcționat pentru lună", 0.02)
        return False
    
    def _select_month_by_visible_text(self, month_name, month_number):
        """Selectează luna după textul vizibil"""
        try:
            month_select = Select(self.driver.find_element(By.ID, "MonthDropdown"))
            month_select.select_by_visible_text(month_name)
            return True
        except:
            return False
    
    def _select_month_by_value(self, month_name, month_number):
        """Selectează luna după valoare"""
        try:
            month_select = Select(self.driver.find_element(By.ID, "MonthDropdown"))
            month_select.select_by_value(str(month_number))
            return True
        except:
            return False
    
    def _select_month_by_index(self, month_name, month_number):
        """Selectează luna după index"""
        try:
            month_select = Select(self.driver.find_element(By.ID, "MonthDropdown"))
            month_select.select_by_index(month_number)
            return True
        except:
            return False
    
    def _select_month_by_javascript(self, month_name, month_number):
        """Selectează luna cu JavaScript"""
        try:
            script = f"""
            var dropdown = document.getElementById('MonthDropdown');
            dropdown.value = '{month_number}';
            var event = new Event('change', {{ bubbles: true }});
            dropdown.dispatchEvent(event);
            """
            self.driver.execute_script(script)
            time.sleep(1)
            return True
        except:
            return False
    
    def select_day_and_year(self, day, year):
        """Selectează ziua și anul"""
        try:
            # Selectează ziua
            self.animate_text(f"📅 Selectez ziua {day}...", 0.02)
            day_select = Select(self.driver.find_element(By.ID, "DayDropdown"))
            day_select.select_by_value(str(day))
            self.animate_text("✅ Ziua selectată! 📆", 0.02)
            time.sleep(1)
            
            # Selectează anul
            self.animate_text(f"📅 Selectez anul {year}...", 0.02)
            year_select = Select(self.driver.find_element(By.ID, "YearDropdown"))
            year_select.select_by_value(str(year))
            self.animate_text("✅ Anul selectat! 🎂", 0.02)
            time.sleep(1)
            
            return True
        except Exception as e:
            self.animate_text(f"❌ Eroare la zi/an: {e}", 0.02)
            return False
    
    def navigate_to_signup(self):
        """Navighează la pagina de signup"""
        self.animate_text("🌐 Navighez la Roblox...", 0.02)
        self.loading_animation(3, "Se încarcă Roblox")
        
        try:
            self.driver.get("https://www.roblox.com")
            time.sleep(3)
            
            # Caută butonul de Sign Up
            signup_selectors = [
                "//span[contains(text(), 'Sign Up')]",
                "//a[contains(text(), 'Sign Up')]",
                "//button[contains(text(), 'Sign Up')]",
            ]
            
            for selector in signup_selectors:
                try:
                    signup_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    self.animate_text(f"✅ Buton Sign Up găsit! 🎯", 0.02)
                    signup_btn.click()
                    time.sleep(3)
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.animate_text(f"❌ Eroare navigare: {e}", 0.02)
            return False
    
    def fill_form_with_style(self, username, password, birth_date):
        """Completează formularul cu stil și animații"""
        try:
            self.animate_text("📝 Încep completarea formularului...", 0.02)
            
            # Username
            self.animate_text(f"👤 Introduc username: {username}", 0.01)
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "signup-username"))
            )
            username_field.clear()
            self.slow_type_with_animation(username_field, username)
            self.loading_animation(2, "Verific username")
            
            # Password
            self.animate_text(f"🔐 Introduc parola: {password}", 0.01)
            password_field = self.driver.find_element(By.ID, "signup-password")
            password_field.clear()
            self.slow_type_with_animation(password_field, password)
            time.sleep(1)
            
            # Data nașterii
            month, day, year = birth_date
            self.animate_text(f"🎂 Setez data nașterii: {month}/{day}/{year}", 0.02)
            
            # Selectează luna, ziua, anul
            month_success = self.select_month_correctly(month)
            day_year_success = self.select_day_and_year(day, year)
            
            # Genul (opțional)
            self.animate_text("🚻 Selectez genul...", 0.02)
            try:
                gender = random.choice(["Male", "Female"])
                gender_selector = f"//label[contains(., '{gender}')]"
                gender_btn = self.driver.find_element(By.XPATH, gender_selector)
                gender_btn.click()
                self.animate_text(f"✅ Gen selectat: {gender} 👨‍🎤👩‍🎤", 0.02)
            except:
                self.animate_text("⚠️  Genul nu a putut fi selectat - continuăm 💁", 0.02)
            
            if month_success and day_year_success:
                self.animate_text("🎉 FORMULAR COMPLETAT CU SUCCES! 🎉", 0.01)
                return True
            else:
                self.animate_text("⚠️  Formular completat parțial - continuăm", 0.02)
                return True
            
        except Exception as e:
            self.animate_text(f"❌ Eroare formular: {e}", 0.02)
            return False
    
    def submit_form_with_flair(self):
        """Trimite formularul cu stil"""
        try:
            self.animate_text("🎯 Trimit formularul...", 0.02)
            self.loading_animation(2, "Se trimite")
            
            # Găsește butonul de submit
            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "signup-button"))
            )
            
            # Animatie înainte de click
            for i in range(3):
                print(f"\r🚀 Trimit în {3-i}...", end="", flush=True)
                time.sleep(1)
            print("\r" + " " * 15 + "\r", end="")
            
            submit_btn.click()
            self.animate_text("✅ Formular trimis! 📤", 0.02)
            
            # Așteaptă rezultatul
            self.animate_text("⏳ Aștept răspunsul...", 0.02)
            self.loading_animation(8, "Se procesează")
            
            return self.check_success()
            
        except Exception as e:
            self.animate_text(f"❌ Eroare submit: {e}", 0.02)
            return False
    
    def check_success(self):
        """Verifică dacă contul a fost creat"""
        try:
            current_url = self.driver.current_url.lower()
            
            success_indicators = ["home", "welcome", "games"]
            if any(indicator in current_url for indicator in success_indicators):
                return True
            
            if "register" not in current_url and "signup" not in current_url:
                return True
                
            return False
        except:
            return False
    
    def slow_type_with_animation(self, element, text):
        """Scrie text cu animație cool"""
        for char in text:
            element.send_keys(char)
            # Animatie de typing
            print(f"\r✏️  Scriu: {text[:text.index(char)+1]}█", end="", flush=True)
            time.sleep(random.uniform(0.05, 0.1))
        print("\r" + " " * (len(text) + 10) + "\r", end="")
    
    def generate_birth_date(self):
        """Generează data nașterii"""
        year = random.randint(1985, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return month, day, year
    
    def check_existing_account(self, username):
        """Verifică dacă username-ul există deja"""
        if not os.path.exists("accounts.txt"):
            return False
        
        try:
            with open("accounts.txt", "r", encoding="utf-8") as f:
                return username in f.read()
        except:
            return False
    
    def save_account(self, username, password):
        """Salvează contul în fișier cu animație"""
        self.animate_text("💾 Salvez contul...", 0.02)
        self.loading_animation(2, "Se salvează")
        
        with open("accounts.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] 👤 {username} | 🔐 {password}\n")
        
        self.animate_text("✅ Cont salvat în accounts.txt! 📁", 0.02)
    
    def show_success_celebration(self, username):
        """Afișează animație de succes"""
        celebration = f"""
        {'🎉' * 20}
        
        🎊 CONT CREAT CU SUCCES! 🎊
        
        👤 Username: {username}
        📊 Total conturi: {self.accounts_created}
        💾 Salvat în: accounts.txt
        
        {'🎉' * 20}
        """
        self.animate_text(celebration, 0.01)
    
    def show_awesome_banner(self):
        """Afișează banner-ul ultra cool"""
        banner = """
        ╔══════════════════════════════════════════════════════════════╗
        ║                                                              ║
        ║    🚀✨ ROBLOX ULTIMATE GENERATOR 9000 ✨🚀                  ║
        ║                                                              ║
        ║    ⚡ CREARE CONTURI FULL AUTO ⚡                            ║
        ║    🌙 LUNA CORECTĂ - JANUARY, FEBRUARY... 🌙                ║
        ║    🎨 DESIGN ANIMAT SUPER COOL 🎨                          ║
        ║    💾 SALVARE AUTOMATĂ ÎN accounts.txt 💾                  ║
        ║    🎯 TU STAI PE SPATE ȘI TE LAZI! 🎯                      ║
        ║                                                              ║
        ║    🔥 GENERATOR PROFESIONIST - ZERO EFFORT 🔥               ║
        ║                                                              ║
        ╚══════════════════════════════════════════════════════════════╝
        """
        self.animate_text(banner, 0.002)
    
    def create_single_account(self):
        """Creează un singur cont"""
        try:
            self.animate_text("\n" + "✨" * 30, 0.01)
            self.animate_text("🚀 ÎNCEP CREAREA CONTULUI ULTIMAT", 0.02)
            self.animate_text("✨" * 30, 0.01)
            
            # Generează date
            username = self.generate_unique_username()
            password = self.generate_strong_password()
            birth_date = self.generate_birth_date()
            
            self.animate_text(f"👤 Username: {username}", 0.01)
            self.animate_text(f"🔐 Password: {password}", 0.01)
            self.animate_text(f"🎂 Data naștere: {birth_date[0]}/{birth_date[1]}/{birth_date[2]}", 0.02)
            
            # Navigare și formular
            if not self.navigate_to_signup():
                return False
            
            if not self.fill_form_with_style(username, password, birth_date):
                return False
            
            # Submit și verificare
            if self.submit_form_with_flair():
                self.save_account(username, password)
                self.accounts_created += 1
                self.show_success_celebration(username)
                return True
            
            return False
            
        except Exception as e:
            self.animate_text(f"❌ Eroare: {e}", 0.02)
            return False
    
    def run_ultimate_generator(self):
        """Rulează generatorul ultimate"""
        self.show_awesome_banner()
        
        self.animate_text("\n🔥 PORNESC GENERATORUL ULTIMAT!", 0.02)
        self.animate_text("🎮 Totul este automat - tu te lazi! 🛋️", 0.02)
        self.animate_text("⏳ Pornire în 3 secunde...", 0.02)
        
        for i in range(3, 0, -1):
            print(f"\r🚀 {i}...", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 10 + "\r", end="")
        
        attempt = 0
        while True:
            attempt += 1
            self.animate_text(f"\n🎯 ÎNCERCAREA #{attempt}", 0.02)
            
            # Browser nou
            if not self.setup_new_browser():
                continue
            
            # Creează cont
            success = self.create_single_account()
            
            # Închide browser
            try:
                self.driver.quit()
            except:
                pass
            
            # Pauză
            wait_time = random.randint(10, 15)
            self.animate_text(f"⏳ Următorul cont în {wait_time}s...", 0.02)
            
            for i in range(wait_time, 0, -1):
                print(f"\r⏰ {i}s ", end="", flush=True)
                time.sleep(1)
            print("\r" + " " * 10 + "\r", end="")

if __name__ == "__main__":
    try:
        generator = RobloxUltimateGenerator()
        generator.run_ultimate_generator()
    except KeyboardInterrupt:
        print(f"\n\n🛑 Generator oprit! Conturi create: {generator.accounts_created}")
        print("📁 Conturile sunt în: accounts.txt")
    except Exception as e:
        print(f"\n\n💥 Eroare: {e}")
