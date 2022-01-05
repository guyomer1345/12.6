from data_classes import Client, Clients, Request
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
    return nickname.isalnum()


def process_set_nickname(current_client: Client, \
        clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if has_nickname(current_client):
        raise HasNickname('Client already has nickname') # TODO disconnects
    
    nickname = request.nickname
    if not is_valid_nickname(nickname):
        raise NicknameNotAllowed('Client tried to use an invalid nickname') # TODO disconnect
    
    if nickname_used(nickname, clients):
        raise NicknameUsed('Client tried to use an existing nickname') # TODO disconnect
    
    current_client.nickname = nickname
    current_client.remove_permissions([Permissions.send])
    if nickname == 'amit':  
        current_client.add_permissions([Permissions.manager])

    current_client.add_permissions([Permissions.read, Permissions.write])
    #TODO add x joined the chat, handle quit, view-managers
    
    