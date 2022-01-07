from consts.consts import Permissions
from data_classes import Client, Clients ,Request
from errors.errors import BadPermissions, CantMuteYourself


def process_mute(current_client: Client, \
     clients: Clients, request: Request) -> None:
    """
    Docstring
    """
    if not Permissions.manager in current_client.permissions:
        raise BadPermissions

    client_nickname = request.args['nickname']
    client = clients.get_by_nickname(client_nickname)

    if current_client == client:
        raise CantMuteYourself(f'{request.nickname} tried to mute himself')
    
    permissions = client.permissions
    if Permissions.read not in permissions and Permissions.write in permissions:
        client.add_permissions([Permissions.read])
        return None

    client.remove_permissions([Permissions.read])

    #TODO SEND MUTED MESSAGE TO CLIENTs
    