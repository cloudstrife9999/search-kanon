from socket import socket as s


length_of_an_int: int = 4


def send_utf8_string(string: str, endpoint: s) -> None:
    length: int = len(string)

    if length > 2**32 - 1:
        raise ValueError("We currently cannot send strings longer than (2**32 - 1) bytes.")

    encoded_length: bytes = (length).to_bytes(length_of_an_int, byteorder="big")

    endpoint.send(encoded_length)
    endpoint.send(bytes(string, "utf-8"))


def read_utf8_string(endpoint: s) -> str:
    encoded_length: bytes = endpoint.recv(length_of_an_int)
    length: int = int.from_bytes(bytes=encoded_length, byteorder="big")

    if length < 0:
        raise ValueError("The length of the string to read cannot be negative.")

    return str(endpoint.recv(length), "utf-8")