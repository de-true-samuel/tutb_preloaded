#!/usr/bin/env python3
"""
File Organizer - A robust tool to organize files by type, date, or custom rules.
"""

import os
import shutil
import argparse
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import sys
from typing import Dict, List, Set, Optional, Tuple
import mimetypes
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_organizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FileOrganizer:
    """Main file organizer class with multiple organization strategies."""
    
    # Common file extensions by category
    FILE_CATEGORIES = {
        'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.ico'},
        'documents': {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.md', '.tex'},
        'spreadsheets': {'.xls', '.xlsx', '.csv', '.ods'},
        'presentations': {'.ppt', '.pptx', '.odp'},
        'archives': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'},
        'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'},
        'video': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'},
        'code': {'.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.json', '.xml'},
        'executables': {'.exe', '.msi', '.app', '.sh', '.bat'},
        'fonts': {'.ttf', '.otf', '.woff', '.woff2'},
        'data': {'.json', '.xml', '.yaml', '.yml', '.sql', '.db', '.sqlite'},
        'torrents': {'.torrent'},
    }
    
    def __init__(self, source_dir: str, dest_dir: Optional[str] = None, 
                 dry_run: bool = False, strategy: str = 'type'):
        """
        Initialize the organizer.
        
        Args:
            source_dir: Directory to organize
            dest_dir: Destination directory (optional, defaults to source_dir)
            dry_run: If True, only show what would be done
            strategy: Organization strategy ('type', 'date', 'extension', 'custom')
        """
        self.source_dir = Path(source_dir).expanduser().resolve()
        self.dest_dir = Path(dest_dir).expanduser().resolve() if dest_dir else self.source_dir
        self.dry_run = dry_run
        self.strategy = strategy
        
        # Ensure directories exist
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Load custom rules if they exist
        self.custom_rules = self._load_custom_rules()
        
        # Track moved files for summary
        self.moved_files = []
        self.skipped_files = []
        self.error_files = []
        
        logger.info(f"Initialized organizer with strategy: {strategy}")
        logger.info(f"Source: {self.source_dir}")
        logger.info(f"Destination: {self.dest_dir}")
        logger.info(f"Dry run: {dry_run}")
    
    def _load_custom_rules(self) -> Dict[str, str]:
        """Load custom organization rules from JSON file."""
        rules_file = self.source_dir / 'organizer_rules.json'
        if rules_file.exists():
            try:
                with open(rules_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error loading custom rules: {e}")
        return {}
    
    def _get_file_category(self, file_path: Path) -> str:
        """Determine the category of a file based on its extension."""
        suffix = file_path.suffix.lower()
        
        # Check custom rules first
        for category, extensions in self.custom_rules.items():
            if suffix in extensions:
                return category
        
        # Check predefined categories
        for category, extensions in self.FILE_CATEGORIES.items():
            if suffix in extensions:
                return category
        
        # Try to determine from MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type:
            main_type = mime_type.split('/')[0]
            if main_type in ['image', 'audio', 'video']:
                return main_type + 's'
        
        # Default category
        return 'other'
    
    def _get_date_folder(self, file_path: Path) -> str:
        """Get folder name based on file modification date."""
        try:
            mod_time = file_path.stat().st_mtime
            date_obj = datetime.fromtimestamp(mod_time)
            return date_obj.strftime('%Y-%m')
        except (OSError, AttributeError) as e:
            logger.warning(f"Could not get date for {file_path}: {e}")
            return 'unknown_date'
    
    def _create_safe_filename(self, original_path: Path, target_dir: Path) -> Path:
        """Create a safe filename to avoid overwrites."""
        counter = 1
        new_path = target_dir / original_path.name
        
        while new_path.exists():
            stem = original_path.stem
            suffix = original_path.suffix
            new_name = f"{stem}_{counter}{suffix}"
            new_path = target_dir / new_name
            counter += 1
        
        return new_path
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (IOError, OSError) as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def _is_duplicate(self, source_file: Path, target_file: Path) -> bool:
        """Check if files are duplicates by comparing hashes."""
        if not target_file.exists():
            return False
        
        source_hash = self._calculate_hash(source_file)
        target_hash = self._calculate_hash(target_file)
        
        return source_hash == target_hash
    
    def organize_by_type(self) -> None:
        """Organize files by their type/category."""
        logger.info("Starting organization by type...")
        
        for file_path in self._get_files_to_organize():
            try:
                category = self._get_file_category(file_path)
                dest_folder = self.dest_dir / category
                dest_folder.mkdir(exist_ok=True)
                
                dest_path = self._create_safe_filename(file_path, dest_folder)
                
                # Check for duplicates
                if dest_path.exists() and self._is_duplicate(file_path, dest_path):
                    logger.info(f"Skipping duplicate file: {file_path.name}")
                    self.skipped_files.append((file_path, "Duplicate file"))
                    continue
                
                if not self.dry_run:
                    shutil.move(str(file_path), str(dest_path))
                    logger.info(f"Moved {file_path.name} -> {dest_folder.name}/")
                else:
                    logger.info(f"[DRY RUN] Would move {file_path.name} -> {dest_folder.name}/")
                
                self.moved_files.append((file_path, dest_path))
                
            except (OSError, shutil.Error, PermissionError) as e:
                logger.error(f"Error moving {file_path}: {e}")
                self.error_files.append((file_path, str(e)))
    
    def organize_by_date(self) -> None:
        """Organize files by modification date."""
        logger.info("Starting organization by date...")
        
        for file_path in self._get_files_to_organize():
            try:
                date_folder = self._get_date_folder(file_path)
                dest_folder = self.dest_dir / date_folder
                dest_folder.mkdir(exist_ok=True)
                
                dest_path = self._create_safe_filename(file_path, dest_folder)
                
                if not self.dry_run:
                    shutil.move(str(file_path), str(dest_path))
                    logger.info(f"Moved {file_path.name} -> {date_folder}/")
                else:
                    logger.info(f"[DRY RUN] Would move {file_path.name} -> {date_folder}/")
                
                self.moved_files.append((file_path, dest_path))
                
            except (OSError, shutil.Error, PermissionError) as e:
                logger.error(f"Error moving {file_path}: {e}")
                self.error_files.append((file_path, str(e)))
    
    def organize_by_extension(self) -> None:
        """Organize files by their extension."""
        logger.info("Starting organization by extension...")
        
        for file_path in self._get_files_to_organize():
            try:
                # Skip files without extensions
                if not file_path.suffix:
                    self.skipped_files.append((file_path, "No extension"))
                    continue
                
                ext_folder = file_path.suffix.lower().lstrip('.')
                if not ext_folder:
                    ext_folder = 'no_extension'
                
                dest_folder = self.dest_dir / ext_folder
                dest_folder.mkdir(exist_ok=True)
                
                dest_path = self._create_safe_filename(file_path, dest_folder)
                
                if not self.dry_run:
                    shutil.move(str(file_path), str(dest_path))
                    logger.info(f"Moved {file_path.name} -> {ext_folder}/")
                else:
                    logger.info(f"[DRY RUN] Would move {file_path.name} -> {ext_folder}/")
                
                self.moved_files.append((file_path, dest_path))
                
            except (OSError, shutil.Error, PermissionError) as e:
                logger.error(f"Error moving {file_path}: {e}")
                self.error_files.append((file_path, str(e)))
    
    def organize_custom(self) -> None:
        """Organize files using custom rules."""
        if not self.custom_rules:
            logger.warning("No custom rules found. Falling back to type organization.")
            self.organize_by_type()
            return
        
        logger.info("Starting organization with custom rules...")
        
        for file_path in self._get_files_to_organize():
            try:
                category = self._get_file_category(file_path)
                dest_folder = self.dest_dir / category
                dest_folder.mkdir(exist_ok=True)
                
                dest_path = self._create_safe_filename(file_path, dest_folder)
                
                if not self.dry_run:
                    shutil.move(str(file_path), str(dest_path))
                    logger.info(f"Moved {file_path.name} -> {category}/")
                else:
                    logger.info(f"[DRY RUN] Would move {file_path.name} -> {category}/")
                
                self.moved_files.append((file_path, dest_path))
                
            except (OSError, shutil.Error, PermissionError) as e:
                logger.error(f"Error moving {file_path}: {e}")
                self.error_files.append((file_path, str(e)))
    
    def _get_files_to_organize(self) -> List[Path]:
        """Get list of files to organize, excluding hidden files and directories."""
        files = []
        
        try:
            for item in self.source_dir.iterdir():
                if item.is_file() and not item.name.startswith('.'):
                    files.append(item)
        except (OSError, PermissionError) as e:
            logger.error(f"Error reading directory {self.source_dir}: {e}")
        
        logger.info(f"Found {len(files)} files to organize")
        return files
    
    def create_summary(self) -> str:
        """Create a summary of the organization process."""
        summary = [
            "\n" + "="*60,
            "FILE ORGANIZATION SUMMARY",
            "="*60,
            f"Source Directory: {self.source_dir}",
            f"Destination Directory: {self.dest_dir}",
            f"Strategy: {self.strategy}",
            f"Dry Run: {self.dry_run}",
            "-"*60,
            f"Files Moved: {len(self.moved_files)}",
            f"Files Skipped: {len(self.skipped_files)}",
            f"Files with Errors: {len(self.error_files)}",
        ]
        
        if self.skipped_files:
            summary.append("\nSkipped Files:")
            for file, reason in self.skipped_files[:10]:  # Show first 10
                summary.append(f"  - {file.name}: {reason}")
            if len(self.skipped_files) > 10:
                summary.append(f"  ... and {len(self.skipped_files) - 10} more")
        
        if self.error_files:
            summary.append("\nFiles with Errors:")
            for file, error in self.error_files[:10]:  # Show first 10
                summary.append(f"  - {file.name}: {error}")
            if len(self.error_files) > 10:
                summary.append(f"  ... and {len(self.error_files) - 10} more")
        
        summary.append("="*60)
        
        return "\n".join(summary)
    
    def organize(self) -> bool:
        """Main organization method."""
        logger.info(f"Starting organization process...")
        
        try:
            if self.strategy == 'type':
                self.organize_by_type()
            elif self.strategy == 'date':
                self.organize_by_date()
            elif self.strategy == 'extension':
                self.organize_by_extension()
            elif self.strategy == 'custom':
                self.organize_custom()
            else:
                logger.error(f"Unknown strategy: {self.strategy}")
                return False
            
            # Print summary
            summary = self.create_summary()
            print(summary)
            logger.info("Organization process completed")
            
            return len(self.error_files) == 0
            
        except Exception as e:
            logger.critical(f"Critical error during organization: {e}", exc_info=True)
            return False

def create_custom_rules_template(directory: str) -> None:
    """Create a template for custom organization rules."""
    template = {
        "project_files": [".py", ".ipynb", ".json", ".yaml", ".yml"],
        "design_assets": [".psd", ".ai", ".sketch", ".fig"],
        "backup_files": [".bak", ".backup", ".old"],
        "notes": [".md", ".txt", ".rtf"]
    }
    
    rules_file = Path(directory).expanduser() / 'organizer_rules.json'
    
    if rules_file.exists():
        response = input(f"Rules file already exists at {rules_file}. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    try:
        with open(rules_file, 'w') as f:
            json.dump(template, f, indent=2)
        print(f"Custom rules template created at: {rules_file}")
        print("Edit this file to add your own categories and extensions.")
    except IOError as e:
        logger.error(f"Error creating rules template: {e}")

def get_directory_size(path: Path) -> int:
    """Calculate total size of directory in bytes."""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(Path(entry.path))
    except (OSError, PermissionError):
        pass
    return total

def analyze_directory(directory: str) -> None:
    """Analyze directory structure and file types."""
    path = Path(directory).expanduser().resolve()
    
    if not path.exists():
        print(f"Directory does not exist: {path}")
        return
    
    print(f"\nAnalyzing directory: {path}")
    print("-" * 60)
    
    file_types = defaultdict(int)
    total_files = 0
    total_size = 0
    
    try:
        for item in path.rglob('*'):
            if item.is_file():
                total_files += 1
                total_size += item.stat().st_size
                
                # Categorize by extension
                ext = item.suffix.lower()
                if not ext:
                    ext = 'no_extension'
                file_types[ext] += 1
    except (OSError, PermissionError) as e:
        print(f"Error during analysis: {e}")
    
    # Print summary
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size / (1024*1024):.2f} MB")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    
    # Print file type distribution
    print("\nFile type distribution (top 20):")
    print("-" * 40)
    for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{ext:10} : {count:6} files")
    
    # Suggest organization strategy
    print("\nSuggested organization strategies:")
    if len(file_types) > 10:
        print("  - 'type': Group files by category (images, documents, etc.)")
    if total_files > 100:
        print("  - 'date': Group files by month/year of modification")
    if len(file_types) < 5:
        print("  - 'extension': Group files by their specific extension")

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Robust File Organizer - Organize your files by type, date, or custom rules.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/Downloads --strategy type
  %(prog)s ~/Desktop --dest ~/Organized --dry-run
  %(prog)s --create-rules ~/Documents
  %(prog)s --analyze ~/Downloads
        """
    )
    
    parser.add_argument('directory', nargs='?', default='.',
                       help='Directory to organize (default: current directory)')
    parser.add_argument('--dest', '-d', 
                       help='Destination directory (default: same as source)')
    parser.add_argument('--strategy', '-s', 
                       choices=['type', 'date', 'extension', 'custom'],
                       default='type',
                       help='Organization strategy (default: type)')
    parser.add_argument('--dry-run', '-n', 
                       action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--create-rules', 
                       metavar='DIRECTORY',
                       help='Create a template for custom rules in the specified directory')
    parser.add_argument('--analyze',
                       metavar='DIRECTORY',
                       help='Analyze directory structure and suggest organization strategy')
    
    args = parser.parse_args()
    
    # Handle create-rules command
    if args.create_rules:
        create_custom_rules_template(args.create_rules)
        return
    
    # Handle analyze command
    if args.analyze:
        analyze_directory(args.analyze)
        return
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate source directory
    source_path = Path(args.directory).expanduser().resolve()
    if not source_path.exists():
        print(f"Error: Source directory does not exist: {source_path}")
        sys.exit(1)
    
    if not source_path.is_dir():
        print(f"Error: Source path is not a directory: {source_path}")
        sys.exit(1)
    
    # Create and run organizer
    organizer = FileOrganizer(
        source_dir=args.directory,
        dest_dir=args.dest,
        dry_run=args.dry_run,
        strategy=args.strategy
    )
    
    success = organizer.organize()
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()