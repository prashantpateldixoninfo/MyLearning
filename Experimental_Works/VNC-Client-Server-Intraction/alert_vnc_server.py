import socket
import threading
import tkinter as tk
import winsound
import datetime

DEBUG = True
SERVER_PORT = 5000
LOG_FILE = "alert_history.log"

def debug(msg):
    if DEBUG:
        print("[SERVER DEBUG]", msg)

# Get local IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    s.close()
    return ip

SERVER_IP = get_local_ip()

def log_event(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {msg}\n")

def show_alert_popup(message):
    debug("Showing SINGLE popup alert")

    popup = tk.Toplevel(root)
    popup.title("🚨 CLIENT ALERT")
    popup.geometry("500x300")
    popup.configure(bg="red")
    popup.attributes("-topmost", True)

    # Big Title
    tk.Label(
        popup,
        text="Server HELP REQUIRED",
        bg="red",
        fg="white",
        font=("Arial", 24, "bold")
    ).pack(pady=10)

    # Alert Details
    tk.Label(
        popup,
        text=message,
        bg="red",
        fg="white",
        font=("Arial", 12),
        justify="left",
        wraplength=460
    ).pack(padx=10, pady=10)

    # ACK Button
    tk.Button(
        popup,
        text="ACKNOWLEDGE",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="red",
        width=15,
        command=popup.destroy
    ).pack(pady=10)

    winsound.Beep(1500, 1000)

    # 🔴 FLASH FUNCTION (MUST BE INSIDE)
    def flash():
        current = popup.cget("bg")
        new_color = "darkred" if current == "red" else "red"
        popup.configure(bg=new_color)

        # Also update labels background
        for widget in popup.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=new_color)

        popup.after(500, flash)   # flash every 0.5 sec

    # ✅ START FLASHING
    flash()


def handle_client(conn, addr):
    debug(f"Connection from {addr}")

    try:
        data = conn.recv(4096).decode()
        debug(f"Received: {data}")

        if data:
            log_event(data.replace("\n", " | "))
            root.after(0, show_alert_popup, f"FROM: {addr[0]}\n\n{data}")
    except Exception as e:
        debug(f"ERROR handle_client: {e}")

    conn.close()
    debug("Connection closed")

def start_server():
    debug("Starting server socket...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", SERVER_PORT))
    server.listen(50)

    debug(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        debug("Client accepted")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# GUI
root = tk.Tk()
root.title("Alert Server (Master PC)")
root.geometry("400x180")

tk.Label(root, text="🟢 Alert Server Running", font=("Arial", 12, "bold")).pack(pady=10)
tk.Label(root, text=f"Server IP: {SERVER_IP}").pack()
tk.Label(root, text=f"Port: {SERVER_PORT}").pack()

threading.Thread(target=start_server, daemon=True).start()
root.mainloop()
