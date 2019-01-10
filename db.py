from sqlalchemy import create_engine
from settings import DB_URL as db_url


engine = create_engine(db_url)
conn = engine.connect()
