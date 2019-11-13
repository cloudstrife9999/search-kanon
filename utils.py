from socket import socket
from common import DB_AUTH_FILE, BYTE_ORDER, USER_JSON_KEY, PWD_JSON_KEY, AUTH_DB_JSON_KEY, STR_ENCODING
from json import load


INT_LENGTH_IN_BYTES: int = 4


def send_utf8_string(string: str, endpoint: socket) -> None:
    length: int = len(string)

    if length > 2**(INT_LENGTH_IN_BYTES * 8) - 1:
        raise ValueError("We currently cannot send strings longer than (2**%d - 1) bytes." % INT_LENGTH_IN_BYTES * 8)

    encoded_length: bytes = (length).to_bytes(INT_LENGTH_IN_BYTES, byteorder=BYTE_ORDER)

    endpoint.send(encoded_length)
    endpoint.send(bytes(string, STR_ENCODING))


def read_utf8_string(endpoint: socket) -> str:
    encoded_length: bytes = endpoint.recv(INT_LENGTH_IN_BYTES)
    length: int = int.from_bytes(bytes=encoded_length, byteorder=BYTE_ORDER)

    if length < 0:
        raise ValueError("The length of the string to read cannot be negative.")

    return str(endpoint.recv(length), STR_ENCODING)


def parse_login_data() -> tuple:
    with open(DB_AUTH_FILE, "r") as f:
        data: Any = load(fp=f)

        return data[USER_JSON_KEY], data[PWD_JSON_KEY], data[AUTH_DB_JSON_KEY]
