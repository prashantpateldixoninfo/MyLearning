import telnetlib
import threading
import time

# Telnet session management
telnet_sessions = {}
session_timeout = 300  # 5-minute timeout


def cleanup_idle_sessions():
    """Remove idle Telnet sessions"""
    while True:
        current_time = time.time()
        for ip, (tn, last_active) in list(telnet_sessions.items()):
            if current_time - last_active > session_timeout:
                print(f"Closing idle session for {ip}")
                tn.close()
                del telnet_sessions[ip]
        time.sleep(10)


# Start cleanup thread
threading.Thread(target=cleanup_idle_sessions, daemon=True).start()


def connect_to_olt(ip: str, username: str, password: str):
    """Establish or reuse a Telnet connection"""
    try:
        if ip in telnet_sessions:
            telnet_sessions[ip] = (
                telnet_sessions[ip][0],
                time.time(),
            )  # Refresh session
            return telnet_sessions[ip][0], "Reusing existing session!"

        tn = telnetlib.Telnet(ip, timeout=5)
        tn.read_until(b"Username:", timeout=3)
        tn.write(username.encode("ascii") + b"\n")

        tn.read_until(b"Password:", timeout=3)
        tn.write(password.encode("ascii") + b"\n")

        response = tn.read_until(b">", timeout=5).decode("ascii")

        if "incorrect" in response.lower():
            tn.close()
            return None, "Invalid credentials."

        telnet_sessions[ip] = (tn, time.time())  # Store session with timestamp
        return tn, "Connected to OLT successfully!"

    except Exception as e:
        return None, f"Telnet connection failed: {str(e)}"


def close_telnet_session(ip: str):
    """Close a Telnet session"""
    tn_data = telnet_sessions.pop(ip, None)
    if tn_data:
        tn_data[0].close()
        return True
    return False
