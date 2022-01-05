import socket
import logging
from typing import List
from data_classes import Clients
from functions.functions import accept_client, end_connection
from errors.errors import ProtocolError, SocketNotExist
from handlers.dispatcher import dispatcher
from parsers.request_parser import request_parser


def process_readable(rlist: List[socket.socket], \
    server: socket.socket, clients: Clients) -> None:
    """
    Add docstring
    """
    try:
        for sock in rlist:
            if sock == server:
                accept_client(server, clients)
                continue
            
            current_client = Clients.get_by_sock(clients, sock)
            request = request_parser(sock) 
            dispatcher(request, current_client, clients)

    except (socket.error, socket.timeout, ProtocolError) as e:
        logging.info(e)
        end_connection(current_client, clients, True)

    except (SocketNotExist) as e:
        logging.info(e)