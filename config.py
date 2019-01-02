import os.path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from settings import BASE_DIR as base_dir
from settings import HEADLESS

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

download_dir = os.path.join(base_dir, 'downloads/')
profile.set_preference('browser.download.dir', download_dir)


options = Options()
options.set_headless(True)

client = webdriver.Firefox(firefox_profile=profile, options=options)
