from consts.consts import Commands
from data_classes import Client

def add_data(client_message: str) -> str:
    """
    Docstring
    """
    data = str(len(client_message)).zfill(8) + client_message

    return data


def add_name(client_message: str) -> str:
    """
    Docstring
    """
    name = client_message.split()[1]
    name = str(len(name)).zfill(2) + name

    return name


def add_name_and_data(client_message : str) -> str:
    """
    Docstring
    """
    name = add_name(client_message)
    client_message = ' '.join(client_message.split()[2:]) # Everything after the name
    data =  add_data(client_message) 

    return name + data



def build_header(name, cmd: Commands) -> str:
    """
    Docstring
    """
    header = str(len(name)).zfill(2) + name
    header += str(cmd.value.status_code)

    return header


def build_body(cmd: Commands, client_message: str) -> str:
    """
    Docstring
    """
    try:
        body = next((adder(client_message) for adder,cmds in \
                parser_dict.items() if cmd in cmds))
    
    except StopIteration:
        return ''
    
    return body


def build_message(client: Client, cmd: Commands, client_message: str) -> str:
    """
    Docstring
    """
    try:            
        if cmd == Commands.SetNickname:
            name = client_message.split()[1]
            client.name = name
            header = build_header(name, cmd)
            return header

        header = build_header(client.name, cmd)
        body = build_body(cmd, client_message)
        message = header + body
        return message

    except:
        return ''


parser_dict = {
    add_data: [Commands.Message],
    add_name: [Commands.Mute, Commands.Kick, Commands.Promote],
    add_name_and_data: [Commands.PrivateMessage] 
}