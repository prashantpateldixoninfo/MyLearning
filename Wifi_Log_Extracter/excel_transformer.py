import os
import sys
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter, range_boundaries
from openpyxl.styles import Font
from copy import copy

# Input to Output column index mapping (0-based)
COLUMN_INDEX_MAP = {
    0: 0,   # A -> A
    1: 1,   # B -> B
    3: 2,   # D -> C
    4: 3,   # E -> D
    5: 4,   # F -> E
    7: 5,   # H -> F
    8: 6,   # I -> G
    9: 7,   # J -> H
    10: 8,  # K -> I
    12: 9,  # M -> J
    13: 10, # N -> K
    14: 16, # O -> Q
    15: 11, # P -> L
    16: 12, # Q -> M
    17: 13, # R -> N
    18: 14, # S -> O
    19: 15, # T -> P
}

SHEET_NAMES = ["Stores & IQC", "SMT", "MI", "BLT & FAT", "PACKING"]

def copy_range_formatting(src_ws, tgt_ws, cell_range):
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            src_cell = src_ws.cell(row=row, column=col)
            tgt_cell = tgt_ws.cell(row=row, column=col, value=src_cell.value)
            if src_cell.has_style:
                tgt_cell.font = copy(src_cell.font)
                tgt_cell.fill = copy(src_cell.fill)
                tgt_cell.border = copy(src_cell.border)
                tgt_cell.alignment = copy(src_cell.alignment)
                tgt_cell.number_format = src_cell.number_format

def transform_excel(input_file, output_file):
    wb_input = load_workbook(input_file)
    wb_output = load_workbook(output_file)

    if "PFMEA-Format" not in wb_output.sheetnames:
        print("[ERROR] 'PFMEA-Format' sheet is missing in output/template file")
        sys.exit(1)

    template_ws = wb_output["PFMEA-Format"]

    for sheet_name in SHEET_NAMES:
        if sheet_name not in wb_input.sheetnames:
            print(f"[SKIP] Sheet '{sheet_name}' not found in input file")
            continue

        input_ws = wb_input[sheet_name]

        # Create or clear sheet in output file
        if sheet_name in wb_output.sheetnames:
            del wb_output[sheet_name]
        new_ws = wb_output.create_sheet(title=sheet_name)

        # Copy template A1:S8 from PFMEA-Format
        copy_range_formatting(template_ws, new_ws, "A1:S8")

        # Read header from input (starting after row 8)
        header_row = input_ws[9]  # Row 9 is index 8 (1-based)

        # Copy and map headers to row 8
        for orig_idx, new_idx in COLUMN_INDEX_MAP.items():
            if orig_idx < len(header_row):
                cell_value = header_row[orig_idx].value
                if cell_value:
                    cell = new_ws.cell(row=8, column=new_idx + 1, value=cell_value)
                    cell.font = Font(bold=True)

        # Copy data rows from row 10 onward
        for row_idx, row in enumerate(input_ws.iter_rows(min_row=10), start=9):
            for orig_idx, new_idx in COLUMN_INDEX_MAP.items():
                if orig_idx < len(row):
                    cell_value = row[orig_idx].value
                    cell = new_ws.cell(row=row_idx, column=new_idx + 1, value=cell_value)
                    if row[orig_idx].has_style:
                        cell.font = copy(row[orig_idx].font)
                        cell.fill = copy(row[orig_idx].fill)
                        cell.alignment = copy(row[orig_idx].alignment)
                        cell.border = copy(row[orig_idx].border)

    wb_output.save(output_file)
    print(f"[OK] Output saved as: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python excel_transformer.py <input.xlsx> <output_template.xlsx>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"[ERROR] File not found: {input_file}")
        sys.exit(1)

    transform_excel(input_file, output_file)
