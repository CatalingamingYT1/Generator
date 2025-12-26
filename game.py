import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser
import socket, threading, json, time, subprocess, urllib.request

# CONFIGURARE
NGROK_TOKEN = "2djWLmNtLhALFfZ74L1K1mcXSV7_3uJhFnqkWjh2UgeDuZzuS"
PORT = 12345

class ObsidianEliteCustomSize:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Obsidian Studio - Custom Size Edition")
        self.root.geometry("1500x900")
        self.root.configure(bg="#050505")

        self.sock = None
        self.clients = []
        self.color = "#1A1A1B"
        self.tool = "brush"
        self.size = 8  # Dimensiunea curentă (controlată de slider)
        self.is_host = False
        self.my_name = "User"

        self.setup_ui()
        self.show_menu()

    def setup_ui(self):
        # --- TOP BAR ---
        self.top_bar = tk.Frame(self.root, bg="#0A0A0A", height=60)
        self.top_bar.pack(side="top", fill="x")
        
        tk.Label(self.top_bar, text="♦ OBSIDIAN STUDIO PRO", fg="#00E5FF", 
                 bg="#0A0A0A", font=("Impact", 24)).pack(side="left", padx=25)

        self.player_count_lbl = tk.Label(self.top_bar, text="PLAYERS: 1", fg="#888", 
                                        bg="#0A0A0A", font=("Consolas", 11, "bold"))
        self.player_count_lbl.pack(side="right", padx=25)

        # --- MAIN CONTAINER ---
        self.main_container = tk.Frame(self.root, bg="#050505")
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # 1. SIDEBAR STÂNGA (UNELTE + SIZE SLIDER)
        self.side_bar = tk.Frame(self.main_container, bg="#0A0A0A", width=80)
        self.side_bar.pack(side="left", fill="y", padx=5)
        
        tools = [("✏️", "pencil"), ("🖌️", "brush"), ("🧽", "eraser"), ("🗑️", "clear")]
        for icon, name in tools:
            cmd = self.clear_all if name == "clear" else lambda n=name: self.set_tool(n)
            btn = tk.Button(self.side_bar, text=icon, font=("Arial", 18), bg="#0A0A0A", fg="white",
                           relief="flat", activebackground="#222", command=cmd)
            btn.pack(pady=10, fill="x")

        # Culoare
        self.color_ind = tk.Frame(self.side_bar, bg=self.color, width=40, height=40, cursor="hand2", relief="solid", borderwidth=1)
        self.color_ind.pack(pady=10)
        self.color_ind.bind("<Button-1>", lambda e: self.choose_color())

        # SLIDER PENTRU MĂRIME (NOU!)
        tk.Label(self.side_bar, text="SIZE", fg="#555", bg="#0A0A0A", font=("Arial", 8, "bold")).pack(pady=(10, 0))
        self.size_slider = tk.Scale(self.side_bar, from_=1, to=100, orient="vertical", 
                                   bg="#0A0A0A", fg="#00E5FF", highlightthickness=0, 
                                   troughcolor="#151515", length=200, command=self.update_size)
        self.size_slider.set(self.size)
        self.size_slider.pack(pady=5)

        # 2. CHAT ÎN DREAPTA
        self.chat_frame = tk.Frame(self.main_container, bg="#0A0A0A", width=300)
        self.chat_frame.pack(side="right", fill="y", padx=5)
        self.chat_frame.pack_propagate(False)
        
        tk.Label(self.chat_frame, text="STUDIO CHAT", fg="#555", bg="#0A0A0A", font=("Arial", 9, "bold")).pack(pady=10)
        
        self.chat_box = tk.Text(self.chat_frame, bg="#050505", fg="#EEE", font=("Segoe UI", 10), 
                               state="disabled", borderwidth=0, highlightthickness=0)
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.msg_entry = tk.Entry(self.chat_frame, bg="#151515", fg="white", borderwidth=0, insertbackground="white")
        self.msg_entry.pack(fill="x", padx=10, pady=15, ipady=10)
        self.msg_entry.bind("<Return>", self.send_chat_msg)

        # 3. CANVAS CENTRAL
        canvas_border = tk.Frame(self.main_container, bg="#1A1A1B", padx=2, pady=2)
        canvas_border.pack(side="left", fill="both", expand=True, padx=5)
        
        self.canvas = tk.Canvas(canvas_border, bg="white", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)

    def update_size(self, val):
        self.size = int(val)

    def set_tool(self, name):
        self.tool = name
        self.color_ind.config(bg="white" if name == "eraser" else self.color)

    def choose_color(self):
        c = colorchooser.askcolor()[1]
        if c: 
            self.color = c
            self.tool = "brush"
            self.color_ind.config(bg=c)

    def show_menu(self):
        self.overlay = tk.Frame(self.root, bg="#050505")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        box = tk.Frame(self.overlay, bg="#0A0A0A", padx=50, pady=50)
        box.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(box, text="SELECT MODE", font=("Arial", 20, "bold"), fg="white", bg="#0A0A0A").pack(pady=20)
        tk.Button(box, text="HOST STUDIO", bg="#00E5FF", fg="black", font=("Arial", 11, "bold"), 
                  width=22, height=2, relief="flat", command=lambda: self.init_net("host")).pack(pady=10)
        tk.Button(box, text="JOIN STUDIO", bg="#1A1A1B", fg="white", font=("Arial", 11, "bold"), 
                  width=22, height=2, relief="flat", command=lambda: self.init_net("client")).pack()

    def init_net(self, mode):
        name = simpledialog.askstring("Name", "Username:")
        self.my_name = name if name else "User"
        self.overlay.destroy()
        if mode == "host":
            self.is_host = True
            threading.Thread(target=self.run_server, daemon=True).start()
        else:
            addr = simpledialog.askstring("Join", "Paste Link:")
            if addr: threading.Thread(target=self.run_client, args=(addr,), daemon=True).start()
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_move)

    def send_chat_msg(self, e=None):
        txt = self.msg_entry.get().strip()
        if txt:
            msg_data = json.dumps({'type': 'chat', 'user': self.my_name, 'text': txt})
            self.display_msg(f"{self.my_name}: {txt}")
            if self.is_host: self.broadcast(msg_data, None)
            elif self.sock: self.sock.sendall((msg_data + "\n").encode())
            self.msg_entry.delete(0, tk.END)

    def display_msg(self, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def run_server(self):
        try:
            subprocess.run(f"ngrok config add-authtoken {NGROK_TOKEN}", shell=True)
            subprocess.Popen(f"ngrok tcp {PORT}", shell=True, stdout=subprocess.DEVNULL)
            time.sleep(4)
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as res:
                url = json.loads(res.read().decode())['tunnels'][0]['public_url'].replace("tcp://", "")
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                self.display_msg(f"Link: {url}")
        except: self.display_msg("System: Error with Ngrok.")
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', PORT)); s.listen(5)
        while True:
            c_sock, _ = s.accept()
            self.clients.append(c_sock)
            self.player_count_lbl.config(text=f"PLAYERS: {len(self.clients)+1}")
            threading.Thread(target=self.handle_client, args=(c_sock,), daemon=True).start()

    def handle_client(self, conn):
        buf = ""
        while True:
            try:
                data = conn.recv(4096).decode()
                if not data: break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    msg = json.loads(line)
                    if msg.get('type') == 'chat': self.root.after(0, self.display_msg, f"{msg['user']}: {msg['text']}")
                    elif msg.get('type') == 'clear': self.root.after(0, self.canvas.delete, "all")
                    else: self.root.after(0, self.draw_remote, msg)
                    self.broadcast(line, conn)
            except: break
        if conn in self.clients: self.clients.remove(conn)

    def run_client(self, addr):
        try:
            h, p = addr.split(":"); self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((h, int(p))); self.display_msg("System: Connected!")
            buf = ""
            while True:
                data = self.sock.recv(4096).decode()
                if not data: break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1); msg = json.loads(line)
                    if msg.get('type') == 'chat': self.root.after(0, self.display_msg, f"{msg['user']}: {msg['text']}")
                    elif msg.get('type') == 'clear': self.root.after(0, self.canvas.delete, "all")
                    else: self.root.after(0, self.draw_remote, msg)
        except: self.display_msg("System: Failed to connect.")

    def broadcast(self, msg, skip):
        for c in self.clients:
            if c != skip:
                try: c.sendall((msg + "\n").encode())
                except: pass

    def on_press(self, e):
        self.cw, self.ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.last_rx, self.last_ry = e.x/self.cw, e.y/self.ch

    def on_move(self, e):
        rx, ry = e.x/self.cw, e.y/self.ch
        col = "white" if self.tool == "eraser" else self.color
        # Folosește self.size care vine de la slider
        self.canvas.create_line(self.last_rx*self.cw, self.last_ry*self.ch, e.x, e.y, fill=col, width=self.size, capstyle="round", smooth=True)
        msg = json.dumps({'x1':self.last_rx, 'y1':self.last_ry, 'x2':rx, 'y2':ry, 'c':col, 's':self.size})
        if self.is_host: self.broadcast(msg, None)
        elif self.sock: self.sock.sendall((msg + "\n").encode())
        self.last_rx, self.last_ry = rx, ry

    def draw_remote(self, m):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.create_line(m['x1']*w, m['y1']*h, m['x2']*w, m['y2']*h, fill=m['c'], width=m['s'], capstyle="round", smooth=True)

    def clear_all(self):
        self.canvas.delete("all")
        msg = json.dumps({'type': 'clear'})
        if self.is_host: self.broadcast(msg, None)
        elif self.sock: self.sock.sendall((msg + "\n").encode())

if __name__ == "__main__":
    ObsidianEliteCustomSize().root.mainloop()
