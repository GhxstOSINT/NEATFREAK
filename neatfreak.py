import os
import time
import json
import shutil
import ctypes
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification  # IMPORT FOR NOTIFICATIONS

# --- CONFIGURATION LOAD ---
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print("ERROR: config.json not found.")
    exit()

WATCH_DIR = Path(config['watch_directory'])
EXTENSION_MAP = config['extension_map']
LEGACY_FOLDERS = ["Archives", "Documents", "Images", "Installers"]

# --- SAFETY PROTOCOL: IGNORE THESE EXTENSIONS ---
IGNORE_EXTS = [".crdownload", ".part", ".tmp", ".ini"]

ICON_MAP = {
    "Images": 306, "Videos": 115, "Audio": 116, "PDFs": 235, "Word": 235,
    "Installers": 15, "Archives": 39, "Code": 27, "Others": 165,
    "Media": 116, "Docs": 235, "Software": 15, "Dev": 27, "Creative": 306
}

def send_notification(filename, folder):
    """Sends a Windows Toast Notification."""
    try:
        notification.notify(
            title='NEATFREAK Organized',
            message=f'Moved {filename}\nto {folder}',
            app_name='NEATFREAK',
            timeout=3
        )
    except Exception:
        pass # If notifications fail, don't crash the script

def change_folder_icon(folder_path):
    if os.name != 'nt': return 
    folder_name = folder_path.name
    icon_index = 0
    for key, index in ICON_MAP.items():
        if key in folder_name:
            icon_index = index
            break
    if icon_index == 0 or (folder_path / "desktop.ini").exists(): return

    try:
        ini_path = folder_path / "desktop.ini"
        with open(ini_path, 'w') as f:
            f.write("[.ShellClassInfo]\n")
            f.write(f"IconResource=%SystemRoot%\\system32\\SHELL32.dll,{icon_index}\n")
            f.write("[ViewState]\n")
            f.write("Mode=\n")
            f.write("Vid=\n")
            f.write("FolderType=Generic\n")

        FILE_ATTRIBUTE_HIDDEN = 0x02
        FILE_ATTRIBUTE_SYSTEM = 0x04
        FILE_ATTRIBUTE_READONLY = 0x01
        ctypes.windll.kernel32.SetFileAttributesW(str(ini_path), FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)
        ctypes.windll.kernel32.SetFileAttributesW(str(folder_path), FILE_ATTRIBUTE_READONLY)
    except Exception:
        pass

def force_update_icons():
    # Only scan specifically for folders we know we manage to save CPU
    for root, dirs, files in os.walk(WATCH_DIR):
        for dir_name in dirs:
            if dir_name not in LEGACY_FOLDERS:
                change_folder_icon(Path(root) / dir_name)

def sort_single_file(file_path):
    try:
        # SAFETY CHECK 1: Don't move script files
        if file_path.name in ["neatfreak.py", "config.json", "neatfreak.pyw"]: return
        
        # SAFETY CHECK 2: Don't touch incomplete downloads
        if file_path.suffix.lower() in IGNORE_EXTS: return

        extension = file_path.suffix.lower()
        if extension in EXTENSION_MAP:
            dest_folder_name = EXTENSION_MAP[extension]
        else:
            dest_folder_name = "Others"

        dest_dir = WATCH_DIR / dest_folder_name
        if not dest_dir.exists():
            os.makedirs(dest_dir, exist_ok=True)
            change_folder_icon(dest_dir)

        final_path = dest_dir / file_path.name
        counter = 1
        while final_path.exists():
            final_path = dest_dir / f"{file_path.stem}_{counter}{extension}"
            counter += 1

        shutil.move(str(file_path), str(final_path))
        print(f"MOVED: {file_path.name} -> {dest_folder_name}")
        
        # TRIGGER NOTIFICATION
        send_notification(file_path.name, dest_folder_name)

    except Exception as e:
        print(f"Error: {e}")

def organize_files():
    print(f"--- Scanning: {WATCH_DIR} ---")
    
    # 1. Root Scan
    for item in os.listdir(WATCH_DIR):
        item_path = WATCH_DIR / item
        if item_path.is_file():
            sort_single_file(item_path)
    
    # 2. Legacy Scan
    for folder_name in LEGACY_FOLDERS:
        legacy_path = WATCH_DIR / folder_name
        if legacy_path.exists() and legacy_path.is_dir():
            for item in os.listdir(legacy_path):
                item_path = legacy_path / item
                if item_path.is_file():
                    sort_single_file(item_path)
            try:
                legacy_path.rmdir()
            except OSError:
                pass
    
    force_update_icons()

class NeatFreakHandler(FileSystemEventHandler):
    def on_modified(self, event): organize_files()
    def on_created(self, event): organize_files()

if __name__ == "__main__":
    print("Performing startup cleanup...")
    organize_files() 
    print("Startup cleanup complete.")

    event_handler = NeatFreakHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=True)
    
    print(f"NEATFREAK Active. Monitoring: {WATCH_DIR}")
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()