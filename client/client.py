import socket
import logging
import sys
import select
import queue
import threading
from data_classes import Screen, Client
from consts.consts import HELP
import processors

screen = Screen()

def create_client_socket() -> socket.socket:
    """
    This function is wrapper function for creating a socket

    :return: Socket object
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    return client_socket


def connect_to_server(client_socket: socket.socket, ip: str, port: str) -> None:
    """
    This function is warrper for function for socket's connect

    :param client_socket: The socket to connect
    :param ip: A string containing the ip
    :param port: A string containing the port
    :return: None
    """
    try:
        client_socket.connect((ip, int(port)))
        logging.info("Successfully connceted to server")

    except socket.error:
        logging.error("You entered an invalid address or the server isn't up")
        sys.exit()


def input_function(screen: Screen) -> None:
    """
    This function takes inputs in a loop

    :param screen: Screen ojbect
    :return: None
    """
    while True:
        client_message = screen.prompt_to_screen()
        if client_message.startswith('/None'):
            client_message.replace('/None', '')

        screen.client_requests.put(client_message)


def printing_function(screen: Screen) -> None:
    """
    This function prints the messages received from the server

    :param screen: Screen objecet
    :return: None
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
                processors.process_readable(client, screen)
            
            if client.sock in wlist:
                processors.process_writeable(client, screen)

    except KeyboardInterrupt:
        logging.info('Shutting down')
        sys.exit()


if __name__ == '__main__':
    main()