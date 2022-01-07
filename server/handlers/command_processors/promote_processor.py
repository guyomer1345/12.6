from consts.consts import Permissions
from data_classes import Client, Clients ,Request
from errors.errors import BadPermissions, CantPromoteYourself


def process_promote(current_client: Client, \
     clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if not Permissions.manager in current_client.permissions:
        raise BadPermissions

    client_nickname = request.args['nickname']
    client = clients.get_by_nickname(client_nickname)

    if current_client == client:
        raise CantPromoteYourself(f'{request.nickname} tried to promote himself')
    
    permissions = client.permissions
    if Permissions.manager not in permissions:
        client.add_permissions([Permissions.manager])
        return None

    client.remove_permissions([Permissions.manager])