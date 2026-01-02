import shutil
import os

SOURCE_FOLDER = r"C:\Users\USER\Documents\CU Files"
BACKUP_FOLDER = r"F:\Backup"
try:
  os.makedirs(BACKUP_FOLDER, exist_ok=True)
  destination = os.path.join(BACKUP_FOLDER, "CU Files")
  shutil.copytree(SOURCE_FOLDER, destination)
  print("Backup Completely Successfully!")
except FileExistsError:
  print("Backup Already Exists.")
except FileNotFoundError:
  print("Folder couldn't be found.")
except PermissionError:
  print("Access Denied")
except Exception as err:
  print(f"Error Found: {err}")