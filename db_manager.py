from pymongo import MongoClient
from pymongo.cursor import Cursor
from bson.regex import Regex
from hashlib import sha256, sha1
from string import ascii_letters as letters
from random import choice
from common import PLAIN_COLLECTION_NAME, SHA1_COLLECTION_NAME, SHA256_COLLECTION_NAME


DB_HOSTNAME: str = "127.0.0.1"
DB_PORT: int = 27017
DB_NAME: str = "kanon"
DATA_FIELD: str = "data"
RANDOM_WORDS_LENGTH: int = 20


def connect() -> MongoClient:
    try:
        return MongoClient(host=DB_HOSTNAME, port=DB_PORT)
    except:
        raise IOError("Failed to connect to the DB.")


def init_db(mongo_client: MongoClient, number_of_plain_entries: int, number_of_sha1_entries: int, number_of_sha256_entries: int) -> None:
    if number_of_plain_entries <= 0 or number_of_sha1_entries <= 0 or number_of_sha256_entries <= 0:
        raise ValueError("You have to insert at least an entry for each category.")
    elif mongo_client is None:
        raise ValueError("Failed to connect to the DB.")
    else:
        __init_collections(mongo_client=mongo_client, number_of_plain_entries=number_of_plain_entries, number_of_sha1_entries=number_of_sha1_entries, number_of_sha256_entries=number_of_sha256_entries)
    

def __init_collections(mongo_client: MongoClient, number_of_plain_entries: int, number_of_sha1_entries: int, number_of_sha256_entries: int) -> None:
    if mongo_client is None:
        raise IOError("Failed to connect to the DB.")
    
    if not has_collection(mongo_client=mongo_client, collection_name=PLAIN_COLLECTION_NAME):
        for _ in range(number_of_sha1_entries):
            mongo_client[DB_NAME][PLAIN_COLLECTION_NAME].insert_one({DATA_FIELD: ''.join(choice(letters) for _ in range(RANDOM_WORDS_LENGTH))})

        print("The plain collection has been initialised.")
    else:
        print("The plain collection was already initialised.")

    if not has_collection(mongo_client=mongo_client, collection_name=SHA1_COLLECTION_NAME):
        for i in range(number_of_sha1_entries):
            mongo_client[DB_NAME][SHA1_COLLECTION_NAME].insert_one({DATA_FIELD: sha1(bytes(str(i), "utf-8")).hexdigest()})

        print("The sha1 collection has been initialised.")
    else:
        print("The sha1 collection was already initialised.")

    if not has_collection(mongo_client=mongo_client, collection_name=SHA256_COLLECTION_NAME):
        for i in range(number_of_sha256_entries):
            mongo_client[DB_NAME][SHA256_COLLECTION_NAME].insert_one({DATA_FIELD: sha256(bytes(str(i), "utf-8")).hexdigest()})

        print("The sha256 collection has been initialised.")
    else:
        print("The sha256 collection was already initialised.")


def search(prefix: str, mongo_client: MongoClient, collection_name: str) -> Cursor:
    if mongo_client is not None:
        regex = Regex('^{}'.format(prefix))
        
        return mongo_client[DB_NAME][collection_name].find({"data": {"$regex" : regex}}, {DATA_FIELD: 1, "_id": 0})
    else:
        raise IOError("Failed to connect to the DB.")


def has_collection(mongo_client: MongoClient, collection_name: str) -> bool:
    if mongo_client is not None:
        return collection_name in mongo_client[DB_NAME].collection_names()
    else:
        raise IOError("Failed to connect to the DB.")