import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helper import (check_previous_file,compare_filenames,write_to_file,
    wait_for_download,move_file_to_sorted_dir)

# Setup download path
download_dir = os.path.join(os.getcwd(), 'temp')
os.makedirs(download_dir, exist_ok=True)

# Configure Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-features=CloudPolicy")
options.add_argument("--disable-features=PushMessaging")
options.add_argument("--disable-background-networking")

options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    },
)

driver = webdriver.Chrome(options=options)
driver.get("https://nepalstock.com/today-price")

# Wait for the download link to be clickable
wait = WebDriverWait(driver, 30)
time.sleep(20)

download_link = driver.find_element(By.CLASS_NAME, "table__file")

# Click to trigger download
download_link.click()

downloaded_filename = wait_for_download(download_dir, timeout=60)
driver.quit()

if downloaded_filename:
    print("Downloaded file:", downloaded_filename)
    # Compare with previous, and update if new
    if not compare_filenames(downloaded_filename):
        print("New file detected.")
        write_to_file(downloaded_filename)
        move_file_to_sorted_dir(download_dir, downloaded_filename)
    else:
        print("File is same as previous.")
else:
    print("Download failed or timed out.")
