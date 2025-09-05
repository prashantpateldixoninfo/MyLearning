import os
import re
import pandas as pd

# ==== CONFIG ====
INPUT_FILE = r"Test_Data_With_Pivot_Table.xlsx"       # <-- change if needed
OUTPUT_FILE = r"stage_error_summary.xlsx"

# ==== HELPERS ====
def safe_sheet_name(name: str) -> str:
    # Excel sheet name <=31 chars; remove invalid chars
    name = re.sub(r'[:\\/?*\[\]]', '_', str(name))
    return name[:31] if len(name) > 31 else name

def pick_columns(df, sheet_name):
    """
    Return (stage_col, err_col) preferring exact column names.
    If 'Error Description' missing, try to find a reasonable fallback.
    """
    cols = list(df.columns)

    # Prefer exact names
    stage_col = "Stage" if "Stage" in cols else None
    err_col   = "Error Description" if "Error Description" in cols else None

    # Fallbacks (only if not found) — with warnings so you know what's used
    if stage_col is None:
        # try case-insensitive exact match first
        for c in cols:
            if c.strip().lower() == "stage":
                stage_col = c
                print(f"⚠️  Using '{c}' as Stage (from sheet '{sheet_name}')")
                break
        # try contains 'stage'
        if stage_col is None:
            for c in cols:
                if "stage" in c.strip().lower():
                    stage_col = c
                    print(f"⚠️  Using '{c}' as Stage (from sheet '{sheet_name}')")
                    break

    if err_col is None:
        # try case-insensitive exact match first
        for c in cols:
            if c.strip().lower() == "error description":
                err_col = c
                print(f"⚠️  Using '{c}' as Error Description (from sheet '{sheet_name}')")
                break
        # common pivot export header fallback
        if err_col is None and "Row Labels" in cols:
            err_col = "Row Labels"
            print(f"⚠️  'Error Description' not found on '{sheet_name}'. Using 'Row Labels' instead.")
        # last resort: any column that contains 'error'
        if err_col is None:
            for c in cols:
                if "error" in c.strip().lower():
                    err_col = c
                    print(f"⚠️  'Error Description' not found on '{sheet_name}'. Using '{c}' instead.")
                    break

    return stage_col, err_col

# ==== READ ALL SHEETS ====
xls = pd.ExcelFile(INPUT_FILE)
frames = []
for s in xls.sheet_names:
    df = pd.read_excel(INPUT_FILE, sheet_name=s)
    # Trim header whitespace
    df.columns = df.columns.str.strip()

    stage_col, err_col = pick_columns(df, s)
    if stage_col is None or err_col is None:
        print(f"❌ Skipping sheet '{s}' — required columns not found. Columns present: {list(df.columns)}")
        continue

    # Keep only the two needed columns
    slim = df[[stage_col, err_col]].copy()
    slim.columns = ["Stage", "Error Description"]  # normalize names
    # Drop rows with missing values in either column
    slim = slim.dropna(subset=["Stage", "Error Description"])
    frames.append(slim)

if not frames:
    raise ValueError("No valid sheets with both 'Stage' and 'Error Description' found.")

all_data = pd.concat(frames, ignore_index=True)

# ==== BUILD OVERALL SUMMARY (like a pivot) ====
summary_all = (
    all_data.groupby(["Stage", "Error Description"])
            .size()
            .reset_index(name="Count")
            .sort_values(["Stage", "Count"], ascending=[True, False])
)

# ==== WRITE OUTPUT WITH CHARTS (xlsxwriter) ====
with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
    wb = writer.book

    # ALL_SUMMARY sheet
    summary_all.to_excel(writer, sheet_name="ALL_SUMMARY", index=False)

    # One sheet per Stage (Top 3)
    for stage in summary_all["Stage"].dropna().unique():
        stage_table = summary_all[summary_all["Stage"] == stage].copy()
        stage_table = stage_table.sort_values("Count", ascending=False)

        # Top 3 rows (or fewer if <3 exist)
        top3 = stage_table.head(3)[["Error Description", "Count"]].reset_index(drop=True)

        sheet_name = safe_sheet_name(stage)
        top3.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0, startcol=0)
        ws = writer.sheets[sheet_name]

        # Build Pie Chart
        # Data range: A1:B{rows}, with headers on row 1
        rows = len(top3) + 1  # including header row
        chart = wb.add_chart({"type": "pie"})
        # categories = Error Description (A2:A{rows})
        chart.add_series({
            "name":       f"Top 3 Errors - {stage}",
            "categories": [sheet_name, 1, 0, rows-1, 0],  # (sheet, first_row, first_col, last_row, last_col)
            "values":     [sheet_name, 1, 1, rows-1, 1],  # counts in column B
            "data_labels": {"percentage": True, "value": True}
        })
        chart.set_title({"name": f"Top 3 Errors - {stage}"})
        chart.set_style(10)

        # Place chart
        ws.insert_chart("E2", chart)

print(f"✅ Wrote '{OUTPUT_FILE}' with one sheet per Stage (Top 3 + Pie chart).")
print("   Also wrote 'ALL_SUMMARY' with full counts.")
