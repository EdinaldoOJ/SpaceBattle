# Dicionários e funções para formatar e analisar mensagens e dados.

# Constantes do protocolo
CMD_FIELD_LENGTH = 16  # Comprimento exato do campo "cmd" (comando) no protocolo, em bytes.
LENGTH_FIELD_LENGTH = 4  # Comprimento exato do campo de comprimento no protocolo, em bytes.
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Tamanho máximo do campo de dados de acordo com o protocolo. É calculado como 10 elevado ao valor de LENGTH_FIELD_LENGTH - 1.
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Tamanho exato do cabeçalho da mensagem, que inclui os campos "cmd" e "length".
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Tamanho máximo da mensagem total, incluindo o cabeçalho e os dados.
DELIMITER = "|"  # Caractere delimitador utilizado no protocolo para separar os campos da mensagem.
DATA_DELIMITER = "#"  # Delimitador utilizado na parte de dados da mensagem para separar os campos de dados.
END_OF_MESSAGE = '$'  # Caractere que indica o fim da mensagem.

# Mensagens de protocolo
# Neste dicionário teremos todos os nomes de comandos do cliente
PROTOCOL_CLIENT = {
    "disconnect_msg": "DISCONNECT",
    "initial_details": "GET_GAME_DATA",
    "game_status_request": "GET_STATUS",
    "shoot_command": "SHOOT",
    "key_down_msg": "KEY_PRESSED",
    "key_up_msg": "KEY_RELEASED"
}

# Neste dicionário teremos todos os nomes de comandos do servidor
PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "error_msg": "ERROR",
    "connection_limit": "MAX_CONNECTED",
    'winner_msg': "WINNER",
    "connected_successfully": "CONNECT_SUCCESS",
    "ok_msg": "OK",
    "game_starting_message": "GAME_STARTING",
    "game_status_response": "STATUS_RESPONSE",
    "initial_data_response": "START_DATA"
}

# Outras constantes
ERROR_RETURN = None  # O que é retornado em caso de erro


def build_message(cmd: str, data: str) -> str or None:
    """
    Obtém o nome do comando (str) e o campo de dados (str) e cria uma mensagem de protocolo válida
    Retorna: str, ou None se ocorrer um erro
    """
    if len(cmd) >= CMD_FIELD_LENGTH or len(data) >= MAX_DATA_LENGTH:
        # Verificando se os parâmetros recebidos são de comprimento permitido
        return None
    while len(cmd) < CMD_FIELD_LENGTH:
        cmd += ' '
    data_len = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
    full_msg = DELIMITER.join((cmd, data_len, data))
    return full_msg


def parse_message(data: str) -> tuple:
    """
    Analisa a mensagem do protocolo e retorna o nome do comando e o campo de dados
    Retorna: cmd (str), dados (str). Se ocorrer algum erro, retorna None, None
    """
    lst = data.split(DELIMITER)
    if len(lst) != 3:
        print(1)
        return None, None
    cmd, expected_data_len, msg = lst
    if len(cmd) != CMD_FIELD_LENGTH or len(expected_data_len) != LENGTH_FIELD_LENGTH:
        return None, None
    try:
        expected_data_len = int(expected_data_len)
    except Exception as e:
        print(3)
        return None, None
    if expected_data_len != len(msg):
        print(4)
        return None, None
    cmd = cmd.replace(' ', '')
    return cmd, msg


def split_data(msg: str, expected_fields: int) -> list:
    """Método auxiliar. obtém uma string e o número de campos esperados nela. divide a string
    usando o delimitador de campo de dados do protocolo (|#) e valida se há número correto de campos.
    Retorna: lista de campos se tudo ok. Se ocorrer algum erro, retorna None"""

    lst = msg.split(DATA_DELIMITER)  # Dividindo os dados em uma lista
    if len(lst) != expected_fields + 1:  # Verificando se o valor esperado corresponde ao comprimento da lista
        return [None]
    return lst


def join_data(msg_fields: list) -> str:
    """
    Método auxiliar. Obtém uma lista, une todos os seus campos a uma string dividida pelo delimitador de dados.
    Retorna: string que se parece com cell1#cell2#cell3
    """
    str_lst = [str(x) for x in msg_fields]  # Convertendo todos os valores da lista em string
    st = DATA_DELIMITER.join(str_lst)  # Juntando a lista em uma string
    return st
