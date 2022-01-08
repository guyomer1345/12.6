import socket
import logging
from typing import List
from data_classes import Clients, Client, Message, Request
from consts.consts import Permissions, Commands


def get_prefix(client: Client, request: Request) -> str:
    """
    This function returns the matching prefix for the message

    :param client: A client object
    :param request: A request object
    :return: The prefix
    """
    prefix = ''
    if Permissions.MANAGER in client.permissions:
        prefix = '@' 
    
    if request.cmd == Commands.PRIVATE_MESSAGE:
        prefix = '!'
    
    return prefix


def end_connection(client: Client, clients: Clients,\
                         alert_clients: bool) -> None: 
    """
    This functions ends the connection with a client
    and notifys the other clients
    
    :param client: A client object
    :param clients: Clients object
    :param alert_clients: Whether to alert the other clients or noot
    :return: None
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
        clients.add_message_to_queue(clients.clients, message)

    logging.info(f'Closed the connection with {ip}')


def accept_client(server: socket.socket, clients: Clients) -> None:
    """
    This function is wrapping function for socket's accept
    and adds the socket to the clients object

    :param server: The server accepting the socket
    :param clients: Clients object
    :return None:
    """
    sock, addr = server.accept()
    sock.settimeout(5)
    logging.info(f'Accepted client at {addr}')
    client = Client(sock)
    client.add_permissions([Permissions.BASIC])
    clients.clients.append(client)