import os
import shutil
from datetime import datetime

SOURCE_DIR = r"C:/Users/USER/Documents/CU Files"
BACKUP_DIR = r"F:/Backup"

try:
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  destination = os.path.join(BACKUP_DIR, timestamp)
  os.makedirs(destination, exist_ok=True)
  shutil.copytree(SOURCE_DIR, os.path.join(destination, "CU Files"))
  print("Backup Completed Succesfully")
except FileNotFoundError:
  print("Folder was not Found.")
except FileExistsError:
  print("Backup already exists.")
except PermissionError:
  print("Permission Denied.")
except Exception as err:
  print(f"Error Found: {err}")