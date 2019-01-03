import os.path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from settings import (
    BASE_DIR,
    DOWNLOAD_DIR,
    TEMP_DIR,
    HEADLESS
)

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference(
    'browser.helperApps.neverAsk.saveToDisk',
    'application/zip'
)

temp_dir = os.path.join(BASE_DIR, TEMP_DIR)
download_dir = os.path.join(BASE_DIR, DOWNLOAD_DIR)
profile.set_preference('browser.download.dir', temp_dir)


options = Options()
options.set_headless(True)
