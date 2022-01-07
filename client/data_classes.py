import os
import socket
from dataclasses import dataclass, field
from queue import Queue


@dataclass
class Screen:
    """
    Docstring
    """
    screen: str = ""
    prompt: str = ""
    messages_queue : Queue[str] = field(default_factory=Queue)
    client_messages_queue: Queue[str] = field(default_factory=Queue)

    def clear_screen(self) -> None:
        """
        Docstring
        """
        os.system('cls')


    def prompt_to_screen(self) -> str:
        """
        Docstring
        """
        self.clear_screen()
        print(self.screen)
        message = input('Enter Message: ')
        self.prompt = 'Enter Message: '

        return message
    

    def print_to_screen(self, message) -> None:
        """
        Docstring
        """
        self.clear_screen()
        self.screen += (message + '\n')
        print(self.screen)
        print(self.prompt)


@dataclass
class Client:
    """
    Docstring
    """
    sock: socket.socket
    name: str = ''