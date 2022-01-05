import logging
from consts.consts import Commands
from data_classes import Client, Clients, Request
from errors.errors import BadPermissions
import handlers.command_processors as command_processors

def dispatcher(request: Request, current_client: Client, \
     clients: Clients) -> None:
    """
    Docstring
    """
    try:
        logging.info(f'Client: {current_client}'+ \
             f'is trying to do action {request.cmd}')
        commands_dict[request.cmd](current_client, clients, request)

    except BadPermissions:
        pass #TODO Send bad permissions to client

    except Exception as e: #TODO go over all the exceptions and handle them accordingly
        logging.debug(f'Exception in dispatcher {e}')


commands_dict = {
    Commands.set_nickname: command_processors.process_set_nickname,
    Commands.message: command_processors.process_message,
    Commands.mute: command_processors.process_mute,
    Commands.kick: command_processors.process_kick,
    Commands.promote: command_processors.process_promote,
    Commands.private_message: command_processors.process_private_message
}