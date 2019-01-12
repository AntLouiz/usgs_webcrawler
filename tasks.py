import json
import glob
from celery import Celery
from spider import get_landsat_image
from uploader import get_shapefile
from settings import TEMP_DIR, BROKER_URL as broker_url
from config import logger
from queries import (
    get_scraping_orders,
    update_scraping_order
)

app = Celery('tasks', broker=broker_url)

app.conf.update(
    result_expires=3600,
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        300.0,
        watch_new_coordinates,
        name='Scrapping Orders'
    )


@app.task
def watch_new_coordinates():
    orders = get_scraping_orders()

    if len(orders):
        for order in orders:
            print(order)
            get_shapefile(
                order['shapefile_key']
            )

            shapefile_path = glob.glob("./{}*.shp".format(TEMP_DIR))[0]

            get_landsat_image(
                order,
                shapefile_path
            )

            update_scraping_order(order['id'], status='finished')
    else:
        print("No orders founded.")
