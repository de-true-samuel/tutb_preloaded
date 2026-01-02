import os
import shutil
import json
from datetime import datetime
import sys

BACKUP_DIR = r"F:/Backup"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
destination = os.path.join(BACKUP_DIR, timestamp)
json_file = r"C:/Users/USER/Desktop/VS Codes/Code_Folder/REAL_PROJECTS/backup_script/files_to_backup.json"

try:
  with open(json_file, 'r', encoding='utf-8') as f:
    source_dirs = json.load(f)
except json.JSONDecodeError:
  print("Error: Invalid JSON in config file.")
  sys.exit(1)
for source in source_dirs['file_paths']:
  try:
    source_dir_name = source.split("/")[-1]
    print(source_dir_name)
    new_file_path = os.path.join(destination, source_dir_name)
    os.makedirs(destination, exist_ok=True)
    shutil.copytree(source, new_file_path)
    print(f"File has beed backed-up in: {destination} ")
  except FileNotFoundError:
    print("Error: Invalid JSON in config file {config_path}")
    print(f"{source} doesn't exist.")
  except FileExistsError:
    print(f"Folder already Backed up: {destination}. Skipping..")
  except PermissionError:
    print("Permission to handle file was denied")
  except Exception as err:
    print(f"Error Found: {err}")