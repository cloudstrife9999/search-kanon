from utils import send_utf8_string, read_utf8_string, parse_login_data
from socket import socket as s
from common import END_OF_DATA, ERROR
from db_manager import connect, search, MongoClient, Cursor, DATA_FIELD


def manage_client(client_socket: s) -> None:
    hash_prefix: str = read_utf8_string(endpoint=client_socket)
    mode: str = read_utf8_string(endpoint=client_socket)
    hash_suffixes: list[str] = __query_for_suffixes(hash_prefix=hash_prefix, mode=mode)

    for suffix in hash_suffixes:
        send_utf8_string(string=suffix, endpoint=client_socket)

    send_utf8_string(string=END_OF_DATA, endpoint=client_socket)
    client_socket.close()


def __query_for_suffixes(hash_prefix: str, mode: str) -> list[str]:
    print("Received '%s'.\nQuerying the '%s' collection for suffixes..." % (hash_prefix, mode))

    to_return: list[str] = __do_query_to_db(hash_prefix=hash_prefix, mode=mode)

    print("Returning the following suffixes:\n")
    print(to_return)
    print("\n")

    return to_return


def __do_query_to_db(hash_prefix: str, mode: str) -> list[str]:
    try:
        prefix_len: int = len(hash_prefix)
        to_return: list[str] = []

        user, password, auth_db = parse_login_data()
        mongo_client: MongoClient = connect(user=user, password=password, auth_db=auth_db)
        results: Cursor = search(mongo_client=mongo_client, prefix=hash_prefix, collection_name=mode)

        for result in results:
            to_return.append(result[DATA_FIELD][prefix_len:])

        results.close()
        mongo_client.close()

        return to_return
    except:
        return [ERROR]
