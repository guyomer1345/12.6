from data_classes import Client, Clients, Request, Message
from errors.errors import NicknameNotAllowed, NicknameUsed, HasNickname
from consts.consts import Permissions


def nickname_used(nickname: str, clients: Clients) -> bool:
    """
    Docstring

    return: True if name exists False otherwise
    """
    return any(client for client in \
         clients.clients if nickname == client.nickname)


def has_nickname(current_client: Client):
    """
    Docstring
    """
    if current_client.nickname:
        return True
    
    return False


def is_valid_nickname(nickname: str) -> bool:
    """
    Docstring
    """
    return nickname.isalnum() and nickname.upper() != 'SERVER'


def process_set_nickname(current_client: Client, \
        clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if has_nickname(current_client):
        raise HasNickname('Client already has nickname')
    
    nickname = request.nickname
    if not is_valid_nickname(nickname):
        raise NicknameNotAllowed('Client tried to use an invalid nickname')
    
    if nickname_used(nickname, clients):
        raise NicknameUsed('Client tried to use an existing nickname')
    
    current_client.nickname = nickname
    current_client.remove_permissions([Permissions.BASIC])
    current_client.add_permissions([Permissions.WRITE, Permissions.READ])
    if not clients.clients:  
        current_client.add_permissions([Permissions.MANAGER])

    message = Message('SERVER', '',\
             f'{current_client.nickname} has joined the chat!'.encode())
    clients.add_message_to_queue(clients.clients, message)