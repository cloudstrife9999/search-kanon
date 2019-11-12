#!/usr/bin/env python3


import random
from hashlib import sha256
from db_manager import connect, init_db, MongoClient
from utils import parse_login_data


NUMBER_OF_PLAIN_ENTRIES:  int = 1000000
NUMBER_OF_SHA1_ENTRIES:  int = 1000000
NUMBER_OF_SHA256_ENTRIES:  int = 1000000


def main() -> None:
    try:
        user, password, auth_db = parse_login_data()
        mongo_client: MongoClient = connect(user=user, password=password, auth_db=auth_db)
        init_db(mongo_client=mongo_client, number_of_plain_entries=NUMBER_OF_PLAIN_ENTRIES, number_of_sha1_entries=NUMBER_OF_SHA1_ENTRIES, number_of_sha256_entries=NUMBER_OF_SHA256_ENTRIES)
        mongo_client.close()
    except:
        print("Failed to generate the test database.")


if __name__ == "__main__":
    main()
