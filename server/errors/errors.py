class ProtocolError(Exception):
    '''Raise when a message doesn't follow protocol guidelines'''
    pass


class ClientDisconnected(Exception):
    '''Raise when a client has disconnected informally'''


class SocketNotExist(Exception):
    '''Raise when trying to perform actions on a socket that isn't connected'''
    pass


class BadNickname(Exception):
    '''Baseclass for bad nickname exceptions'''


class NicknameUsed(BadNickname):
    '''Raise when a nickname is already used'''
    pass


class NicknameNotAllowed(BadNickname):
    '''Raise when a nickname is not allowed'''
    pass


class HasNickname(BadNickname):
    '''Raise when a client already has a nickname'''
    pass


class BadPermissions(Exception):
    '''Raise when a client doesn't have needed permissions'''
    pass


class UserDoesNotExist(Exception):
    '''Raise when a message is sent to a non existing user'''
    pass


class CantMuteYourself(Exception):
    '''Raise when a manager tries to mute himself'''
    pass


class CantKickYourself(Exception):
    '''Raise when a manager tries to kick himself'''
    pass


class CantPromoteYourself(Exception):
    '''Raise when a manager tries to promote himself'''
    pass