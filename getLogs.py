#!/usr/bin/env python3

import os
import shutil

def read_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def copy_matching_folders(ids, source_folder='/ccshare/logs/smplogs', destination_folder='logs'):
    # Check if the destination folder exists, if not, create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all folders in the source directory
    try:
        source_folders = [f for f in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, f))]
    except FileNotFoundError:
        print(f"Source folder {source_folder} not found.")
        return

    # Loop through each folder and check if its name matches any ID
    for folder in source_folders:
        if folder in ids:
            src_path = os.path.join(source_folder, folder)
            dest_path = os.path.join(destination_folder, folder)

            # Create a temporary directory to store the files to be archived
            temp_dir = os.path.join(destination_folder, f"{folder}_temp")
            os.makedirs(temp_dir, exist_ok=True)

            # Traverse the folder structure and copy specific files
            for root, dirs, files in os.walk(src_path):
                for filename in files:
                    if filename.endswith(('input_mgr.0.gz', 'NetConMgr.1.gz', 'NetConMgr.0.gz')):
                        file_src_path = os.path.join(root, filename)
                        file_dest_path = os.path.join(temp_dir, filename)
                        shutil.copy(file_src_path, file_dest_path)

            # Create a .gz archive for the folder
            try:
                shutil.make_archive(dest_path, 'gztar', temp_dir)
                print(f"Archived {folder} to {dest_path}.gz")
            except Exception as e:
                print(f"Failed to archive {folder}. Error: {e}")

            # Remove the temporary directory
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    # Read IDs from file
    ids_to_match = read_ids_from_file('list.txt')

    if ids_to_match:
        copy_matching_folders(ids_to_match)
