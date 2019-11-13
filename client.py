#!/usr/bin/env python3


import socket

from socket import socket
from utils import send_utf8_string, read_utf8_string
from common import HOST, PORT, PREFIX_LEN, END_OF_DATA, ERROR, SHA1_SEARCH_MODE, SHA256_SEARCH_MODE, STR_ENCODING
from argparse import ArgumentParser, Namespace
from hashlib import sha1, sha256


def __parse_arguments() -> tuple:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-s", "--string-to-search", type=str, required=True, metavar="string_to_search", help="The string to search")
    parser.add_argument("-m", "--mode", type=str, required=True, metavar="mode", help="Mode: '{}', or '{}' (without quotes)".format(SHA1_SEARCH_MODE, SHA256_SEARCH_MODE))

    args: Namespace = parser.parse_args()

    return args.string_to_search, args.mode


def __generate_search_material(to_search: str, mode: str) -> tuple:
    if mode == SHA1_SEARCH_MODE:
        reference: str = sha1(bytes(to_search, STR_ENCODING)).hexdigest()

        return reference, reference[:PREFIX_LEN]
    elif mode == SHA256_SEARCH_MODE:
        reference: str = sha256(bytes(to_search, STR_ENCODING)).hexdigest()

        return reference, reference[:PREFIX_LEN]
    else:
        raise ValueError("We only support '{}', and '{}' (without quotes) as search modes.".format(SHA1_SEARCH_MODE, SHA256_SEARCH_MODE))


def __do_search(prefix: str, mode: str) -> list:
    with socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, PORT))
        send_utf8_string(string=prefix, endpoint=server_socket)
        send_utf8_string(string=mode, endpoint=server_socket)

        return __receive_data(endpoint=server_socket)


def __receive_data(endpoint: socket) -> list:
    received: list[str] = []

    while True:
        tmp: str = read_utf8_string(endpoint=endpoint)

        if tmp == ERROR:
            raise IOError("There was a fatal error server side.")
        elif tmp == END_OF_DATA:
            break
        else:
            received.append(tmp)

    return received


def __check_for_match(prefix: str, suffixes: list, reference: str) -> str:
    for suffix in suffixes:
        if reference == prefix + suffix:
            return suffix

    return None


def __print_results(to_search: str, prefix: str, suffix: str, reference: str) -> None:
    if suffix is not None:
        print("SUCCESS: '%s' was found on the server!\n" % to_search)
        print("Prefix:    %s" % prefix)
        print("Suffix:    %s%s" % (' '*PREFIX_LEN, suffix))
        print("Reference: %s" % reference)
    else:
        print("FAILURE: '%s' was not found on the server." % to_search)


def __attempt_search(to_search: str, prefix: str, reference: str, mode: str) -> None:
    try:
        received: list[str] = __do_search(prefix=prefix, mode=mode)

        print("Received the following suffixes from the server:\n")
        print(received)
        print()

        suffix: str = __check_for_match(prefix=prefix, suffixes=received, reference=reference)

        __print_results(to_search=to_search, prefix=prefix, suffix=suffix, reference=reference)
    except ConnectionRefusedError:
        print("The server is unavailable at the moment. Try later.")
    except IOError as e:
        print(str(e))


def main() -> None:
    to_search, mode = __parse_arguments()
    reference, prefix = __generate_search_material(to_search=to_search, mode=mode)

    print("Searching for '%s'" % to_search)
    print("The reference value (%s) is '%s'" % (mode, reference))
    print("Sending the prefix '%s' to the server...\n" % prefix)


    __attempt_search(to_search=to_search, prefix=prefix, reference=reference, mode=mode)


if __name__ == "__main__":
    main()
