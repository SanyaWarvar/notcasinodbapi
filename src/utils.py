from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from database import DATABASE_URL


def validate_database():
    engine = create_engine(DATABASE_URL)
    if not database_exists(engine.url):  # Checks for the first time
        create_database(engine.url)  # Create new DB
        print("New Database Created" + database_exists(engine.url))  # Verifies if database is there or not.
    else:
        print("Database Already Exists")
