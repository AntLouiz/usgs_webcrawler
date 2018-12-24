import os.path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

base_dir = os.path.abspath('./')
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')
profile.set_preference('browser.download.dir', base_dir)

options = Options()
options.set_headless(True)

client = webdriver.Firefox(firefox_profile=profile, options=options)
