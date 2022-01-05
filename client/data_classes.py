import os
from dataclasses import dataclass, field
from queue import Queue


@dataclass
class Screen:
    screen: str = ""
    prompt: str = ""
    messages_queue : Queue[str] = field(default_factory=Queue)


    def clear_screen(self):
        os.system('cls')


    def prompt_to_screen(self):
        self.clear_screen()
        print(self.screen)
        message = input('Enter Message: ')
        self.prompt = 'Enter Message: ' + message

        return message
    

    def print_to_screen(self, message):
        self.clear_screen()
        self.screen += (message + '\n')
        print(self.screen)
        print(self.prompt)