# Ensuring that there's always a table in the database that corresponds to our defined models
# This code checks if all the models defined in models.py have corresponding tables that exist in the database
# else, SQLAlchemy creates them by default

from . import models, database

models.Base.metadata.create_all(bind=database.engine)
