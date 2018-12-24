from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from settings import BASE_DIR as base_dir

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')
profile.set_preference('browser.download.dir', base_dir)

options = Options()
options.set_headless(True)

client = webdriver.Firefox(firefox_profile=profile, options=options)
