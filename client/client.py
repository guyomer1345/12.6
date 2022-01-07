import socket
import logging
import sys
import select
import queue
import threading
from typing_extensions import runtime
from data_classes import Screen, Client
from consts.consts import HELP
from processors import readable_proccessor, writeable_processor

screen = Screen()

def create_client_socket() -> socket.socket:
    """
    Docstring
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    return client_socket


def connect_to_server(client_socket: socket.socket, ip: str, port: str) -> None:
    """
    Docstring
    """
    try:
        client_socket.connect((ip, int(port)))
        logging.info("Successfully connceted to server")

    except socket.error:
        logging.error("You entered an invalid address or the server isn't up")
        sys.exit()


def input_function(screen: Screen) -> None:
    """
    Docstring
    """
    while True:
        client_message = screen.prompt_to_screen()
        if client_message.startswith('/None'):
            client_message.replace('/None', '')

        screen.client_messages_queue.put(client_message)


def printing_function(screen: Screen) -> None:
    """
    Docstring
    """
    screen.messages_queue.put(HELP)
    while True:
        try:
            message = screen.messages_queue.get(False)
            screen.print_to_screen(message)

        except queue.Empty:
            pass


def main():
    if len(sys.argv) != 3:
        logging.error('Please run the client in the following way: '\
            + 'client.py <ip> <port>')
        sys.exit()
    ip, port = sys.argv[1:3]

    client_socket = create_client_socket()
    client = Client(client_socket)
    connect_to_server(client.sock, ip ,port)

    for func in [printing_function, input_function]:
        thread = threading.Thread(target = func, args=(screen, ))
        thread.daemon = True
        thread.start()

    try:
        running = True
        while running:
            rlist, wlist, xlist = select.select([client.sock], \
                                                [client.sock], [])
            if client.sock in rlist:
                readable_proccessor.process_readable(client, screen)
            
            if client.sock in wlist:
                writeable_processor.process_writeable(client, screen)

    except KeyboardInterrupt:
        logging.info('Shutting down')
        sys.exit()


if __name__ == '__main__':
    main()