import json
import glob
from celery import Celery
from spider import get_landsat_image
from uploader import get_shapefile
from settings import TEMP_DIR
from config import temp_dir


broker_url = 'amqp://antlouiz:luiz05012016@127.0.0.1:5672/watcher'
app = Celery('tasks', broker=broker_url)

app.conf.update(
    result_expires=3600,
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        500.0,
        watch_new_coordinates,
        name='Scrapping after 2 seconds'
    )


@app.task
def watch_new_coordinates():
    with open('coordinates.json', 'r') as coordinates:
        coordinates = json.load(coordinates)
        for coord in coordinates:
            if not coordinates[coord]['scrapped']:
                user_id = coordinates[coord]['user_id']
                get_shapefile(
                    user_id
                )

                shapefile_path = glob.glob("./{}*.shp".format(TEMP_DIR))[0]

                get_landsat_image(
                    coordinates[coord]['lat'],
                    coordinates[coord]['long'],
                    shapefile_path
                )

                coordinates[coord]['scrapped'] = True

                with open('coordinates.json', 'w') as new_coord:
                    json.dump(coordinates, new_coord)

                break
