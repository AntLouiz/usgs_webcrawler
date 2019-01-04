import glob
import time
import os.path
from datetime import datetime
from settings import BASE_URL as base_url
from settings import USGS_PASSWORD as password
from settings import USGS_USERNAME as username
from settings import TEMP_DIR
from selenium import webdriver
from config import profile, options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from unzipper import clean_file
from exceptions import TimeoutError, WebCrawlerError, ResultsNotFoundError
from config import download_dir, temp_dir


def make_login(client, credentials):
    input_username = client.find_element_by_xpath("//input[@id='username']")
    input_username.send_keys(credentials['username'])

    input_password = client.find_element_by_xpath("//input[@id='password']")
    input_password.send_keys(credentials['password'])

    client.find_element_by_xpath("//input[@id='loginButton']").click()

    client.implicitly_wait(10)


def download_image(client):

    try:
        client.find_element_by_xpath(
            "(//td[@class='resultRowContent']//a[@class='download'])[1]"
        ).click()

    except NoSuchElementException:
        raise ResultsNotFoundError('No results found.')


def check_zip_download_finished(download_dir):
    waiting_seconds = 0
    download_finished = False

    time.sleep(waiting_seconds)

    while not download_finished:
        time.sleep(1)
        try:
            glob.glob("{}*.zip.part".format(download_dir))[0]
            download_finished = False

        except IndexError:
            download_finished = True

    if not download_finished:
        raise TimeoutError('The download is not finished.')

    time.sleep(waiting_seconds)

    return download_finished


def crawl():

    # Coordenadas de Parnaíba:
    coordinates = {
        'lat': -2.9055,
        'long': -41.7734
    }

    credentials = {
        'username': username,
        'password': password
    }

    client = webdriver.Firefox(firefox_profile=profile, options=options)

    response = client.get(base_url)

    wait(client, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[9]/div[1]/button"))).click()

    coordinate_button = client.find_element_by_xpath("//div[@id='lat_lon_section']/label[2]")
    coordinate_button.click()


    client.find_element_by_xpath(
        "//input[@id='coordEntryAdd']"
    ).click()

    input_lat = client.find_element_by_xpath(
        "//div[@aria-describedby='coordEntryDialogArea']//input[@class='latitude txtbox decimalBox']"
    )

    input_long = client.find_element_by_xpath(
        "//div[@aria-describedby='coordEntryDialogArea']//input[@class='longitude txtbox decimalBox']"
    )

    client.implicitly_wait(2)

    input_lat.send_keys(
        str(coordinates['lat'])
    )

    input_long.send_keys(
        str(coordinates['long'])
    )

    client.find_element_by_xpath(
        "//div[@id='coordEntryDialogArea']/..//span[text()='Add']"
    ).click()

    client.implicitly_wait(2)

    client.find_element_by_xpath(
        "//input[@value='Data Sets »']"
    ).click()

    client.implicitly_wait(5)

    client.find_element_by_xpath("//li[@id='cat_210']/div").click()

    client.find_element_by_xpath(
        "//span[@title='Landsat Collection 1 Standard Level-1 Scene Products']"
    ).click()

    client.find_element_by_xpath(
        "//input[@id='coll_12864']"
    ).click()

    client.find_element_by_xpath(
        "//form[@name='dataSetForm']//input[@value='Results »']"
    ).click()

    download_image(client)

    login_button = client.find_element_by_xpath("//input[@value='Login']")

    if login_button:
        login_button.click()

        client.implicitly_wait(10)

        make_login(client, credentials)
        download_image(client)

    download_button = client.find_element_by_xpath(
        "//*[@id='optionsPage']/div[1]/div[4]/input"
    )

    download_button.click()


def get_landsat_image():
    try:
        crawl()
        try:
            check_zip_download_finished(temp_dir)

            downloaded_file = glob.glob("./{}*.zip".format(TEMP_DIR))[0]

            download_file_path = os.path.join(
                download_dir,
                str(datetime.now())
            )

            clean_file(
                downloaded_file,
                download_file_path
            )

        except TimeoutError:
            print("Timeout error on the image download.")

    except WebCrawlerError:
        print("WebCrawler Error")


if __name__ == '__main__':
    get_landsat_image()
