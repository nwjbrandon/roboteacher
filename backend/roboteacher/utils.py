import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from roboteacher.constants import DB_HOSTNAME, DB_NAME, DB_PASSWORD, DB_USERNAME


def create_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def create_mongodb_connection():
    db_uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/?retryWrites=true&w=majority"
    client = MongoClient(db_uri, server_api=ServerApi("1"))
    db_conn = client[DB_NAME]
    return db_conn
