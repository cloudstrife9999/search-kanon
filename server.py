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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))

        try:
            __loop(server_socket=s)
        except KeyboardInterrupt:
            print("\nBye!")
            s.close()


if __name__ == "__main__":
    main()
