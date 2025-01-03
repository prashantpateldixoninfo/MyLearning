import tkinter as tk
import requests
from shared.config import BACKEND_URL


def fetch_data():
    try:
        response = requests.get(f"{BACKEND_URL}/api/data")
        response.raise_for_status()
        label.config(text=response.json().get("key"))
    except requests.exceptions.RequestException as e:
        label.config(text=f"Error: {e}")


root = tk.Tk()
root.title("GUI with Backend")

label = tk.Label(root, text="Data will appear here")
label.pack()

button = tk.Button(root, text="Fetch Data", command=fetch_data)
button.pack()

root.mainloop()
