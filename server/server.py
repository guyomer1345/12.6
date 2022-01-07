import socket
import select
import logging
from typing import List
from data_classes import Clients
from handlers.client_processors.readable_processor import process_readable #TODO init in client_processors
from handlers.client_processors.writeable_processor import writeable_processor
from consts.consts import IP, PORT, MAX_LISTEN, Permissions

logging.basicConfig(level=logging.DEBUG)
clients = Clients()


def create_server(ip: str ,port: int)  -> socket.socket:
    """
    Docstring
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(MAX_LISTEN)
    logging.info(f'Server is running on port {port}')

    return server


def get_clients(clients: Clients,\
                permissions: Permissions) -> List[socket.socket]:
    """
    Docstring
    """
    return[client.sock for client in \
        clients.clients if permissions in client.permissions]


def main():
    server = create_server(IP, PORT)
    while True: #TODO Change from True, empty names leaving server to no name
        send_clients = get_clients(clients, Permissions.send)
        read_clients = get_clients(clients, Permissions.read)
        write_clients = get_clients(clients, Permissions.write) 
        wlist = list(set(send_clients+read_clients+write_clients)) + [server]
        rlist = list(set(write_clients+read_clients))
        rlist, wlist, xlist = select.select(wlist, rlist, [])

        process_readable(rlist, server, clients)
        writeable_processor(clients)

    
if __name__ == '__main__':
    main()