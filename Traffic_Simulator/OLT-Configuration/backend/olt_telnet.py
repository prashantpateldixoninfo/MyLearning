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

        if "invalid" in response.lower():
            tn.close()
            return None, f"Telnet connection failed for IP {ip} | Reason: Username or password invalid."

        telnet_sessions[ip] = (tn, time.time())  # Store session with timestamp
        return tn, f"Connected to OLT {ip}"

    except Exception as e:
        return None, f"Telnet connection failed for IP {ip} | Reason: {str(e)}"

def close_telnet_session(ip: str):
    """Close a Telnet session"""
    print(f"Closing session for {ip}")
    tn_data = telnet_sessions.pop(ip, None)
    if tn_data:
        tn_data[0].close()
        return True
    return False

def check_telnet_status(ip: str):
    """Check if a Telnet session is active for a given IP."""
    if ip in telnet_sessions:
        return {"status": "Active", "message": f"Session is active for"}
    return {"status": "Inactive", "message": f"No active session found for"}
