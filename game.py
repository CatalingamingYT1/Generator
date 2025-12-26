import tkfrom tkinter import simpledialog, messagebox, colorchooser
import socket, threading, json, time, subprocess, urllib.request

# CONFIGURARE
NGROK_TOKEN = "2djWLmNtLhALFfZ74L1K1mcXSV7_3uJhFnqkWjh2UgeDuZzuS"
PORT = 12345

class ObsidianEliteMax:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Obsidian Elite MAX - Massive Canvas Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg="#050505")

        self.sock = None
        self.clients = []
        self.color = "#1A1A1B"
        self.tool = "brush"
        self.size = 6
        self.is_host = False
        self.my_name = "User"

        self.setup_ui()
        self.show_menu()

    def setup_ui(self):
        # --- TOP BAR (Logo & Players) ---
        self.top_bar = tk.Frame(self.root, bg="#0A0A0A", height=50)
        self.top_bar.pack(side="top", fill="x")
        
        self.logo_label = tk.Label(self.top_bar, text="♦ OBSIDIAN ELITE MAX", fg="#00E5FF", 
                                  bg="#0A0A0A", font=("Impact", 20))
        self.logo_label.pack(side="left", padx=20)

        self.player_count_lbl = tk.Label(self.top_bar, text="PLAYERS: 1", fg="#00E5FF", 
                                        bg="#0A0A0A", font=("Consolas", 10, "bold"))
        self.player_count_lbl.pack(side="right", padx=20)

        # --- MAIN LAYOUT ---
        # Sidebar stânga (Foarte îngust pentru a lăsa loc la Canvas)
        self.side_bar = tk.Frame(self.root, bg="#0A0A0A", width=60)
        self.side_bar.pack(side="left", fill="y")
        
        for icon, name, sz in [("✏️", "pencil", 2), ("🖌️", "brush", 8), ("🧽", "eraser", 40), ("🗑️", "clear", 0)]:
            cmd = self.clear_all if name == "clear" else lambda n=name, s=sz: self.set_tool(n, s)
            btn = tk.Button(self.side_bar, text=icon, font=("Arial", 16), bg="#0A0A0A", fg="white",
                           relief="flat", activebackground="#222", command=cmd)
            btn.pack(pady=15, fill="x")

        self.color_ind = tk.Frame(self.side_bar, bg=self.color, width=35, height=35, cursor="hand2")
        self.color_ind.pack(pady=10)
        self.color_ind.bind("<Button-1>", lambda e: self.choose_color())

        # Containerul de Canvas (GIGANT)
        self.canvas_container = tk.Frame(self.root, bg="#111", padx=2, pady=2)
        self.canvas_container.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_container, bg="white", highlightthickness=0, cursor="arrow")
        self.canvas.pack(fill="both", expand=True)

        # Chat-ul la bază (Ocupă puțin loc pe verticală)
        self.chat_frame = tk.Frame(self.root, bg="#0A0A0A", height=120)
        self.chat_frame.pack(side="bottom", fill="x")
        
        self.chat_box = tk.Text(self.chat_frame, bg="#050505", fg="#00E5FF", font=("Segoe UI", 9), 
                               state="disabled", height=4, borderwidth=0, highlightthickness=0)
        self.chat_box.pack(side="top", fill="x", padx=10, pady=2)
        
        self.msg_entry = tk.Entry(self.chat_frame, bg="#111", fg="white", borderwidth=0, insertbackground="white")
        self.msg_entry.pack(side="bottom", fill="x", padx=10, pady=5, ipady=5)
        self.msg_entry.bind("<Return>", self.send_chat_msg)

    def set_tool(self, name, sz):
        self.tool = name
        self.size = sz
        self.color_ind.config(bg="white" if name == "eraser" else self.color)

    def choose_color(self):
        c = colorchooser.askcolor()[1]
        if c: 
            self.color = c
            self.set_tool("brush", 8)
            self.color_ind.config(bg=c)

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
                    line, buf = buf.split("\n", 1)
                    msg = json.loads(line)
                    if msg.get('type') == 'chat': self.root.after(0, self.display_msg, f"{msg['user']}: {msg['text']}")
                    elif msg.get('type') == 'clear': self.root.after(0, self.canvas.delete, "all")
                    else: self.root.after(0, self.draw_remote, msg)
                    self.broadcast(line, conn)
            except: break
        self.clients.remove(conn)

    def run_client(self, addr):
        try:
            h, p = addr.split(":"); self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((h, int(p)))
            self.display_msg("System: Connected to Elite Studio!")
            buf = ""
            while True:
                data = self.sock.recv(4096).decode()
                if not data: break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    msg = json.loads(line)
                    if msg.get('type') == 'chat': self.root.after(0, self.display_msg, f"{msg['user']}: {msg['text']}")
                    elif msg.get('type') == 'clear': self.root.after(0, self.canvas.delete, "all")
                    else: self.root.after(0, self.draw_remote, msg)
        except: pass

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
    ObsidianEliteMax().root.mainloop()
