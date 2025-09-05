import os
import sys
import shutil

def extract_folder_name(filename):
    # Assuming the filename starts with the folder name before the first underscore
    return filename.split('_')[0]

def move_file_to_folder(filepath):
    if not os.path.isfile(filepath):
        print(f"[SKIP] Not a valid file: {filepath}")
        return

    filename = os.path.basename(filepath)
    folder_name = extract_folder_name(filename)
    folder_path = os.path.join(os.path.dirname(filepath), folder_name)

    # Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Destination path
    dest_path = os.path.join(folder_path, filename)

    # Move the file
    shutil.move(filepath, dest_path)
    print(f"[OK] Moved '{filename}' to '{folder_path}'")

def main():
    if len(sys.argv) < 2:
        print("Usage: python organize_files_by_serial.py <folder_with_dat_files>")
        sys.exit(1)

    base_dir = sys.argv[1]
    if not os.path.isdir(base_dir):
        print(f"[ERROR] Invalid directory: {base_dir}")
        sys.exit(1)

    # Move each .dat file
    for entry in os.listdir(base_dir):
        if entry.lower().endswith(".dat"):
            full_path = os.path.join(base_dir, entry)
            move_file_to_folder(full_path)

if __name__ == "__main__":
    main()
