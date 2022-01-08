import os
import socket
from queue import Queue
from dataclasses import dataclass, field


@dataclass
class Screen:
    """
    An object used to take inputs and show messages
    """
    screen: str = ""
    prompt: str = ""
    messages_queue : Queue[str] = field(default_factory=Queue)
    client_requests: Queue[str] = field(default_factory=Queue)

    def clear_screen(self) -> None:
        """
        This function clears the screen

        :return: None
        """
        os.system('cls')

    def prompt_to_screen(self) -> str:
        """
        This function takes input from the user

        :return: The input taken as a string
        """
        self.clear_screen()
        print(self.screen)
        message = input('Enter Message: ')
        self.prompt = 'Enter Message: '

        return message
    
    def print_to_screen(self, message) -> None:
        """
        This function wraps print to print to the screen object

        :param message: A string containing the message
        :return: None
        """
        self.clear_screen()
        self.screen += (message + '\n')
        print(self.screen)
        print(self.prompt)


@dataclass
class Client:
    """
    An object used to store a socket and a nickname
    """
    sock: socket.socket
    name: str = ''