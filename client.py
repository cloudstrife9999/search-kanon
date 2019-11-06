#!/usr/bin/env python3


import socket

from socket import socket as s
from utils import send_utf8_string, read_utf8_string
from common import HOST, PORT, PREFIX_LEN, END_OF_DATA
from argparse import ArgumentParser, Namespace
from hashlib import sha1, sha256


def __parse_arguments() -> tuple:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-s", "--string-to-search", type=str, required=True, metavar="string_to_search", help="The string to search")
    parser.add_argument("-m", "--mode", type=str, required=True, metavar="mode", help="Mode: 'plain', 'sha1', or 'sha256' (without quotes)")

    args: Namespace = parser.parse_args()

    return args.string_to_search, args.mode


def __generate_search_material(to_search: str, mode: str) -> tuple:
    if mode == "plain" and len(to_search) <= 5:
        raise ValueError("We only support searching for strings longer than %d characters for plain search mode." % PREFIX_LEN)
    elif mode == "plain":
        return to_search, to_search[:PREFIX_LEN]
    elif mode == "sha1":
        reference: str = sha1(bytes(to_search, "utf-8")).hexdigest()

        return reference, reference[:PREFIX_LEN]
    elif mode == "sha256":
        reference: str = sha256(bytes(to_search, "utf-8")).hexdigest()

        return reference, reference[:PREFIX_LEN]
    else:
        raise ValueError("We only support 'plain', 'sha1', and 'sha256' (without quotes) as search modes.")


def __do_search(prefix: str) -> list:
    with s(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, PORT))
        send_utf8_string(string=prefix, endpoint=server_socket)

        received: list = []

        while True:
            tmp: str = read_utf8_string(endpoint=server_socket)

            if tmp == END_OF_DATA:
                break
            else:
                received.append(tmp)

        server_socket.close()

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


def main() -> None:
    to_search, mode = __parse_arguments()
    reference, prefix = __generate_search_material(to_search=to_search, mode=mode)

    print("Searching for '%s'" % to_search)
    print("The reference value (plain or hash, depending on the mode) is '%s'" % reference)
    print("Sending the prefix '%s' to the server...\n" % prefix)

    received: list = __do_search(prefix=prefix)

    print("Received the following suffixes from the server:")
    print(received)
    print()

    suffix: str = __check_for_match(prefix=prefix, suffixes=received, reference=reference)

    __print_results(to_search=to_search, prefix=prefix, suffix=suffix, reference=reference)


if __name__ == "__main__":
    main()
