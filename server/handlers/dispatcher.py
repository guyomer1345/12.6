import logging
from consts.consts import Commands
from data_classes import Client, Clients, Request, Message
from errors.errors import BadNickname, BadPermissions,\
                         CantKickYourself, CantMuteYourself
from functions.functions import end_connection
import handlers.command_processors as command_processors


def dispatcher(request: Request, current_client: Client, \
     clients: Clients) -> None:
    """
    This function takes a request and sends it to its
    corresponding functions and handles errors accordingly

    :param request: A request object
    :param current_client: The client making the request
    :clients: Clients object
    :return: None
    """
    message = ''
    try:
        logging.info(f'Client: {current_client}'+ \
             f'is trying to do action {request.cmd}')
        commands_dict[request.cmd](current_client, clients, request)

    except BadPermissions as e:
        message = Message('SERVER', '',\
            "You don't have permissions for that!".encode())
        logging.info(e)

    except BadNickname as e:
        logging.info(e)
        end_connection(current_client, clients, True)
    
    except (CantMuteYourself, CantKickYourself) as e:
        logging.info(e)
        message = Message('SERVER', '',\
            "You cant use that on yourself!".encode())
    
    finally:
        if message:
            clients.add_message_to_queue([current_client], message)



commands_dict = {
    Commands.SET_NICKNAME: command_processors.process_set_nickname,
    Commands.MESSAGE: command_processors.process_message,
    Commands.MUTE: command_processors.process_mute,
    Commands.KICK: command_processors.process_kick,
    Commands.PROMOTE: command_processors.process_promote,
    Commands.PRIVATE_MESSAGE: command_processors.process_private_message
}