import logging
import socket
import sys
from data_classes import Client, Screen


def process_readable(client: Client, screen: Screen) -> None:
    """
    Docstring
    """
    try:
        sock = client.sock
        amount = int(sock.recv(9))
        data = b''
        while len(data) != amount:
            data += sock.recv(amount - len(data))
        
        screen.messages_queue.put(data.decode())

    except (socket.error, ValueError):
        client.sock.close()
        logging.info('Shutting down')
        sys.exit()
