#!/usr/bin/env python3


import socket
import client_manager

from common import HOST, PORT


def __loop(server_socket: socket.socket) -> None:
    while True:
        server_socket.listen()
        conn, _ = server_socket.accept()
        client_manager.manage_client(client_socket=conn)


def main() -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))

            print("Server started.\n")

            try:
                __loop(server_socket=s)
            except KeyboardInterrupt:
                print("\nServer stopped.\nBye!")
    except Exception as e:
        print("\nThe server just crashed due to an uncatched %s. Bye!" % e)


if __name__ == "__main__":
    main()
