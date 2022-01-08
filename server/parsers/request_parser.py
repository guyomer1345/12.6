import logging
import socket
from typing import Dict
from collections import ChainMap
from data_classes import Request
from errors.errors import ProtocolError, ClientDisconnected
from consts.consts import Commands, NAME_LEN, CMD_LEN, DATA_LEN


def recv(sock: socket.socket, length: int) -> bytes:
    """
    This function is wrapper function for socket's recv

    :raise ClientDisconnected: If the amount received wasn't an integer
    :raise  ProtocolError: If the message wasn't sent by the protocol guidelines
    :param sock: The socket to recv from
    :param length: How many bytes represent the amount to read
    :return: The data read in bytes
    """
    try:
        amount = int(sock.recv(length))
    except ValueError:
        raise ClientDisconnected('Client disconnected')
    except:
        raise ProtocolError('An error in the protocol occured')

    try:
        data = b''
        while(len(data) != amount):
            data += sock.recv(amount - len(data))
        
        return data

    except:
        raise socket.error


def read_name(sock: socket.socket) -> Dict[str, bytes]:
    """
    This functions is wrapping function for recv used to receive a name

    :param sock: The socket to recv from
    :return: A dictionary containing the name
    """
    name = recv(sock, NAME_LEN).decode()

    return {'nickname': name}


def read_data(sock: socket.socket) -> Dict[str, bytes]:
    """
    This functions is wrapping function for recv used to receive data

    :param sock: The socket to recv from
    :return: A dictionary containing the data
    """
    data = recv(sock, DATA_LEN)

    return {'data': data}


def read_cmd(sock: socket.socket) -> int:
    """
    This functions is wrapping function for socket's recv used to receive a cmd

    :param sock: The socket to recv from
    :return: An integer representing the command 
    """
    cmd = int(sock.recv(CMD_LEN))

    return cmd


def request_parser(sock: socket.socket) -> Request:
    """
    This function parses the data read into a request object

    :raise ProtocolError: If the data wasn't send according to the protocol
    :param sock: The socket to receieve the data from   
    :return: A request object
    """
    try:
        name = read_name(sock)['nickname']
        cmd = Commands(read_cmd(sock))
        args = [reader(sock) for reader,cmds in \
            reader_dict.items() if cmd in cmds]
        args = dict(ChainMap(*args))

        request = Request(name, cmd, args)
        logging.info(f'Requst is {request}')

        return request

    except:
        raise ProtocolError('An error in the protocol occured')


reader_dict = {
    read_name: 
    [Commands.PROMOTE, Commands.KICK, Commands.MUTE, Commands.PRIVATE_MESSAGE],
    read_data: 
    [Commands.MESSAGE, Commands.PRIVATE_MESSAGE]
    }