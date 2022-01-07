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
    Docstring
    """
    nickname: str
    cmd: Commands
    args: Dict[str, bytes]


@dataclass
class Message:
    sender: str
    prefix: str
    data: bytes
    date: str = str(datetime.now())[HOURS:MINUTES]

    def build(self) -> bytes:
        """
        Docstring
        """
        message = (self.date + ' ').encode() +\
                 (self.prefix+self.sender+': ').encode() + \
                     self.data
        message = str(len(message)).zfill(9).encode() + message

        return message

        
@dataclass
class Client:
    """
    Docstring
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
        Docstring
        """
        [self.permissions.remove(permission) for permission in permissions]


    def add_permissions(self, permissions: List[Permissions]) -> None:
        """
        Docstring
        """
        [self.permissions.append(permission) for permission in permissions]


@dataclass
class Clients:
    """
    Docstring
    """
    clients: List[Client] = field(default_factory=list)


    def get_by_nickname(self, nickname: str):
        """
        Docstring
        """
        try:
            sock = [client for client in \
                self.clients if client.nickname == nickname][0]
        
            return sock
        
        except IndexError:
            raise SocketNotExist("Socket doesn't exist")

    
    def view_managers(self) -> str:
        """
        Docstring
        """
        managers = [client.nickname for client in \
                 self.clients if Permissions.MANAGER in client.permissions]
        managers = ' '.join(managers)

        return managers


    def get_by_sock(self, sock: socket.socket) -> Client:
        """
        Docstring
        """
        try:
            client = [client for client in \
                 self.clients if client.sock == sock][0]
            
            return client
        
        except IndexError:
            raise SocketNotExist("Socket doesn't exist")
        

    def remove_client(self, sock: socket.socket) -> None:
        """
        Docstring
        """
        try:
            client_to_remove = [client for client in \
                 self.clients if client.sock == sock][0]
            self.clients.remove(client_to_remove)
        
        except:
            raise SocketNotExist("Socket doesn't exist")


    def add_message_to_queue(self, clients: List[Client], message: Message) -> None:
        """
        Docstring
        """
        for client in clients:
            if Permissions.WRITE in client.permissions: 
                client.message_queue.put(message)