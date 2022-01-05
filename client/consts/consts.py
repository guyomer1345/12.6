from enum import Enum

HELP = \
"""
Do note that before sending messages you have to set up a nickname.
The following commands me be available to you:
help, set_nickname, mute, promote, kick, private_message.
If no command is specified a normal message will be sent
""".strip()


class Commands(Enum):
    MESSAGE: str = 'message'
    MUTE: str = 'mute'