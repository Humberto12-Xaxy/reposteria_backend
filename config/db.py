from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:193260@localhost:5432/desserts_table")
conn = engine.connect()
meta = MetaData()
Session = sessionmaker(bind= engine)
session = Session()