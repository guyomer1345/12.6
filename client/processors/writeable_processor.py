import queue
import socket
from data_classes import Client, Screen
from consts.consts import Commands, HELP
from parsers.message_parser import build_request


def process_writeable(client: Client, screen: Screen) -> None:
    """
    This functions sends a message to the server

    :param client: The client sending the message
    :param screen: A screen object
    :return None:
    """
    requests_left = True
    while requests_left:
        try:
            requests_left = screen.client_requests.get(False)

            cmd = next((cmd for cmd in Commands \
                if requests_left.startswith(cmd.value.phrase)), None)
            
            if not cmd:
                cmd = Commands.Message # Default value
            
            if cmd == Commands.Help:
                screen.messages_queue.put(HELP)
                continue
                
            if cmd != Commands.SetNickname and not client.name:
                screen.messages_queue.put('Please set a nickname '\
                    +'before sending messages!')
                continue
            
            request = build_request(client, cmd, requests_left).encode()
            client.sock.send(request)

        except queue.Empty:
            requests_left = False

        except socket.error:
            pass
        