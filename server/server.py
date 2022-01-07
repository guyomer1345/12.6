import socket
import select
import logging
from typing import List
from data_classes import Clients
import handlers.client_processors as client_processors
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
    running = True
    try:
        while running:
            send_clients = get_clients(clients, Permissions.BASIC)
            read_clients = get_clients(clients, Permissions.WRITE)
            write_clients = get_clients(clients, Permissions.READ) 
            wlist = list(set(send_clients+read_clients+write_clients)) + [server]
            rlist = list(set(write_clients+read_clients))
            rlist, wlist, xlist = select.select(wlist, rlist, [])

            client_processors.process_readable(rlist, server, clients)
            client_processors.writeable_processor(clients)

    except KeyboardInterrupt:
        running = False
        logging.info('Server shutting down!')

    
if __name__ == '__main__':
    main()