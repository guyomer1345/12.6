import socket
import logging
import sys
import select
import queue
import threading
from data_classes import Screen
from consts.consts import HELP

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


def find_name(screen: Screen):  #TODO find name...
    """
    Docstring
    """
    screen.messages_queue.put(help)
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
    connect_to_server(client_socket, ip ,port)

    printing_thread = threading.Thread(target = find_name, args=(screen, ))
    printing_thread.daemon = True
    printing_thread.start()

    while True: #TODO change from true
        rlist, wlist, xlist = select.select([client_socket], \
                                            [client_socket], [])
        if client_socket in rlist:
            pass
        
        if client_socket in wlist:
            pass


if __name__ == '__main__':
    main()

#TODO : change client to data_class (add name to it)
#TODO think about how to create enum class (so both numbers and words will be supportedf)