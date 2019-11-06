from utils import send_utf8_string, read_utf8_string
from socket import socket as s
from common import END_OF_DATA


def manage_client(client_socket: s) -> None:
    hash_prefix: str = read_utf8_string(endpoint=client_socket)
    hash_suffixes: list[str] = __query_for_suffixes(hash_prefix=hash_prefix)

    for suffix in hash_suffixes:
        send_utf8_string(string=suffix, endpoint=client_socket)

    send_utf8_string(string=END_OF_DATA, endpoint=client_socket)
    client_socket.close()


def __query_for_suffixes(hash_prefix: str) -> list:
    print("Received '%s'.\nQuerying for suffixes..." % hash_prefix)

    to_return: list = __do_query(hash_prefix=hash_prefix)

    print("Returning the following suffixes:\n")
    print(to_return)
    print("\n")

    return to_return


def __do_query(hash_prefix: str) -> list:
    prefix_len: int = len(hash_prefix)
    to_return: list = []

    with open("test.txt", "r") as f:
        lines: list = [l.rstrip() for l in f.readlines()]

        for line in lines:
            if line.startswith(hash_prefix):
                to_return.append(line[prefix_len:])

    return to_return
