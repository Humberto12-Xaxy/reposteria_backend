from sqlalchemy import Table
from config.db import meta, engine

dessert = Table('dessert', meta, autoload_with= engine)