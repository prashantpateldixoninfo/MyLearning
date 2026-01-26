
---

```markdown
# Wifi Log Excel Combiner

This Python script parses `.dat` log files inside subdirectories (where each folder is named after a serial number), extracts test parameters and values, and generates:

1. An individual Excel result file (`<SerialNumber>_Test_Result.xlsx`) in each subfolder.
2. A combined **Master Excel** file (`Master_Test_Result.xlsx`) in the parent folder, summarizing all results.

---

## 📁 Folder Structure Example

```

Wifiports3/
├── NKOTEF000024/
│   ├── log1.dat
│   └── log2.dat
├── NKOTEF000030/
│   ├── log1.dat
│   └── log2.dat
└── ...

````

---

## ✅ Features

- Extracts Serial Number from lines like `UADCSTART|`
- Extracts test parameters and their values from `PRODUCTSTEP|TestItem|`
- Extracts Min/Max values from last log file for each parameter
- Computes average value per parameter
- Generates individual Excel sheets per serial
- Creates a **Master Excel** combining all data

---

## 🔧 Installation

1. Make sure you have **Python 3.6+** installed.

2. Install dependencies:

```bash
pip install openpyxl
````

---

## 🚀 How to Run

Navigate to your project directory and run:

```bash
python regex_all_folders.py "Wifiports3"
```

Or if the folder has space or is nested:

```bash
python regex_all_folders.py ".\Wifiports3"
```

✅ This will:

* Traverse all subdirectories under `Wifiports3`
* Parse `.dat` files
* Generate:

  * `NKOTEF000024_Test_Result.xlsx`, `NKOTEF000030_Test_Result.xlsx`, etc.
  * `Master_Test_Result.xlsx` (in `Wifiports3/`)

---

## 📊 Excel Output Format

### Individual Serial Sheet (e.g., `NKOTEF000024_Test_Result.xlsx`)

| Test Item                        | log1.dat | log2.dat | ... | Average | Min  | Max  |
| -------------------------------- | -------- | -------- | --- | ------- | ---- | ---- |
| MTK7916D\_11ag\_54M\_Group0\_... | 22.91    | 23.04    |     | 22.98   | 18.0 | 28.0 |
| ...                              | ...      | ...      |     | ...     | ...  | ...  |

### Master Sheet (`Master_Test_Result.xlsx`)

| Test Item                        | NKOTEF000024 | NKOTEF000030 | ... | Min  | Max  |
| -------------------------------- | ------------ | ------------ | --- | ---- | ---- |
| MTK7916D\_11ag\_54M\_Group0\_... | 22.98        | 23.21        |     | 18.0 | 28.0 |
| ...                              | ...          | ...          |     | ...  | ...  |

---
