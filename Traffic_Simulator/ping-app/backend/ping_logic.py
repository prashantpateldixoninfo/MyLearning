import subprocess
import platform

def run_ping(host, count=4):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, str(count), host], text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {e}"
