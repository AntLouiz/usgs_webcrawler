import os.path
from decouple import config

USGS_USERNAME = config('USGS_USERNAME')
USGS_PASSWORD = config('USGS_PASSWORD')
BASE_URL = 'https://earthexplorer.usgs.gov/'
BASE_DIR = os.path.abspath('./')
HEADLESS = config('HEADLESS', default=True)
TEMP_DIR = '_temp/'
DOWNLOAD_DIR = config(
    'DOWNLOAD_DIR',
    default='downloads/'
)

DB_URL = config(
    'DATABASE_URL',
    default='sqlite:///{}'.format(
        os.path.join(BASE_DIR, 'db.sqlite3')
    )
)

BROKER_URL = config(
    'BROKER_URL'
)
