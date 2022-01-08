from data_classes import Client, Clients, Request, Message
from errors.errors import NicknameNotAllowed, NicknameUsed, HasNickname
from consts.consts import Permissions


def nickname_used(nickname: str, clients: Clients) -> bool:
    """
    This function checks if the nickname already exists in other clients

    :param nickname: The nickname the client asked fort
    :param clients: Clients object 
    :return: True if name exists False otherwise
    """
    return any(client for client in \
         clients.clients if nickname == client.nickname)


def has_nickname(current_client: Client):
    """
    This function check if the client already has a name

    :param current_client: The client making the request
    :return: True if has name False otherwise
    """
    if current_client.nickname:
        return True
    
    return False


def is_valid_nickname(nickname: str) -> bool:
    """
    This functions checks if the nickname asked for was valid

    :param nickname: The nickname the client requested
    :return: True if name is valid False otherwise
    """
    return nickname.isalnum() and nickname.upper() != 'SERVER'


def process_set_nickname(current_client: Client, \
        clients: Clients, request: Request) -> None:
    """
    This function takes care of set nickname requests

    :raise HasNickname: If the client already has a nickname
    :raise NicknameNotAllowed: If the nickname asked for is not allowed
    :raise NicknameUsed: If the nickname asked for is already used
    :param current_client: The client trying to promote
    :param clients: Clients object
    :request Request: The request the client is trying to make
    :return: None
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
    if clients.clients == [current_client]: # If its the first client  
        current_client.add_permissions([Permissions.MANAGER])

    message = Message('SERVER', '',\
             f'{current_client.nickname} has joined the chat!'.encode())
    clients.add_message_to_queue(clients.clients, message)