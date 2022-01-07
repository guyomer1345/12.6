import socket
import logging
from typing import List
from data_classes import Clients, Client, Message, Request
from consts.consts import Permissions, Commands
from errors.errors import SocketNotExist


def get_prefix(client: Client, request: Request) -> str:
    """
    Docstring
    """
    prefix = ''
    if Permissions.manager in client.permissions:
        prefix = '@' 
    
    if request.cmd == Commands.private_message:
        prefix = '!'
    
    return prefix


def add_message_to_queue(clients: List[Client], message: Message) -> None:
    """
    Docstring
    """
    for client in clients:
        if Permissions.read in client.permissions: 
            client.message_queue.put(message)


def end_connection(client: Client, clients: Clients,\
                         alert_clients: bool) -> None: 
    """
    Add docstring
    """
    sock = client.sock
    ip = sock.getsockname()[0]
    clients.remove_client(sock)
    sock.close()
    if not client.nickname:
        client.nickname = 'No nickname'
        
    if alert_clients:
        message = Message('SERVER', '',\
             f'{client.nickname} has left the chat!'.encode())
        add_message_to_queue(clients.clients, message)

    logging.info(f'Closed the connection with {ip}')


def accept_client(server: socket.socket, clients: Clients) -> None:
    """
    Add docstring
    """
    sock, addr = server.accept()
    sock.settimeout(5)
    logging.info(f'Accepted client at {addr}')
    client = Client(sock)
    client.add_permissions([Permissions.send])
    clients.clients.append(client)