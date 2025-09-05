Perfect 👍 Here’s a clean **README.md** you can use for your Tkinter-based Excel Validation Tool:

---

# 📊 Excel Production Data Validation Tool

A Python **Tkinter GUI application** to validate Excel production data against predefined rules.
Originally built for Google Colab, now converted into a **desktop-friendly app** that runs directly in Visual Studio Code (or any Python environment).

---

## 🚀 Features

* ✅ Load Excel files (`.xlsx`, `.xls`) directly from your computer
* ✅ Select a sheet from the workbook
* ✅ View and edit validation rules in an interactive **table**
* ✅ Validate columns against multiple rule types:

  * **Duplicate** – all values must match a default
  * **Uniqueness** – all values must be unique
  * **Unique-IncrementSN** – serial numbers must increment correctly
  * **Unique-IncrementMAC** – MAC addresses must increment correctly
* ✅ Export validation results to a new Excel file with timestamp
* ✅ Simple GUI with buttons and dropdowns (no coding required for users)

---

## 📂 Project Structure

```
Production_Data_Validation/
│
├── Production_Data_Validation_FWA.py   # Main Tkinter app
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```

---

## 🔧 Installation

1. **Clone or download** this repository
2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. Run the app:

   ```bash
   python Production_Data_Validation_FWA.py
   ```
2. In the GUI:

   * Click **“📂 Upload Excel File”** → Select your `.xlsx` file
   * Choose a **sheet** from the dropdown
   * Click **“📋 Show Menu Table”** to review/edit rules
   * Click **“✅ Run Validation”** to generate results
3. Validation results are saved as:

   ```
   <OriginalFileName>_Validation_Result_YY_MM_DD.xlsx
   ```

---

## 📝 Example Validation Rules

| Validation Name | Default Value | Function            |
| --------------- | ------------- | ------------------- |
| SerialNumber    | ANK0DA2F0020  | Unique-IncrementSN  |
| MAC             | 609849A1021   | Unique-IncrementMAC |
| UserName        | admin         | Duplicate           |
| IMEI            | 351185560000  | Uniqueness          |

---

## 📦 Packaging (Optional)

If you want to share the tool as a **standalone EXE** (no Python needed):

```bash
pip install pyinstaller
pyinstaller --onefile Production_Data_Validation_FWA.py.py
```

The executable will appear in the `dist/` folder.

---

## ✅ Requirements

* Python 3.9+
* pandas
* openpyxl
* (Tkinter is included with Python)

---

## 📌 License

MIT License – free to use, modify, and distribute.

---
