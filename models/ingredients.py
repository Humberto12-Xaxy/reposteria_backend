from sqlalchemy import Table
from config.db import meta, engine

ingredients = Table('ingredients', meta, autoload_with= engine)