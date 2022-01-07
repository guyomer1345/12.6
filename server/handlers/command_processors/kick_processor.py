from consts.consts import Permissions
from data_classes import Client, Clients, Message ,Request
from errors.errors import BadPermissions, CantKickYourself
from functions.functions import end_connection


def process_kick(current_client: Client, \
     clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if Permissions.MANAGER not in current_client.permissions:
        raise BadPermissions

    client_nickname = request.args['nickname']
    client = clients.get_by_nickname(client_nickname)

    if current_client == client:
        raise CantKickYourself(f'{request.nickname} tried to kick himself')
    
    message = Message('server', '', \
                f'{client.nickname} was kicked from the chat !'.encode())
    end_connection(client, clients, False)
    clients.add_message_to_queue(clients.clients, message)