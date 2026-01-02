# Refactored and Efficient Version of main_v3.0.py
import os
import shutil
import json
from datetime import datetime
import sys

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

def main():
    # Use relative or configurable config path
    CONFIG_PATH = 'files_to_backup.json'  # Or make this configurable
    BACKUP_DIR = r"F:/Backup"
    
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
    destination = os.path.join(BACKUP_DIR, timestamp)
    
    try:
        os.makedirs(destination, exist_ok=True)
    except OSError as e:
        print(f"Error: Cannot create backup directory {destination}: {e}")
        sys.exit(1)
    
    # Backup valid paths
    successful_backups = []
    failed_backups = []
    
    for source in valid_paths:
        source_dir_name = os.path.basename(source.rstrip('/\\'))
        new_file_path = os.path.join(destination, source_dir_name)
        
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
    
    # Summary report
    print(f"\nBackup Summary:")
    print(f"Successful: {len(successful_backups)}")
    print(f"Failed: {len(failed_backups)}")
    print(f"Skipped (invalid paths): {len(invalid_paths)}")
    print(f"Backup location: {destination}")

if __name__ == "__main__":
    main()