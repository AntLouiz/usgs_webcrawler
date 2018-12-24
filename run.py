import os.path
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options


def make_login(driver, credentials):
    input_username = driver.find_element_by_xpath("//input[@id='username']")
    input_username.send_keys(credentials['username'])

    input_password = driver.find_element_by_xpath("//input[@id='password']")
    input_password.send_keys(credentials['password'])

    driver.find_element_by_xpath("//input[@id='loginButton']").click()

    driver.implicitly_wait(10)


def download_image(driver):
    driver.find_element_by_xpath(
        "(//td[@class='resultRowContent']//a[@class='download'])[1]"
    ).click()


"""
Coordenadas de Parnaíba:
"""
coordinates = {
    'lat': -2.9055,
    'long': -41.7734
}

credentials = {
    'username': '****',
    'password': '****'
}

url = 'https://earthexplorer.usgs.gov/'
base_dir = os.path.abspath('./')
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')
profile.set_preference('browser.download.dir', base_dir)

options = Options()
options.set_headless(True)

driver = webdriver.Firefox(firefox_profile=profile, options=options)

response = driver.get(url)
coordinate_button = driver.find_element_by_xpath("//div[@id='lat_lon_section']/label[2]")
coordinate_button.click()


driver.find_element_by_xpath(
    "//input[@id='coordEntryAdd']"
).click()

input_lat = driver.find_element_by_xpath(
    "//div[@aria-describedby='coordEntryDialogArea']//input[@class='latitude txtbox decimalBox']"
)

input_long = driver.find_element_by_xpath(
    "//div[@aria-describedby='coordEntryDialogArea']//input[@class='longitude txtbox decimalBox']"
)

driver.implicitly_wait(2)

input_lat.send_keys(
    str(coordinates['lat'])
)

input_long.send_keys(
    str(coordinates['long'])
)

driver.find_element_by_xpath(
    "//div[@id='coordEntryDialogArea']/..//span[text()='Add']"
).click()

driver.implicitly_wait(2)

driver.find_element_by_xpath(
    "//input[@value='Data Sets »']"
).click()

driver.implicitly_wait(5)

driver.find_element_by_xpath("//li[@id='cat_210']/div").click()

driver.find_element_by_xpath(
    "//span[@title='Landsat Collection 1 Standard Level-1 Scene Products']"
).click()

driver.find_element_by_xpath(
    "//input[@id='coll_12864']"
).click()

driver.find_element_by_xpath(
    "//form[@name='dataSetForm']//input[@value='Results »']"
).click()

download_image(driver)

login_button = driver.find_element_by_xpath("//input[@value='Login']")

if login_button:
    login_button.click()

    driver.implicitly_wait(10)

    make_login(driver, credentials)
    download_image(driver)


download_button = driver.find_element_by_xpath(
    "//input[@value='Download'][1]"
)

download_button.click()
