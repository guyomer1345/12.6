import logging
from consts.consts import Permissions
from data_classes import Client, Clients, Message, Request
from functions.functions import get_prefix
from errors.errors import BadPermissions


def process_private_message(current_client: Client, \
     clients: Clients, request: Request) -> None:
    """
    The function takes care of private message requests

    :rasise BadPermissions: If client doesn't have manager himself
    :param current_client: The client trying to promote
    :param clients: Clients object
    :request Request: The request the client is trying to make
    :return: None
    """
    if not Permissions.WRITE in current_client.permissions:
        raise BadPermissions(f'Client {current_client.nickname} ' + \
            'tried to write with bad permissions')
    
    data = request.args['data']  
    client_nickname = request.args['nickname']
    client = clients.get_by_nickname(client_nickname)
    
    prefix = get_prefix(current_client, request)
    message = Message(request.nickname, prefix, data)
    clients.add_message_to_queue([client, current_client], message)