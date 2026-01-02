# Compression and Efficiency Time
import os
import shutil
import json
from datetime import datetime
import sys
from pathlib import Path
import zipfile
import time
import stat

def load_config(config_path):
    """Load and validate configuration"""
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in config file {config_path}")
        sys.exit(1)
    
    return config

def validate_paths(paths):
    """Check if all source paths exist"""
    valid_paths = []
    invalid_paths = []
    
    for path in paths:
        if os.path.exists(path):
            valid_paths.append(path)
        else:
            invalid_paths.append(path)
            print(f"Warning: Source path does not exist: {path}")
    
    return valid_paths, invalid_paths

def zip_in_same_parent(source_folder):
    source_path = Path(source_folder).resolve() # Full path to the folder
    parent_dir = source_path.parent             # The folder containing the source
    
    # Define the zip name (e.g., MyData.zip)
    zip_name = f"{source_path.name}.zip"
    zip_full_path = parent_dir / zip_name

    with zipfile.ZipFile(zip_full_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_path):
            for filename in filenames:
                file_path = Path(foldername) / filename
                
                # IMPORTANT: Skip the zip file itself if it's being created inside the source
                if file_path == zip_full_path:
                    continue
                    
                arcname = file_path.relative_to(source_path)
                zipf.write(file_path, arcname)
    
    print(f"\nZip created at: {zip_full_path}")

def remove_readonly(func, path, excinfo):
    """Clear the read-only bit and reattempt the deletion."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    # Use relative or configurable config path
    CONFIG_PATH = Path('files_to_backup.json')  # Or make this configurable
    BACKUP_DIR = Path(r"F:/Backup")
    MAX_BACKUP = 5
    
    # Load configuration
    config = load_config(CONFIG_PATH)
    
    if 'file_paths' not in config:
        print("Error: 'file_paths' key not found in config")
        sys.exit(1)
    
    # Validate all source paths
    valid_paths, invalid_paths = validate_paths(config['file_paths'])
    
    if not valid_paths:
        print("Error: No valid source paths to backup")
        sys.exit(1)
    
    # Create backup directory once
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_file = BACKUP_DIR / f"backup_{timestamp}"
    
    try:
        os.makedirs(zip_file, exist_ok=True)
    except OSError as e:
        print(f"Error: Cannot create backup directory {zip_file}: {e}")
        sys.exit(1)
    
    # Backup valid paths
    successful_backups = []
    failed_backups = []
    
    for source in valid_paths:
        source_dir_name = os.path.basename(source.rstrip('/\\'))
        new_file_path = zip_file / source_dir_name
        
        try:
            if os.path.exists(new_file_path):
                print(f"Skipping {source} - already exists in backup")
                continue
                
            shutil.copytree(source, new_file_path)
            successful_backups.append(source)
            print(f"Successfully backed up: {source} to {new_file_path}")

        except Exception as e:
            failed_backups.append((source, str(e)))
            print(f"Failed to backup {source}: {e}")

    zip_in_same_parent(zip_file) #Creating the zip folder
    temp_file = zip_file
    time.sleep(1)
    try:
        if os.path.exists(temp_file):
            shutil.rmtree(temp_file, onexc=remove_readonly)
            print(f"\nTemporary folder has been deleted successfully!: {zip_file}")
    except PermissionError:\
        print(f"\nAccess Denied. Could not delete file: {zip_file}")
    except OSError:
        print(f"\nError: Cannot deleted file -> {zip_file}")
    except Exception as err:
        print(f"\nError Occured: {err}")
    # Summary report
    print(f"\nBackup Summary:")
    print(f"Successful: {len(successful_backups)}")
    print(f"Failed: {len(failed_backups)}")
    print(f"Skipped (invalid paths): {len(invalid_paths)}")
    print(f"Backup location: {zip_file}")

if __name__ == "__main__":
    main()