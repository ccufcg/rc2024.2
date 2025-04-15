import socket
from sys import argv, exit
import configparser

# Váriaveis de configuração do cliente
UDP_PORT = None
MAX_FILE_SIZE = None
SERVER_IP = None
TIMEOUT_LIMIT = None


def load_client_settings():
    """
    Carrega as configurações do cliente (e.g. porta UDP do servidor, tamanho
    máximo de arquivo, endereço IP do servor), presentes no arquivo de 
    configurações.
    """

    global UDP_PORT, MAX_FILE_SIZE, SERVER_IP, TIMEOUT_LIMIT

    config = configparser.ConfigParser()
    config.read("config.ini")

    UDP_PORT = int(config["SERVER_CONFIG"]["UDP_PORT"])
    MAX_FILE_SIZE = int(config["CLIENT_CONFIG"]["MAX_FILE_SIZE"])
    SERVER_IP = config["CLIENT_CONFIG"]["SERVER_IP"]
    TIMEOUT_LIMIT = float(config["CLIENT_CONFIG"]["TIMEOUT_LIMIT"])


def start_negotiation(requested_file: str) -> dict:
    """
    Envia uma requisição (via UDP) para o servidor, solicitando um determinado
    arquivo.

    Parameters
    ----------
    requested_file : str
        O nome do arquivo solicitado.

    Returns
    -------
    dict
        Retorna um mapa contendo as informações retornadas pelo servidor. Caso
        a negociação falhe, uma exceção é lançada informando o erro ocorrido.
    """

    server_address = (SERVER_IP, UDP_PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(TIMEOUT_LIMIT)
        request = f"REQUEST,TCP,{requested_file}"

        try:
            udp_socket.sendto(request.encode(), server_address)
            data, _ = udp_socket.recvfrom(1024)

        except socket.timeout:
            print(f"[TIMEOUT]: Unable to get response from {server_address}")
            exit(1)

    response = parse_response(data)

    if response.get("FAILED"):
        print(f"[ERROR]: {response.get('ERROR_MSG')}")
        exit(1)

    return response


def transfer_file_over_tcp(request_data: dict) -> tuple[str, int]:
    """
    Solicita a transferência (via TCP) do arquivo indicado na negociação inicial
    para o servidor. Ao término da transferência, envia um ACK para o servidor
    com o número de bytes recebido, encerrando a conexão.

    Parameters
    ----------
    request_data : dict
        Um mapa com as informações retornadas da negociação inicial com o
        servidor.

    Returns
    -------
    tuple[str, int]
        Uma tupla contendo o nome do arquivo e seu tamanho em bytes.
    """

    socket_port = int(request_data.get("SOCKET_PORT"))
    filename = request_data.get("FILENAME")

    server_address = (SERVER_IP, socket_port)
    received_bytes = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        print(f"[CLIENT] Connecting to {SERVER_IP} at port {socket_port}")
        tcp_socket.settimeout(TIMEOUT_LIMIT)

        try:
            tcp_socket.connect(server_address)

            request = f"get,{filename}"
            tcp_socket.sendall(request.encode())

            response = tcp_socket.recv(MAX_FILE_SIZE)
            received_bytes = len(response)

            ack = f"ftcp_ack,{received_bytes}"
            tcp_socket.sendall(ack.encode())

        except socket.timeout:
            print("[TIMEOUT]: Connection with TCP server has timed out.")
            exit(1)

        except ConnectionRefusedError:
            print("[ERROR]: Connection was refused by the server.")
            exit(1)

        except BrokenPipeError:
            print("[ERROR]: Connection was terminated while data transmission.")
            exit(1)

    return filename, received_bytes


def parse_response(data: bytes) -> dict:
    """
    Extrai as informações da resposta do servidor.

    Parameters
    ----------
    data : bytes
        Os dados de uma resposta do servidor.

    Returns
    -------
    dict
        Um mapa contendo as informações da requisição. Contém os seguintes
        campos:

        - PROTOCOL (str): o protocolo indicado para a transferência do arquivo
        - FAILED (bool): flag que indica se a requisição falhou
        - SOCKET_PORT (int): a porta do socket para a transferência do arquivo
        - FILENAME (str): o nome do arquivo solicitado
        - ERROR_MSG (str): mensagem de erro retornada pelo servidor, em caso de
          falhas

        Para requisições válidas, o campo ERROR_MSG terá valor "None".

        Para requisições inválidas, os campos PROTOCOL, FILENAME e SOCKET_PORT
        terão valor "None".
    """

    res_data = {
        "FAILED": False,
        "SOCKET_PORT": None,
        "PROTOCOL": None,
        "FILENAME": None,
        "ERROR_MSG": None,
    }

    decoded_data = data.decode().split(",")
    command, *fields = decoded_data

    if command == "ERROR":
        res_data["FAILED"] = True
        res_data["ERROR_MSG"] = fields[0]
    else:
        res_data["PROTOCOL"], res_data["SOCKET_PORT"], res_data["FILENAME"] = fields

    return res_data


if __name__ == "__main__":
    if len(argv) != 2:
        print("Uso: python3 client_ftcp.py [ARQUIVO]")
        exit(1)

    load_client_settings()

    requested_file = argv[1]
    response = start_negotiation(requested_file)
    file, byte_count = transfer_file_over_tcp(response)

    print(f"[CLIENT] File \"{file}\" ({byte_count} B) received successfully!")
