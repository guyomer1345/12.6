from consts.consts import Commands
from data_classes import Client

def add_data(client_request: str) -> str:
    """
    This function takes data and padds it

    :param client_request: The data to pad
    :return: The data after padding
    """
    data = str(len(client_request)).zfill(8) + client_request

    return data


def add_name(client_request: str) -> str:
    """
    This functions gets the name from the message and padds it

    :param client_request: The request containing the name
    :return: The name after padding
    """
    name = client_request.split()[1]
    name = str(len(name)).zfill(2) + name

    return name


def add_name_and_data(client_request : str) -> str:
    """
    This function is wrapping function for add name and add data

    :param client_request: The request containing the name and data
    :return: The data after padding
    """
    name = add_name(client_request)
    client_request = ' '.join(client_request.split()[2:]) # Everything after the name
    data =  add_data(client_request) 

    return name + data



def build_header(name, cmd: Commands) -> str:
    """
    This functions builds the message header

    :param name: The client name
    :param cmd: The command requested
    :return: The header in a string format
    """
    header = str(len(name)).zfill(2) + name
    header += str(cmd.value.status_code)

    return header


def build_body(cmd: Commands, client_request: str) -> str:
    """
    This functions builds the request body

    :param cmd: The command requested
    :param client_request: The request
    :return: The message body in a string format
    """
    try:
        body = next((adder(client_request) for adder,cmds in \
                parser_dict.items() if cmd in cmds))
    
    except StopIteration:
        return ''
    
    return body


def build_request(client: Client, cmd: Commands, client_request: str) -> str:
    """
    This function builds the request

    :param client: A client object
    :param cmd: The command requested
    :param client_request: The client request 
    :return: The message in a string format
    """
    try:            
        if cmd == Commands.SetNickname:
            name = client_request.split()[1]
            client.name = name
            header = build_header(name, cmd)
            return header

        header = build_header(client.name, cmd)
        body = build_body(cmd, client_request)
        message = header + body
        return message

    except:
        return ''


parser_dict = {
    add_data: [Commands.Message],
    add_name: [Commands.Mute, Commands.Kick, Commands.Promote],
    add_name_and_data: [Commands.PrivateMessage] 
}