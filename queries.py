from datetime import datetime
from sqlalchemy import update, insert
from sqlalchemy import MetaData, Table
from db import conn, engine, session


def result_to_dict(keys, result):
    result_dict = dict(zip(keys, result))

    return result_dict


def get_scraping_orders():
    metadata = MetaData(bind=None)
    ScrapingOrder = Table(
        'core_scrapingorder',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    Coordinates = Table(
        'core_coordinates',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    Shapefiles = Table(
        'core_shapefile',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    query_fields = {
        'status': ScrapingOrder.c.status,
        'latitude': Coordinates.c.latitude,
        'longitude': Coordinates.c.longitude,
        'shapefile_key': Shapefiles.c.key,
        'id': ScrapingOrder.c.key
    }

    filter_fields = {
        'scrapping_coord_id': ScrapingOrder.c.coordinates_id,
        'coordinate_id': Coordinates.c.id,
        'coord_shape_id': Coordinates.c.shapefile_id,
        'shapefile_id': Shapefiles.c.id,
        'is_active': ScrapingOrder.c.is_active
    }

    query_results = session.query(
        *query_fields.values()
    ).filter(
        filter_fields['scrapping_coord_id'] == filter_fields['coordinate_id']
    ).filter(
        filter_fields['coord_shape_id'] == filter_fields['shapefile_id']
    ).filter(
        query_fields['status'] == 'waiting'
    ).filter(
        filter_fields['is_active'] == True
    ).all()

    results = []

    for result in query_results:
        results.append(
            result_to_dict(
                list(query_fields.keys()),
                result
            )
        )

    return results


def update_scraping_order(key, status='no_result'):
    metadata = MetaData(bind=None)
    scrapingorder_table = Table(
        'core_scrapingorder',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    query_update = update(
        scrapingorder_table
    ).where(
        scrapingorder_table.c.key == key
    ).values(
        status=status
    )

    conn.execute(query_update)


def insert_raster_to_order(raster_key, thumbnail_link, download_link, order_key):
    metadata = MetaData(bind=None)
    order_table = Table(
        'core_scrapingorder',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    raster_table = Table(
        'core_raster',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    insert_raster = insert(raster_table).values({
        'key': raster_key,
        'thumbnail_link': thumbnail_link,
        'download_link': download_link,
        'download_date': datetime.now(),
        'is_active': True
    })

    conn.execute(insert_raster)

    new_raster = session.query(raster_table).filter(
        raster_table.c.key == raster_key
    ).one()

    query_update = update(
        order_table
    ).where(
        order_table.c.key == order_key
    ).values(
        raster_id=new_raster[0]
    )

    conn.execute(query_update)
