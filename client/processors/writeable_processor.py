import queue
import socket
from data_classes import Client, Screen
from consts.consts import Commands, HELP
from parsers.message_parser import build_message


def process_writeable(client: Client, screen: Screen) -> None:
    """
    Docstring
    """
    messages_left = True
    while messages_left:
        try:
            client_message = screen.client_messages_queue.get(False)

            cmd = next((cmd for cmd in Commands \
                if client_message.startswith(cmd.value.phrase)), None)
            
            if not cmd:
                cmd = Commands.Message # Default value
            
            if cmd == Commands.Help:
                screen.messages_queue.put(HELP)
                continue
                
            if cmd != Commands.SetNickname and not client.name:
                screen.messages_queue.put('Please set a nickname '\
                    +'before sending messages!')
                continue
            
            message = build_message(client, cmd, client_message).encode()
            client.sock.send(message)

        except queue.Empty:
            messages_left = False

        except socket.error:
            pass
        