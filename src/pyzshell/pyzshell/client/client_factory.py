import logging
from socket import socket

from pyzshell.client.client import Client
from pyzshell.client.darwin_client import DarwinClient
from pyzshell.protocol import UNAME_VERSION_LEN


def recvall(sock, size: int) -> bytes:
    buf = b''
    while size:
        try:
            chunk = sock.recv(size)
        except BlockingIOError:
            continue
        size -= len(chunk)
        buf += chunk
    return buf


def create_client(hostname: str, port: int = None):
    sock = socket()
    sock.connect((hostname, port))
    uname_version = recvall(sock, UNAME_VERSION_LEN).decode()
    logging.info(f'connected system uname.version: {uname_version}')
    os_flavor = uname_version.split()[0].lower()

    if os_flavor == 'darwin':
        return DarwinClient(sock, uname_version, hostname, port)

    return Client(sock, uname_version, hostname, port)
