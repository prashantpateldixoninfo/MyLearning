import os
import sys
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill
from copy import copy

# Column mapping between Original and Modified sheets
COLUMN_MAP = {
    "S.No.": "S. No.",
    "Process": "Process Step / Function",
    "Potential Failure Mode": "Potential Failure Mode",
    "Potential Effect(s) of Failure": "Potential Effect(s) of Failure",
    "Sev. (S)": "Severity (S)",
    "Potential Causes(s) mechanism(s) of the Failure": "Potential Cause(s) / Mechanism of Failure",
    "Occ. (O)": "Occurrence (O)",
    "Prevention": "Prevention",
    "Detection": "Detection",
    "Det. (O)": "Detection (D)",
    "RPN (S X O X D)": "RPN (S×O×D)",
    "Recommended Action(s)": "Recommended Actions",
    "Responsibility & target  Completion Date": "Responsibility",
    "Action(s) Taken": "Action Taken",
    "Sev.": "New S",
    "Occ.": "New O",
    "Det.": "New D",
    "RPN": "New RPN",
}

SHEET_NAMES = ["Stores & IQC", "SMT", "MI", "BLT & FAT", "PACKING"]


def copy_row_formatting(source_row, target_row):
    for source_cell, target_cell in zip(source_row, target_row):
        target_cell.value = source_cell.value
        if source_cell.has_style:
            target_cell.font = copy(source_cell.font)
            target_cell.fill = copy(source_cell.fill)
            target_cell.border = copy(source_cell.border)
            target_cell.alignment = copy(source_cell.alignment)
            target_cell.number_format = source_cell.number_format


def transform_excel(original_file, modified_file):
    wb_original = load_workbook(original_file)
    wb_modified = Workbook()
    wb_modified.remove(wb_modified.active)

    if "PFMEA-Format" not in wb_original.sheetnames:
        print("[ERROR] 'PFMEA-Format' sheet is missing in original file")
        sys.exit(1)

    template_ws = wb_original["PFMEA-Format"]

    for sheet_name in wb_original.sheetnames:
        original_ws = wb_original[sheet_name]
        if sheet_name.strip() in SHEET_NAMES:
            new_ws = wb_modified.create_sheet(title=sheet_name.strip())

            # Copy rows 1-7 from PFMEA-Format
            for row_idx in range(1, 8):
                source_row = template_ws[row_idx]
                target_row = new_ws[row_idx]
                copy_row_formatting(source_row, target_row)

            # Find header row (assumed to start from row 8 in original)
            header_row = [cell.value for cell in original_ws[8]]

            # Get index and names of columns to map
            selected_columns = [(i, COLUMN_MAP[col]) for i, col in enumerate(header_row) if col in COLUMN_MAP]

            if not selected_columns:
                print(f"[SKIP] No mapped columns in sheet '{sheet_name}'")
                continue

            # Write headers at row 8
            for col_idx, (_, new_col_name) in enumerate(selected_columns, start=1):
                cell = new_ws.cell(row=8, column=col_idx, value=new_col_name)

            # Write data starting from row 9
            for row_idx, row in enumerate(original_ws.iter_rows(min_row=9, values_only=True), start=9):
                for col_idx, (original_index, _) in enumerate(selected_columns, start=1):
                    new_ws.cell(row=row_idx, column=col_idx, value=row[original_index])
        else:
            # Copy sheet as-is
            new_ws = wb_modified.create_sheet(title=sheet_name.strip())
            for row in original_ws.iter_rows():
                new_ws.append([cell.value for cell in row])

    wb_modified.save(modified_file)
    print(f"[OK] Output saved as: {modified_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python excel_transformer.py <original.xlsx> <modified.xlsx>")
        sys.exit(1)

    orig_file = sys.argv[1]
    mod_file = sys.argv[2]

    if not os.path.isfile(orig_file):
        print(f"[ERROR] File not found: {orig_file}")
        sys.exit(1)

    transform_excel(orig_file, mod_file)
