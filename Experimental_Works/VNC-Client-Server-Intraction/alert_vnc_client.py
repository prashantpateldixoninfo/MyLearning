import socket
import threading
import tkinter as tk
import platform
import datetime

DEBUG = True
SERVER_PORT = 5000
SERVER_IP = "192.168.0.113"   # 🔴 CHANGE TO SERVER PC IP

overlay = None

def debug(msg):
    if DEBUG:
        print("[CLIENT DEBUG]", msg)

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

CLIENT_IP = get_local_ip()

def show_overlay():
    global overlay
    debug("Showing popup alert")

    overlay = tk.Toplevel(root)
    overlay.title("⚠ Client HELP REQUIRED")
    overlay.geometry("400x200")
    overlay.attributes("-topmost", True)
    overlay.configure(bg="red")

    tk.Label(
        overlay,
        text="Client HELP REQUIRED\nSupervisor Notified",
        fg="white",
        bg="red",
        font=("Arial", 20, "bold"),
        justify="center"
    ).pack(expand=True, pady=20)

    tk.Button(
        overlay,
        text="ACKNOWLEDGE",
        font=("Arial", 12, "bold"),
        command=close_overlay
    ).pack(pady=10)
    # overlay.after(10000, close_overlay)  # auto close in 10 sec

def close_overlay():
    global overlay
    if overlay:
        overlay.destroy()
        overlay = None


def send_socket(full_msg):
    debug(f"Connecting to {SERVER_IP}:{SERVER_PORT}")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((SERVER_IP, SERVER_PORT))
        debug("Connected")

        s.sendall(full_msg.encode())
        debug("Message sent")

        s.close()
        status.set("✅ Alert sent")
        show_overlay()

    except Exception as e:
        debug(f"Socket error: {e}")
        status.set(f"❌ {e}")

def send_alert():
    msg = text_box.get("1.0", tk.END).strip()
    if not msg:
        status.set("⚠ Enter message")
        return

    client = platform.node()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    full_msg = (
        f"CLIENT NAME: {client}\n"
        f"CLIENT IP  : {CLIENT_IP}\n"
        f"TIME       : {timestamp}\n"
        f"ISSUE      : {msg}"
    )

    debug("Preparing to send alert")
    threading.Thread(target=send_socket, args=(full_msg,), daemon=True).start()

# GUI
root = tk.Tk()
root.title("Client Alert Panel")
root.geometry("450x320")

tk.Label(root, text="Enter Alert Message", font=("Arial", 10, "bold")).pack(pady=5)

text_box = tk.Text(root, height=6, width=50)
text_box.pack()

tk.Button(root, text="SEND ALERT", bg="red", fg="white",
          font=("Arial", 11, "bold"), command=send_alert).pack(pady=10)

tk.Button(root, text="CLEAR ALERT", command=close_overlay).pack()

status = tk.StringVar()
tk.Label(root, text=f"Client IP: {CLIENT_IP}").pack()
tk.Label(root, textvariable=status).pack(pady=5)

root.mainloop()
