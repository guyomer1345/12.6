import enum
from configparser import ConfigParser


class Permissions(enum.Enum): #TODO Change to caps AND swap read\write
    send: int = 0 #TODO Find better name
    read: int = 1 
    write: int = 2
    manager: int = 3


class Commands(enum.Enum):
    set_nickname:int = 0
    message:int = 1
    promote:int = 2
    kick:int = 3
    mute:int = 4
    private_message:int = 5


config = ConfigParser()
config.read('config/config.ini')

HOURS = 11
MINUTES = 16
IP = config.get('settings', 'ip')
PORT = int(config.get('settings', 'port'))
NAME_LEN = int(config.get('settings', 'name_len'))
CMD_LEN = int(config.get('settings', 'cmd_len'))
DATA_LEN = int(config.get('settings', 'data_len'))
MAX_LISTEN = int(config.get('settings', 'max_listen'))