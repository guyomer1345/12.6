import socket
from queue import Queue
from datetime import datetime
from typing import Dict, List
from errors.errors import SocketNotExist
from dataclasses import dataclass, field
from consts.consts import Permissions, Commands, HOURS, MINUTES


@dataclass
class Request:
    """
    An object used to store requests
    """
    nickname: str
    cmd: Commands
    args: Dict[str, bytes]


@dataclass
class Message:
    """
    An object used to store messages
    """
    sender: str
    prefix: str
    data: bytes
    date: str = str(datetime.now())[HOURS:MINUTES]

    def build(self) -> bytes:
        """
        This function takes the stored paramters and builds them to a message

        :return: The message encoded to bytes
        """
        message = (self.date + ' ').encode() +\
                 (self.prefix+self.sender+': ').encode() + \
                     self.data
        message = str(len(message)).zfill(9).encode() + message

        return message

        
@dataclass
class Client:
    """
    An object used to store the information about a client
    """
    sock: socket.socket
    _nickname: str = ''
    permissions: List[Permissions] = field(default_factory=list)
    message_queue: Queue[bytes] = field(default_factory=Queue)
    
    @property
    def nickname(self) -> str:
        return self._nickname
    
    @nickname.setter
    def nickname(self, nickname: str) -> None:
        self._nickname = nickname
    
    def remove_permissions(self, permissions: List[Permissions]) -> None:
        """
        This functions removes permissions from the client

        :param permissions: A list of permissions to remove
        :return: None
        """
        [self.permissions.remove(permission) for permission in permissions]

    def add_permissions(self, permissions: List[Permissions]) -> None:
        """
        This functions adds permissions from the client

        :param permissions: A list of permissions to add
        :return: None
        """
        [self.permissions.append(permission) for permission in permissions]


@dataclass
class Clients:
    """
    An object used to store a list of clients
    """
    clients: List[Client] = field(default_factory=list)

    def get_by_nickname(self, nickname: str) -> socket.socket:
        """
        This functions finds the client with a given nickname

        :raise SocketNotExist: If couldn't find any matching sockets
        :param nickname: The nickname to filter by
        :return: The socket of the client with the given nickname
        """
        try:
            sock = [client for client in \
                self.clients if client.nickname == nickname][0]
        
            return sock
        
        except IndexError:
            raise SocketNotExist("Socket doesn't exist")

    
    def view_managers(self) -> str:
        """
        This functions finds all the clients with the manager permission

        :return: A list of clients with the manager permission
        """
        managers = [client.nickname for client in \
                 self.clients if Permissions.MANAGER in client.permissions]
        managers = ', '.join(managers)

        return managers

    def get_by_sock(self, sock: socket.socket) -> Client:
        """
        This functins find the client associated with a given socket

        :raise SocketNotExist: If couldn't find any matching clients
        :sock: The socket to filter by
        :return: The client matching the socket
        """
        try:
            client = [client for client in \
                 self.clients if client.sock == sock][0]
            
            return client
        
        except IndexError:
            raise SocketNotExist("Socket doesn't exist")

    def remove_client(self, sock: socket.socket) -> None:
        """
        This functions removes a socket from the clients object

        :raise SocketNotExist: If no client was found
        :param sock: The socket to remove  
        :return: None
        """
        try:
            client_to_remove = [client for client in \
                 self.clients if client.sock == sock][0]
            self.clients.remove(client_to_remove)
        
        except:
            raise SocketNotExist("Socket doesn't exist")

    def add_message_to_queue(self, clients: List[Client], message: Message) -> None:
        """
        This functions adds message to a client messages queue

        :param clients: A list containing client objects
        :message: The message object to add
        :return: None
        """
        for client in clients:
            if Permissions.READ in client.permissions: 
                client.message_queue.put(message)