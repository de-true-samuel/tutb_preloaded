#Version_1 of fire_organizer

from pathlib import Path
import os
import shutil
import sys


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", '.csv'],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Archives": [".zip", ".tar", ".gz"],
    "Set-Ups": ['.exe'],
}

og_file_path = r"C:\Users\USER\Downloads"


def get_category(ext: str, file_type: dict) -> str:
  for category, exts in file_type.items():
    if ext in exts:
      return category
  return "Others"

def organize_file(source_path: str):
  file_path = Path(source_path)
  files_only = [item for item in file_path.iterdir() if item.is_file()]

  for file in files_only:
    ext = file.suffix.lower()
    if not ext: continue
    new_dir = file_path / get_category(ext, FILE_TYPES)
    try:
      os.makedirs(new_dir, exist_ok=True)
      shutil.move(file, new_dir)
      print(f"Moved {file.name} --> {new_dir}\n")
    except PermissionError:
      print(f"Permission denied: {file.name}. Skipping...")
    except FileNotFoundError:
      print(f"File not found: {file}. Skipping...")
    except Exception as err:
      print(f"Error Found: {err}")
  print("")

if __name__ == "__main__":
  path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\USER\Downloads"
  organize_file(path)

# import schedule
# import time
# schedule.every().day.at("20:00").do(organize_file)

# while True:
#   schedule.run_pending()
#   time.sleep(1)
