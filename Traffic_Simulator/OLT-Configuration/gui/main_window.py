import tkinter as tk
from tkinter import messagebox
import requests
from shared.config import BACKEND_URL


def send_data():
    user_input = input_field.get()
    if not user_input.strip():
        messagebox.showerror("Error", "Input cannot be empty!")
        return

    try:
        response = requests.post(f"{BACKEND_URL}/submit", json={"input": user_input})
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Data sent successfully! {response.json()}")
        else:
            messagebox.showerror(
                "Error", f"Failed to send data: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def fetch_data():
    try:
        response = requests.get(f"{BACKEND_URL}/get_data")
        if response.status_code == 200:
            data = response.json().get("data")
            messagebox.showinfo("Fetched Data", f"Data from backend: {data}")
        else:
            messagebox.showerror("Error", "No data available on backend.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main window
root = tk.Tk()
root.title("Huawei OLT Configuration")

# Input field
input_label = tk.Label(root, text="Enter your data:")
input_label.pack(pady=5)

input_field = tk.Entry(root, width=40)
input_field.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=send_data)
submit_button.pack(pady=10)

label = tk.Label(root, text="Data from Huawei OLT will be displayed here")
label.pack()

button = tk.Button(root, text="Fetch Data", command=fetch_data)
button.pack()

# Run the GUI
root.mainloop()
