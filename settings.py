import os.path
from decouple import config

USGS_USERNAME = config('USGS_USERNAME')
USGS_PASSWORD = config('USGS_PASSWORD')
BASE_URL = 'https://earthexplorer.usgs.gov/'
BASE_DIR = os.path.abspath('./')
HEADLESS = config('HEADLESS', default=True)
