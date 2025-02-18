import sys
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
EXCLUDED_FOLDERS = {".git"}
INSTALL_SCRIPT_PREFIX = "install"

# List all folders in a directory and return as a list
def list_folders(directory):
    return [p for p in Path(directory).iterdir() if p.is_dir() and p.name not in EXCLUDED_FOLDERS]

# Show menu for folder selection
def show_menu(folders, level):
    count = 1
    for folder in folders:
        print(f"{count}. {folder.name}")
        count += 1

    if level > 0:
        print(f"{count}. Return")
        count += 1
    print(f"{count}. Exit")

# Execute the install script if present
def execute_install_script(directory):
    folder_name = Path(directory).name
    script_name = f"{INSTALL_SCRIPT_PREFIX}{folder_name}.sh"
    script_path = Path(directory) / script_name
    
    if script_path.is_file():
        logging.info(f"Executing install script: {script_path}")
        os.system(f"bash {script_path}")
    else:
        logging.info(f"No install script found in {directory}")

# Handle user selection
def handle_selection(folders, level, current_path):
    try:
        choice = int(input("Select an option: "))
        if choice == len(folders) + 2:
            sys.exit()
        elif choice == len(folders) + 1:
            return current_path.parent, level - 1
        elif 1 <= choice <= len(folders):
            return folders[choice - 1], level + 1
        else:
            print("Invalid selection. Please try again.")
            return current_path, level
    except ValueError:
        print("Invalid input. Please enter a number.")
        return current_path, level

# Main function to navigate directories
def navigate_directories(root, level=0):
    current_path = Path(root)
    while True:
        folders = list_folders(current_path)
        if not folders:
            execute_install_script(current_path)
            break

        show_menu(folders, level)
        current_path, level = handle_selection(folders, level, current_path)

if __name__ == "__main__":
    #root_directory = input("Enter the root directory: ")
    root_directory = "."
    if not os.path.isdir(root_directory):
        print(f"Error: {root_directory} is not a valid directory.")
        sys.exit(1)
    navigate_directories(root_directory)
