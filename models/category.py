from sqlalchemy import Table
from config.db import meta, engine

category = Table('category', meta, autoload_with= engine)