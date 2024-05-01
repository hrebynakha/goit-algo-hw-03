"""Home work 1"""
import argparse
import os
from pathlib import Path
import shutil
import hashlib

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--path', type=str, nargs='?', default='files',
                    help='From path to copy files')
parser.add_argument('--dest',  type=str, nargs='?', default='dist',
                    help='Destination path to copy files')
args = parser.parse_args()

class PathNotFound(Exception):
    """Not found path in os"""


def handle_error(func):
    """Decorator function to handle errors"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PathNotFound:
            print("Path not found.")
        except PermissionError:
            print("Permission denied for this folder.")
        except TypeError:
            print("Opps...Some type not correct...")
        except Exception: # disable it to show error
            print("Opps...Some error happend...")
    return inner

def check_hash(file):
    """Checking file hash to allwo duplicates name copy"""
    with open(file, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read()    
        # pipe contents of the file through
        md5 = hashlib.md5(data).hexdigest()
    return md5

@handle_error
def copy_file(file, dest_root):
    """Copy file from path to dest path"""
    suffix = file.suffix if file.suffix else ".not_extension"
    dest_folder = Path(dest_root, suffix)
    if not os.path.exists(dest_folder):
        dest_folder.mkdir(parents=True, exist_ok=False)
    dest_path = Path(dest_folder, file.name)
    do_copy = True
    if os.path.exists(dest_path):
        current_file_hash = check_hash(file)
        if current_file_hash == check_hash(dest_path):
            print(f"OK. Alredy copied file: {file} in {dest_path}")
            do_copy = False
        else:
            new_name = current_file_hash + '__' + str(file.name)
            print(f"WARNING.File: {file} must be rnamed to {new_name}")
            dest_path = Path(dest_folder, new_name)
    if do_copy:
        print(f"Copy from {file} to {dest_path}")
        shutil.copyfile(file, dest_path)

@handle_error
def make_copy(root_path, dest_root):
    """Make copies for files and sort by extentios"""
    for item in root_path.iterdir():
        if item.is_file():
            copy_file(item, dest_root)
        elif item.is_dir():
            make_copy(item, dest_root)

@handle_error
def main():
    """Main function"""
    root_path, dest = Path(args.path), Path(args.dest)
    if not os.path.exists(root_path):
        raise PathNotFound
    # make dest dir
    if not os.path.exists(dest):
        dest.mkdir(parents=True, exist_ok=False)
    make_copy(root_path, dest)

if __name__ == "__main__":
    main()
