from sqlalchemy import Table
from config.db import meta, engine

ingredients_dessert = Table('ingredients_dessert', meta, autoload_with= engine)