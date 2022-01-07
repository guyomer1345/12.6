import enum
from configparser import ConfigParser


class Permissions(enum.Enum):
    BASIC = 0
    WRITE = 1 
    READ = 2
    MANAGER = 3


class Commands(enum.Enum):
    SET_NICKNAME = 0
    MESSAGE = 1
    PROMOTE = 2
    KICK = 3
    MUTE = 4
    PRIVATE_MESSAGE = 5


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