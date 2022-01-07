import logging
import socket
from typing import Dict
from data_classes import Request
from errors.errors import ProtocolError
from consts.consts import Commands, NAME_LEN, CMD_LEN, DATA_LEN


def recv(sock: socket.socket, msg_len: int) -> bytes:
    """
    Docstring
    """
    try:
        amount = int(sock.recv(msg_len))
    except:
        raise ProtocolError('Protcol error, or client disconnected') #TODO change to more specifi (cant convert to int)
    
    try:
        data = b''
        while(len(data) != amount):
            data += sock.recv(amount - len(data))
        
        return data

    except:
        raise socket.error


def read_name(sock: socket.socket) -> Dict[str, bytes]:
    """
    Docstring
    """
    name = recv(sock, NAME_LEN).decode()

    return {'nickname': name}


def read_data(sock: socket.socket) -> Dict[str, bytes]:
    """
    Docstring
    """
    data = recv(sock, DATA_LEN)

    return {'data': data}


def read_cmd(sock: socket.socket) -> int:
    """
    Docstring
    """
    cmd = int(sock.recv(CMD_LEN))

    return cmd


def request_parser(client: socket.socket) -> Request:
    """
    Docstring
    """
    name = read_name(client)['nickname']
    if not name:
        raise socket.error
        
    try:
        cmd = Commands(read_cmd(client))
        args = [reader(client) for reader,cmds in \
            reader_dict.items() if cmd in cmds] #TODO dataclass with builder? # if yes fix args[0]

        request = Request(name, cmd, args)
        logging.info(f'Requst is {request}')

        return request

    except:
        raise ProtocolError('An error in the protocol occured')


reader_dict = {
    read_name: 
    [Commands.promote, Commands.kick, Commands.mute, Commands.private_message],
    read_data: 
    [Commands.message, Commands.private_message]
    }