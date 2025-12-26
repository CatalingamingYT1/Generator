import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser
import socket, threading, json, time, subprocess, urllib.request

# CONFIGURARE
NGROK_TOKEN = "2djWLmNtLhALFfZ74L1K1mcXSV7_3uJhFnqkWjh2UgeDuZzuS"
PORT = 12345

class ObsidianEliteMaxShapes:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Obsidian Elite MAX - Shapes & Giant Brush")
        self.root.geometry("1400x900")
        self.root.configure(bg="#050505")

        self.sock = None
        self.clients = []
        self.color = "#1A1A1B"
        self.tool = "brush"
        self.size = 8
        self.is_host = False
        self.my_name = "User"
        
        # Variabile pentru forme
        self.start_x, self.start_y = 0, 0
        self.temp_shape = None

        self.setup_ui()
        self.show_menu()

    def setup_ui(self):
        # --- TOP BAR ---
        self.top_bar = tk.Frame(self.root, bg="#0A0A0A", height=50)
        self.top_bar.pack(side="top", fill="x")
        
        self.logo_label = tk.Label(self.top_bar, text="♦ OBSIDIAN SHAPES PRO", fg="#00E5FF", bg="#0A0A0A", font=("Impact", 20))
        self.logo_label.pack(side="left", padx=20)

        self.player_count_lbl = tk.Label(self.top_bar, text="PLAYERS: 1", fg="#00E5FF", bg="#0A0A0A", font=("Consolas", 10, "bold"))
        self.player_count_lbl.pack(side="right", padx=20)

        # --- SIDEBAR (EXTINS CU FORME) ---
        self.side_bar = tk.Frame(self.root, bg="#0A0A0A", width=70)
        self.side_bar.pack(side="left", fill="y")
        
        tools = [
            ("🖌️", "brush", 8),
            ("📏", "line", 4),
            ("⬜", "rect", 4),
            ("⭕", "oval", 4),
            ("🧽", "eraser", 50),
            ("🗑️", "clear", 0)
        ]

        for icon, name, sz in tools:
            cmd = self.clear_all if name == "clear" else lambda n=name, s=sz: self.set_tool(n, s)
            btn = tk.Button(self.side_bar, text=icon, font=("Arial", 18), bg="#0A0A0A", fg="white",
                           relief="flat", activebackground="#222", command=cmd)
            btn.pack(pady=10, fill="x")

        # Color Indicator
        self.color_ind = tk.Frame(self.side_bar, bg=self.color, width=40, height=40, cursor="hand2", relief="raised")
        self.color_ind.pack(pady=15)
        self.color_ind.bind("<Button-1>", lambda e: self.choose_color())

        # SIZE SLIDER (ACUM PÂNĂ LA 150)
        tk.Label(self.side_bar, text="SIZE", fg="#555", bg="#0A0A0A", font=("Arial", 7, "bold")).pack()
        self.size_slider = tk.Scale(self.side_bar, from_=1, to=150, orient="vertical", 
                                   bg="#0A0A0A", fg="#00E5FF", highlightthickness=0, 
                                   troughcolor="#111", length=200, command=self.update_size)
        self.size_slider.set(8)
        self.size_slider.pack(pady=5)

        # --- CANVAS (GIGANT) ---
        self.canvas_container = tk.Frame(self.root, bg="#111", padx=2, pady=2)
        self.canvas_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_container, bg="white", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)

        # --- CHAT BAR ---
        self.chat_frame = tk.Frame(self.root, bg="#0A0A0A", height=100)
        self.chat_frame.pack(side="bottom", fill="x")
        
        self.chat_box = tk.Text(self.chat_frame, bg="#050505", fg="#00E5FF", font=("Segoe UI", 9), state="disabled", height=3)
        self.chat_box.pack(side="top", fill="x", padx=10, pady=2)
        
        self.msg_entry = tk.Entry(self.chat_frame, bg="#111", fg="white", borderwidth=0, insertbackground="#00E5FF")
        self.msg_entry.pack(side="bottom", fill="x", padx=10, pady=5, ipady=4)
        self.msg_entry.bind("<Return>", self.send_chat_msg)

    def update_size(self, val):
        self.size = int(val)

    def set_tool(self, name, sz):
        self.tool = name
        self.size_slider.set(sz)
        self.color_ind.config(bg="white" if name == "eraser" else self.color)

    def choose_color(self):
        c = colorchooser.askcolor()[1]
        if c: 
            self.color = c
            self.color_ind.config(bg=c)
            if self.tool == "eraser": self.tool = "brush"

    def show_menu(self):
        self.overlay = tk.Frame(self.root, bg="#050505")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        box = tk.Frame(self.overlay, bg="#0A0A0A", padx=40, pady=40)
        box.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(box, text="SELECT MODE", font=("Arial", 18, "bold"), fg="white", bg="#0A0A0A").pack(pady=10)
        tk.Button(box, text="HOST STUDIO", bg="#00E5FF", fg="black", font=("Arial", 10, "bold"), width=20, height=2, relief="flat", command=lambda: self.init_net("host")).pack(pady=5)
        tk.Button(box, text="JOIN STUDIO", bg="#222", fg="white", font=("Arial", 10, "bold"), width=20, height=2, relief="flat", command=lambda: self.init_net("client")).pack()

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
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, e):
        self.cw, self.ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.start_rx, self.start_ry = e.x/self.cw, e.y/self.ch
        self.last_rx, self.last_ry = self.start_rx, self.start_ry

    def on_move(self, e):
        rx, ry = e.x/self.cw, e.y/self.ch
        col = "white" if self.tool == "eraser" else self.color
        
        if self.tool in ["brush", "eraser"]:
            self.canvas.create_line(self.last_rx*self.cw, self.last_ry*self.ch, e.x, e.y, fill=col, width=self.size, capstyle="round", smooth=True)
            self.send_draw_data('line_draw', self.last_rx, self.last_ry, rx, ry, col, self.size)
            self.last_rx, self.last_ry = rx, ry
        else:
            # Preview pentru forme
            if self.temp_shape: self.canvas.delete(self.temp_shape)
            x1, y1 = self.start_rx * self.cw, self.start_ry * self.ch
            if self.tool == "line": self.temp_shape = self.canvas.create_line(x1, y1, e.x, e.y, fill=col, width=self.size)
            elif self.tool == "rect": self.temp_shape = self.canvas.create_rectangle(x1, y1, e.x, e.y, outline=col, width=self.size)
            elif self.tool == "oval": self.temp_shape = self.canvas.create_oval(x1, y1, e.x, e.y, outline=col, width=self.size)

    def on_release(self, e):
        if self.tool in ["line", "rect", "oval"]:
            rx, ry = e.x/self.cw, e.y/self.ch
            col = self.color
            self.send_draw_data(self.tool, self.start_rx, self.start_ry, rx, ry, col, self.size)
            self.temp_shape = None

    def send_draw_data(self, t, x1, y1, x2, y2, c, s):
        msg = json.dumps({'type': 'draw', 't': t, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'c': c, 's': s})
        if self.is_host: self.broadcast(msg, None)
        elif self.sock: self.sock.sendall((msg + "\n").encode())

    def draw_remote(self, m):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        x1, y1, x2, y2 = m['x1']*w, m['y1']*h, m['x2']*w, m['y2']*h
        if m['t'] in ['line_draw', 'line']: self.canvas.create_line(x1, y1, x2, y2, fill=m['c'], width=m['s'], capstyle="round", smooth=True)
        elif m['t'] == 'rect': self.canvas.create_rectangle(x1, y1, x2, y2, outline=m['c'], width=m['s'])
        elif m['t'] == 'oval': self.canvas.create_oval(x1, y1, x2, y2, outline=m['c'], width=m['s'])

    # --- NETWORKING (IDENTIC) ---
    def send_chat_msg(self, e=None):
        txt = self.msg_entry.get().strip()
        if txt:
            msg = json.dumps({'type': 'chat', 'user': self.my_name, 'text': txt})
            self.display_msg(f"{self.my_name}: {txt}")
            if self.is_host: self.broadcast(msg, None)
            elif self.sock: self.sock.sendall((msg + "\n").encode())
            self.msg_entry.delete(0, tk.END)

    def display_msg(self, text):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.config(state="disabled"); self.chat_box.see(tk.END)

    def run_server(self):
        try:
            subprocess.run(f"ngrok config add-authtoken {NGROK_TOKEN}", shell=True)
            subprocess.Popen(f"ngrok tcp {PORT}", shell=True, stdout=subprocess.DEVNULL)
            time.sleep(4)
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as res:
                url = json.loads(res.read().decode())['tunnels'][0]['public_url'].replace("tcp://", "")
                self.root.clipboard_clear(); self.root.clipboard_append(url)
                self.display_msg(f"System: Link copied to clipboard!")
        except: pass
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
                    line, buf = buf.split("\n", 1); msg = json.loads(line)
                    if msg.get('type') == 'chat': self.root.after(0, self.display_msg, f"{msg['user']}: {msg['text']}")
                    elif msg.get('type') == 'draw': self.root.after(0, self.draw_remote, msg)
                    elif msg.get('type') == 'clear': self.root.after(0, self.canvas.delete, "all")
                    self.broadcast(line, conn)
            except: break
        self.clients.remove(conn)

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
                    elif msg.get('type') == 'draw': self.root.after(0, self.draw_remote, msg)
                    elif msg.get('type') == 'clear': self.root.after(0, self.canvas.delete, "all")
        except: pass

    def broadcast(self, msg, skip):
        for c in self.clients:
            if c != skip:
                try: c.sendall((msg + "\n").encode())
                except: pass

    def clear_all(self):
        self.canvas.delete("all")
        msg = json.dumps({'type': 'clear'})
        if self.is_host: self.broadcast(msg, None)
        elif self.sock: self.sock.sendall((msg + "\n").encode())

if __name__ == "__main__":
    ObsidianEliteMaxShapes().root.mainloop()
