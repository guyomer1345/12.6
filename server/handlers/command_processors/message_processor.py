from typing import Tuple, List
from consts.consts import Permissions
from data_classes import Client, Clients, Message, Request
from functions.functions import get_prefix, end_connection
from errors.errors import BadPermissions


def process_view_managers(current_client: Client, \
                            clients: Clients) -> Tuple[Message, List[Client]]:
    """
    Docstring
    """
    message = Message('SERVER', '' , clients.view_managers().encode())
    clients_to_send = [current_client]

    return message, clients_to_send


special_cases = {
    b'/view-managers': process_view_managers
}


def process_message(current_client: Client, \
     clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if not Permissions.WRITE in current_client.permissions:
        raise BadPermissions(f'Client {current_client.nickname} ' + \
            'tried to write with bad permissions')
    
    data = request.args['data']
    if data == b'/quit':
        end_connection(current_client, clients, True)
        return None

    clients_to_send = clients.clients
    prefix = get_prefix(current_client, request)
    message = Message(request.nickname, prefix, data)
    if data in special_cases.keys():
        message, clients_to_send = special_cases[data](current_client, clients)

    clients.add_message_to_queue(clients_to_send, message)