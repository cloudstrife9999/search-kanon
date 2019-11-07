#!/usr/bin/env python3


import random
from hashlib import sha256
from db_manager import connect, init_db, MongoClient


NUMBER_OF_ENTRIES:  int = 1000000


def main() -> None:
    try:
        mongo_client: MongoClient = connect()
        init_db(mongo_client=mongo_client, number_of_entries=NUMBER_OF_ENTRIES)
        mongo_client.close()
    except:
        print("Failed to generate the test database.")


if __name__ == "__main__":
    main()
