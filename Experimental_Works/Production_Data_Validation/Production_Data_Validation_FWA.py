import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# =========================
# Config
# =========================
ENABLE_LOGS = True

# =========================
# Helpers
# =========================
def log(msg, level="DEBUG"):
    if ENABLE_LOGS:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [{level}] {msg}")

# =========================
# Validation Logic
# =========================
function_options = ["Duplicate", "Uniqueness", "Unique-IncrementSN", "Unique-IncrementMAC"]

def validate_column(col, func, default_val):
    log(f"Validating {col.name} with {func}, default={default_val}")
    if func == "Duplicate":
        return all(col.fillna("").astype(str) == str(default_val))
    elif func == "Uniqueness":
        return col.is_unique
    elif func == "Unique-IncrementSN":
        try:
            nums = col.dropna().astype(str).str.extract(r'(\d+)$')[0].astype(int)
            return nums.is_monotonic_increasing
        except Exception as e:
            log(f"SN validation failed: {e}", "ERROR")
            return False
    elif func == "Unique-IncrementMAC":
        try:
            nums = col.dropna().astype(str).apply(lambda x: int(x.replace(":", "").replace("-", ""), 16))
            return nums.is_monotonic_increasing
        except Exception as e:
            log(f"MAC validation failed: {e}", "ERROR")
            return False
    return False

# =========================
# Static Menu Template
# =========================
menu_df_template = pd.DataFrame([
    ["Mnemonic", "5G32-A", "Duplicate"],
    ["PN", "3TG03358AAAA", "Duplicate"],
    ["SerialNumber", "ANK0DA2F00200001", "Unique-IncrementSN"],
    ["MAC", "609849A1021", "Unique-IncrementMAC"],
    ["IP_address", "192.168.0.1", "Duplicate"],
    ["UserName", "admin", "Duplicate"],
    ["OperatorID", "BATL", "Duplicate"],
    ["CountryID", "eu", "Duplicate"],
    ["MfrID", "ANK", "Duplicate"],
    ["HardwareVersion", "3TG03366AAAA", "Duplicate"],
    ["PartNumber", "3TG03350AAAC", "Duplicate"],
    ["ImageVersion", "5G-ODCPE-BHARTI_R240200BieT0401E0780", "Duplicate"],
    ["WEB_Hardware", "3TG03366AAAA", "Duplicate"],
    ["WEB_Software", "AOD311NK_R_1.0", "Duplicate"],
    ["Test_Software", "5G-ODCPE-BHARTI_D240400B31T0401E0460", "Duplicate"],
    ["Factorycode", "36", "Duplicate"],
    ["IMEI", "35118556000052", "Uniqueness"],
    ["BlueTooth_PIN", "129454", "Uniqueness"],
    ["IMEI2", "35118556000060", "Uniqueness"],
], columns=["Validation Name", "Default Value", "Function"])

# =========================
# GUI App
# =========================
class ValidationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Validation Tool")
        self.file_path = None
        self.sheet_name = None
        self.data_df = None
        self.menu_df = menu_df_template.copy()
        self.results_df = None

        # UI Layout
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Buttons
        self.btn_open = tk.Button(frame, text="📂 Open Excel File", command=self.open_file)
        self.btn_open.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.sheet_var = tk.StringVar()
        self.sheet_dropdown = ttk.Combobox(frame, textvariable=self.sheet_var, state="readonly")
        self.sheet_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.btn_show_menu = tk.Button(frame, text="📋 Show Menu Table", command=self.show_menu, state="disabled")
        self.btn_show_menu.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.btn_validate = tk.Button(frame, text="✅ Run Validation", command=self.run_validation, state="disabled")
        self.btn_validate.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.btn_save = tk.Button(frame, text="💾 Save Results", command=self.save_results, state="disabled")
        self.btn_save.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Menu Table with Validation Name
        self.menu_tree = ttk.Treeview(frame, columns=("Name", "Default", "Function"), show="headings", height=10)
        self.menu_tree.heading("Name", text="Validation Name")
        self.menu_tree.heading("Default", text="Default Value")
        self.menu_tree.heading("Function", text="Function")
        self.menu_tree.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=10)

        # Results Table with Validation Name
        self.result_tree = ttk.Treeview(frame, columns=("Name", "Default", "Function", "Result"), show="headings", height=10)
        self.result_tree.heading("Name", text="Validation Name")
        self.result_tree.heading("Default", text="Default Value")
        self.result_tree.heading("Function", text="Function")
        self.result_tree.heading("Result", text="Result")
        self.result_tree.grid(row=2, column=0, columnspan=5, sticky="nsew", pady=10)

        # Resize
        for i in range(5):
            frame.grid_columnconfigure(i, weight=1)

    def open_file(self):
        filetypes = [("Excel Files", "*.xlsx *.xls")]
        self.file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=filetypes)
        if not self.file_path:
            return

        try:
            xls = pd.ExcelFile(self.file_path)
            self.sheet_dropdown["values"] = xls.sheet_names
            self.sheet_dropdown.current(0)
            self.sheet_name = xls.sheet_names[0]
            self.btn_show_menu["state"] = "normal"
            messagebox.showinfo("File Loaded", f"Loaded {os.path.basename(self.file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def show_menu(self):
        try:
            self.sheet_name = self.sheet_var.get()
            self.data_df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

            # Fill defaults from data
            self.menu_df = menu_df_template.copy()
            for col in self.menu_df["Validation Name"]:
                if col in self.data_df.columns and len(self.data_df) > 1:
                    val = self.data_df[col].iloc[1]
                    if pd.notna(val):
                        self.menu_df.loc[self.menu_df["Validation Name"] == col, "Default Value"] = str(val)

            # Populate menu table
            for row in self.menu_tree.get_children():
                self.menu_tree.delete(row)
            for _, row in self.menu_df.iterrows():
                self.menu_tree.insert("", "end", values=(row["Validation Name"], row["Default Value"], row["Function"]))

            self.btn_validate["state"] = "normal"
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sheet: {e}")

    def run_validation(self):
        if self.data_df is None:
            messagebox.showerror("Error", "No sheet loaded.")
            return

        results = []
        for _, row in self.menu_df.iterrows():
            val_name = row["Validation Name"]
            default_val = row["Default Value"]
            func = row["Function"]

            if val_name in self.data_df.columns:
                col = self.data_df[val_name]
                status = validate_column(col, func, default_val)
                results.append([val_name, default_val, func, "✅ Pass" if status else "❌ Fail"])
            else:
                results.append([val_name, default_val, "Column Missing", "❌ Fail"])

        self.results_df = pd.DataFrame(results, columns=["Validation Name", "Default Value", "Function", "Result"])

        # Populate results table
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)
        for _, row in self.results_df.iterrows():
            self.result_tree.insert("", "end", values=(row["Validation Name"], row["Default Value"], row["Function"], row["Result"]))

        self.btn_save["state"] = "normal"

    def save_results(self):
        if self.results_df is None:
            messagebox.showerror("Error", "No results to save.")
            return

        today = datetime.today().strftime("%y_%m_%d")
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        out_name = f"{base_name}_Validation_Result_{today}.xlsx"
        self.results_df.to_excel(out_name, index=False)
        messagebox.showinfo("Saved", f"Results saved as {out_name}")


# =========================
# Main
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = ValidationApp(root)
    root.mainloop()
