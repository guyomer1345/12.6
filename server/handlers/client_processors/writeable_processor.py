import logging
import queue
from data_classes import Clients

def writeable_processor(clients: Clients) -> None:
    """
    Add docstring
    """
    for client in clients.clients:
        try:
            message = client.message_queue.get(False)
            logging.debug(f'Client {client} has message {message}')
            data = message.build()
            sock = client.sock
            sock.send(data)

        except queue.Empty:
            pass
        except Exception as e:
            logging.debug(f'QUEUE DEAD {e}') #TODO change