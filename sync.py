import argparse
import os
import shutil
import time


def sync_folders(source_folder, target_folder):
    # Get paths for both source and target folder
    source_folder = os.path.abspath(source_folder)
    target_folder = os.path.abspath(target_folder)

    # Create directory for target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print("Created target folder: " + target_folder)

    # List files on source and target folder, str() is used to convert the list into a string
    source_files = os.listdir(source_folder)
    target_files = os.listdir(target_folder)
    print("Files in " + source_folder + ": " + str(source_files))
    print("Files in " + target_folder + ": " + str(target_files))

    # Remove files or directories from target folder that don't exist on the source folder
    for name in target_files:
        target_item = os.path.join(target_folder, name)  # Join paths between target_folder and the item on the folder
        if name not in source_files:
            if os.path.isfile(target_item):
                os.remove(target_item)
                print("Removed file: " + target_item + " from the " + target_folder)
            elif os.path.islink(target_item):
                os.remove(target_item)
                print("Removed symbolic link: " + target_item + " from the " + target_folder)
            elif os.path.isdir(target_item):
                shutil.rmtree(target_item)
                print("Removed directory: " + target_item + " from the " + target_folder)

    # Copy files from the source folder to the target folder
    for name in source_files:
        source_item = os.path.join(source_folder, name)
        target_item = os.path.join(target_folder, name)
        if os.path.isfile(source_item):  # Copy a file
            shutil.copy(source_item, target_item)
            print("Copied file named: " + source_item + " to " + target_item)
        elif os.path.isdir(source_item):  # Copy a directory
            if not os.path.exists(target_item):
                shutil.copytree(source_item, target_item)
                print("Copied directory named: " + source_item + " to " + target_item)
            else:
                sync_folders(source_item, target_item)  # Sync subdirectories on the target folder
                print("All subdirectories from: " + source_item + " were copied to " + target_item)


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Script to copy files from source folder to replica folder.")
    parser.add_argument("-s", "--source", type=str, help="Path to the source folder.")
    parser.add_argument("-r", "--replica", type=str, help="Path to the replica folder.")
    parser.add_argument("-i", "--interval", type=int, help="Interval in seconds between synchronization.")

    # Parse command-line arguments
    args = parser.parse_args()

    # Check if the paths where given on the command line
    if not args.source or not args.replica or not args.interval:
        parser.print_help()
    else:
        while True:
            source_folder = args.source
            target_folder = args.replica

            sync_folders(source_folder, target_folder)
            # Time.sleep is measured in seconds
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
