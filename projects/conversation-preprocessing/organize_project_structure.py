"""
Script to reorganize the 'conversation-preprocessing' project folder
into a more structured layout.

This script will:
- Create new directories: config, scripts, logs, data (with subdirectories).
- Move .py scripts to scripts/.
- Move config.yaml to config/.
- Move .log files to logs/.
- Move contents of old data folders (raw_logs, cleaned_logs, processed_logs)
to new locations under data/ and remove old folders.
- Rewrite existing .bat files to update paths.
- Creates an 'archive' folder for specified old/unhandled files.

Run this script from the root of the 'conversation-preprocessing' directory.
It's highly recommended to BACK UP YOUR PROJECT FOLDER before running this.
"""

import os
import shutil
import argparse

__version__ = "1.0.0"
__author__ = "Kode_Animator (with A.C.E. assistance)"

# --- Configuration: Define target structure and files ---

# New directory names
CONFIG_DIR = "config"
SCRIPTS_DIR = "scripts"
LOGS_DIR = "logs"
DATA_DIR = "data"
ARCHIVE_DIR = "archive" # For old/unhandled files

# New data subdirectories under DATA_DIR
DATA_RAW_LOGS = os.path.join(DATA_DIR, "raw_logs")
DATA_CLEANED_SIGNPOSTED = os.path.join(DATA_DIR, "01_cleaned_signposted")
DATA_ATTRIBUTED_TEXT = os.path.join(DATA_DIR, "02_attributed_text")
DATA_JSON_OUTPUT = os.path.join(DATA_DIR, "03_json_output")

# Python scripts to move to SCRIPTS_DIR
PYTHON_SCRIPTS = [
    "conversation_precleaner_v1.py",
    "conversation_speaker_attributor_v1.py",
    "conversation_to_json_converter_v1.py",
    # This script itself will be moved if found, after execution.
    # "organize_project_structure.py" # Handled separately
]

# Config file to move
CONFIG_FILE = "config.yaml"

# Log files to move
LOG_FILES = ["python_error.log", "python_output.log"]

# Old data folders (key: old name, value: new path under DATA_DIR)
OLD_DATA_FOLDERS_MAP = {
    "raw_logs": DATA_RAW_LOGS,
    "cleaned_logs": DATA_CLEANED_SIGNPOSTED,
    "processed_logs": DATA_ATTRIBUTED_TEXT,
    "json_output": DATA_JSON_OUTPUT, # If it exists
}

# Batch files to rewrite (key: filename, value: associated script name)
BATCH_FILES_TO_REWRITE = {
    "run_precleaner.bat": "conversation_precleaner_v1.py",
    "run_speaker_attributor.bat": "conversation_speaker_attributor_v1.py",
    "run_json_converter.bat": "conversation_to_json_converter_v1.py",
}

# Files/folders to move to ARCHIVE_DIR
FILES_TO_ARCHIVE = [
    "conversation_parser_v3.py", # Old script
    "test_output_dir",           # Old test output
    "run_conversation_parser.bat", # Batch for old script
    "test_permissions.bat"       # Old test batch
]


# --- Helper Functions ---

def create_dir_if_not_exists(dir_path):
    """Creates a directory if it doesn't already exist."""
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            print(f"Successfully created directory: {dir_path}")
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")
            # Decide if this is a critical error
            raise
    else:
        print(f"Directory already exists: {dir_path}")

def move_file_or_dir(src, dest_dir, dest_name=None):
    """Moves a file or directory to a destination directory."""
    if not os.path.exists(src):
        print(f"Source not found, skipping move: {src}")
        return False
    
    dest_path = os.path.join(dest_dir, dest_name if dest_name else os.path.basename(src))
    try:
        shutil.move(src, dest_path)
        print(f"Successfully moved '{src}' to '{dest_path}'")
        return True
    except Exception as e:
        print(f"Error moving '{src}' to '{dest_path}': {e}")
        return False

def move_folder_contents(src_folder, dest_folder):
    """Moves all contents from src_folder to dest_folder, then removes src_folder."""
    if not os.path.isdir(src_folder):
        print(f"Source folder not found, skipping content move: {src_folder}")
        return False

    create_dir_if_not_exists(dest_folder)
    moved_anything = False
    for item_name in os.listdir(src_folder):
        src_item_path = os.path.join(src_folder, item_name)
        dest_item_path = os.path.join(dest_folder, item_name)
        try:
            shutil.move(src_item_path, dest_item_path)
            print(f"  Moved '{src_item_path}' to '{dest_item_path}'")
            moved_anything = True
        except Exception as e:
            print(f"  Error moving item '{src_item_path}': {e}")
    
    if moved_anything or not os.listdir(src_folder): # Remove if empty or successfully moved
        try:
            shutil.rmtree(src_folder)
            print(f"Successfully removed old data folder: {src_folder}")
        except Exception as e:
            print(f"Error removing old data folder '{src_folder}': {e}. Please remove manually.")
    return True


def rewrite_batch_file(bat_filename, script_name, old_data_paths, new_data_paths_map):
    """
    Rewrites a batch file to update script path and data paths.
    old_data_paths: list of old path segments like ".\raw_logs"
    new_data_paths_map: dict mapping old path segment to new like {".\raw_logs": ".\data\raw_logs"}
    """
    if not os.path.exists(bat_filename):
        print(f"Batch file not found, cannot rewrite: {bat_filename}")
        return

    # Backup original batch file
    backup_filename = bat_filename + ".bak"
    try:
        shutil.copyfile(bat_filename, backup_filename)
        print(f"Backed up '{bat_filename}' to '{backup_filename}'")
    except Exception as e:
        print(f"Could not back up '{bat_filename}': {e}. Skipping rewrite.")
        return

    new_lines = []
    script_path_updated = False
    paths_updated_in_file = False

    with open(backup_filename, 'r') as f_in: # Read from backup
        for line in f_in:
            original_line = line
            # Update SCRIPT_NAME path
            if f'SET SCRIPT_NAME="{script_name}"' in line:
                line = f'SET SCRIPT_NAME=".\\{SCRIPTS_DIR}\\{script_name}"\n'
                script_path_updated = True
                paths_updated_in_file = True
            else:
                # Update data paths
                for old_path_segment, new_path_segment in new_data_paths_map.items():
                    # Be careful with quotes and variable names (e.g., INPUT_FILE_OR_DIR, OUTPUT_DIR)
                    # This is a simplified replacement; more robust parsing might be needed for complex batch files.
                    if old_path_segment in line:
                        line = line.replace(old_path_segment, new_path_segment)
                        paths_updated_in_file = True
            new_lines.append(line)

    if paths_updated_in_file:
        try:
            with open(bat_filename, 'w') as f_out:
                f_out.writelines(new_lines)
            print(f"Successfully rewrote '{bat_filename}' with updated paths.")
        except Exception as e:
            print(f"Error writing updated batch file '{bat_filename}': {e}")
    else:
        print(f"No path updates were made to '{bat_filename}' (perhaps already updated or paths not found).")


# --- Main Reorganization Logic ---
def organize_project(this_script_name="organize_project_structure.py"):
    print("Starting project reorganization...")
    print("IMPORTANT: Please ensure you have backed up your project folder before proceeding.")
    # confirmation = input("Type 'YES' to continue, anything else to abort: ")
    # if confirmation.upper() != 'YES':
    #     print("Operation aborted by user.")
    #     return

    # 1. Create new directory structure
    print("\n--- Creating New Directories ---")
    base_dirs_to_create = [CONFIG_DIR, SCRIPTS_DIR, LOGS_DIR, DATA_DIR, ARCHIVE_DIR]
    data_subdirs_to_create = [DATA_RAW_LOGS, DATA_CLEANED_SIGNPOSTED, DATA_ATTRIBUTED_TEXT, DATA_JSON_OUTPUT]
    
    for dir_path in base_dirs_to_create + data_subdirs_to_create:
        create_dir_if_not_exists(dir_path)

    # 2. Move Python scripts
    print("\n--- Moving Python Scripts ---")
    for script_file in PYTHON_SCRIPTS:
        if script_file == this_script_name:
            print(f"Skipping move for the currently running script: {script_file}")
            continue
        move_file_or_dir(script_file, SCRIPTS_DIR)
    
    # 3. Move config file
    print("\n--- Moving Config File ---")
    move_file_or_dir(CONFIG_FILE, CONFIG_DIR)

    # 4. Move log files
    print("\n--- Moving Log Files ---")
    for log_file in LOG_FILES:
        move_file_or_dir(log_file, LOGS_DIR)

    # 5. Move contents of old data folders
    print("\n--- Migrating Data Folders ---")
    for old_folder, new_path in OLD_DATA_FOLDERS_MAP.items():
        move_folder_contents(old_folder, new_path)
        
    # 6. Rewrite Batch Files
    print("\n--- Rewriting Batch Files ---")
    # Define how old path segments in batch files map to new ones
    # This needs to be robust enough for common SET commands in your batch files.
    # Example: SET VAR=".\old_path" -> SET VAR=".\data\new_path_under_data"
    batch_path_replacements = {
        # For run_precleaner.bat
        '"'+os.path.join(".", "raw_logs")+'"': '"'+os.path.join(".", DATA_RAW_LOGS)+'"', # .\raw_logs
        '"'+os.path.join(".", "cleaned_logs")+'"': '"'+os.path.join(".", DATA_CLEANED_SIGNPOSTED)+'"', # .\cleaned_logs
        # For run_speaker_attributor.bat
        # (cleaned_logs already mapped)
        '"'+os.path.join(".", "processed_logs")+'"': '"'+os.path.join(".", DATA_ATTRIBUTED_TEXT)+'"', # .\processed_logs
        # For run_json_converter.bat
        # (processed_logs already mapped)
        '"'+os.path.join(".", "json_output")+'"': '"'+os.path.join(".", DATA_JSON_OUTPUT)+'"', # .\json_output
    }
    for bat_file, script_name_in_bat in BATCH_FILES_TO_REWRITE.items():
        rewrite_batch_file(bat_file, script_name_in_bat, [], batch_path_replacements)

    # 7. Move unhandled/old files to archive
    print("\n--- Archiving Old/Unhandled Files ---")
    for item_to_archive in FILES_TO_ARCHIVE:
        move_file_or_dir(item_to_archive, ARCHIVE_DIR)
        
    # 8. Move this script itself to the scripts folder at the very end
    if os.path.exists(this_script_name): # Check if it's in the root
        print(f"\n--- Moving this script ('{this_script_name}') to '{SCRIPTS_DIR}' ---")
        if not move_file_or_dir(this_script_name, SCRIPTS_DIR):
            print(f"Please manually move '{this_script_name}' to the '{SCRIPTS_DIR}' folder.")
        else:
            print(f"Note: This script has been moved. To run it again, navigate to '{SCRIPTS_DIR}'.")


    print("\nProject reorganization process finished.")
    print("Please review the changes and manually update any paths in your VS Code workspace or other tools if needed.")
    print("Remember to check the new batch files in the root directory.")

if __name__ == "__main__":
    # Get the name of the current script to avoid moving it prematurely
    current_script_name = os.path.basename(__file__)
    organize_project(this_script_name=current_script_name)

