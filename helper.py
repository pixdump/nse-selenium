import os
import time
import shutil
from datetime import datetime

def check_previous_file():
    with open('prev.txt','r') as prev:
        text = prev.read().strip()
        return text


def write_to_file(content: str,filename='prev.txt') -> None:
    with open(file=filename,mode='w') as file:
        file.write(content.strip())


def compare_filenames(filename: str):
    previous_filename: str = check_previous_file()
    return filename == previous_filename



def wait_for_download(download_dir, timeout=30):
    """
    Waits for a new file to appear in the directory and returns its name.
    Assumes that the directory was empty or only contains known files.
    """
    seconds = 0
    downloaded_file = None
    while seconds < timeout:
        files = os.listdir(download_dir)
        # Skip temporary or partial files like .crdownload
        valid_files = [f for f in files if not f.endswith('.crdownload')]
        if valid_files:
            downloaded_file = valid_files[0]  # assuming only one file is downloaded
            break
        time.sleep(1)
        seconds += 1
    return downloaded_file


def move_file_to_sorted_dir(download_dir: str, filename: str, base_dir="data"):
    try:
        # Example: Today's Price - 2025-06-10.csv
        date_str = filename.split(" - ")[-1].replace(".csv", "").strip()
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Build new path: data/yyyy/mm/price_dd.csv
        year = str(date_obj.year)
        month = f"{date_obj.month:02}"
        day = f"{date_obj.day:02}"

        target_dir = os.path.join(base_dir, year, month)
        os.makedirs(target_dir, exist_ok=True)

        new_filename = f"price_{day}.csv"
        new_path = os.path.join(target_dir, new_filename)

        # Move the file
        shutil.move(os.path.join(download_dir, filename), new_path)
        print(f"Moved to: {new_path}")
        return new_path
    except Exception as e:
        print(f"Error while moving file: {e}")
        return None
