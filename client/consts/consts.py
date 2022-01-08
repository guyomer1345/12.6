from enum import Enum, EnumMeta

PREFIX = "/"
HELP = \
"""
Do note that before sending messages you have to set up a nickname only once!.
The following commands me be available to you:
/help, /set-nickname, /mute, /promote, /kick, /private-message, /quit, /view-managers.
If no command is specified a normal message will be sent\n
""".strip()


class Commands(Enum):
    class SetNickname(EnumMeta):
        status_code = 0
        phrase = f'{PREFIX}set-nickname'

    class Message(EnumMeta):
        status_code = 1
        phrase = f'{PREFIX}None'

    class Promote(EnumMeta):
        status_code = 2
        phrase = f'{PREFIX}promote'

    class Kick(EnumMeta):
        status_code = 3
        phrase = f'{PREFIX}kick'

    class Mute(EnumMeta):
        status_code = 4
        phrase = f'{PREFIX}mute'

    class PrivateMessage(EnumMeta):
        status_code = 5
        phrase = f'{PREFIX}private-message'

    class Help(EnumMeta):
        status_code = 6
        phrase = f'{PREFIX}help'