import subprocess

def run_ping(host):
    try:
        return subprocess.check_output(["ping", "-c", "4", host], text=True)
    except subprocess.CalledProcessError as e:
        return e.output
