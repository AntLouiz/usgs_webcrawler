from sqlalchemy import select, MetaData, Table
from db import conn, engine


def get_scraping_orders():
    metadata = MetaData(bind=None)
    scrapingorder_table = Table(
        'core_scrapingorder',
        metadata,
        autoload=True,
        autoload_with=engine
    )

    query_select = select(
        [scrapingorder_table]
    )

    result = conn.execute(query_select)

    return result
