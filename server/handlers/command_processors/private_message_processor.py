import logging
from consts.consts import Permissions
from data_classes import Client, Clients, Message, Request
from functions.functions import add_message_to_queue, get_prefix
from errors.errors import BadPermissions


def process_private_message(current_client: Client, \
     clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if not Permissions.read in current_client.permissions: # Handle bad_premissions as add cant send to queue
        raise BadPermissions(f'Client {current_client.nickname} ' + \
            'tried to write with bad permissions')
    
    logging.debug(f'REQUEST IS {request}')
    data = request.args[1]['data']  #TODO change to a normal dict instead of whatever this is
    client_nickname = request.args[0]['nickname']
    client = clients.get_by_nickname(client_nickname)
    
    prefix = get_prefix(current_client, request)
    message = Message(request.nickname, prefix, data)
    add_message_to_queue([client, current_client], message)