from pymongo import MongoClient
from pymongo.cursor import Cursor
from bson.regex import Regex
from hashlib import sha256


DB_HOSTNAME: str = "127.0.0.1"
DB_PORT: int = 27017
DB_NAME: str = "kanon"
COLLECTION_NAME: str = "sha256"
DATA_FIELD: str = "data"


def connect() -> MongoClient:
    try:
        return MongoClient(host=DB_HOSTNAME, port=DB_PORT)
    except:
        raise IOError("Failed to connect to the DB.")


def init_db(mongo_client: MongoClient, number_of_entries: int) -> None:
    if number_of_entries <= 0:
        raise ValueError("You have to insert at least an entry.")
    elif mongo_client is None:
        raise ValueError("Failed to connect to the DB.")
    elif not has_collection(mongo_client=mongo_client):
        for i in range(number_of_entries):
            mongo_client[DB_NAME][COLLECTION_NAME].insert_one({DATA_FIELD: sha256(bytes(str(i), "utf-8")).hexdigest()})

        print("The database has been initialised.")
    else:
        print("The database was already initialised.")
    

def search(prefix: str, mongo_client: MongoClient) -> Cursor:
    if mongo_client is not None:
        regex = Regex('^{}'.format(prefix))
        
        return mongo_client[DB_NAME][COLLECTION_NAME].find({"data": {"$regex" : regex}}, {DATA_FIELD: 1, "_id": 0})
    else:
        raise IOError("Failed to connect to the DB.")


def has_collection(mongo_client: MongoClient) -> bool:
    return COLLECTION_NAME in mongo_client[DB_NAME].collection_names()