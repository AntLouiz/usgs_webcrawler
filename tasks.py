import glob
import os.path
from config import temp_dir
from celery import Celery
from celery.utils.log import get_task_logger
from spider import execute_scraping_order
from uploader import get_shapefile
from settings import TEMP_DIR, BROKER_URL as broker_url
from queries import (
    get_scraping_orders,
    update_scraping_order
)

app = Celery('tasks', broker=broker_url)
logger = get_task_logger(__name__)

@app.task
def crawl_order(order):
    logger.info(order)
    get_shapefile(
        order['shapefile_key']
    )

    shapefile_dir = os.path.join(temp_dir, order['shapefile_key'])
    shapefile_path = glob.glob("{}/*.shp".format(shapefile_dir))[0]
    execute_scraping_order(
        order,
        shapefile_path
    )

    update_scraping_order(order['id'], status='finished')

