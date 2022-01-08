import logging
import queue
from data_classes import Clients

def writeable_processor(clients: Clients) -> None:
    """
    This functions goes over all the writeable sockets
    and sends them the messages in their queue

    :param: Clients object
    :return: None
    """
    for client in clients.clients:
        try:
            messages_left = True
            while messages_left:
                message = client.message_queue.get(False)
                logging.debug(f'Client {client} has message {message}')
                data = message.build()
                sock = client.sock
                sock.send(data)

        except queue.Empty:
            messages_left = False