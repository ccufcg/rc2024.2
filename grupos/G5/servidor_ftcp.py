import socket
import threading
import configparser

# Váriaveis de configuração do servidor
MAX_REQUEST_SIZE = None
TCP_PORT = None
UDP_PORT = None
FILES = {"FILE_A": None, "FILE_B": None}


def load_config():
    """
    Carrega as configurações definidas no arquivo de configurações.
    """
    global MAX_REQUEST_SIZE, TCP_PORT, UDP_PORT, FILES

    config = configparser.ConfigParser()
    config.read("config.ini")

    MAX_REQUEST_SIZE = int(config["SERVER_CONFIG"]["MAX_REQUEST_SIZE"])
    TCP_PORT = int(config["SERVER_CONFIG"]["TCP_PORT"])
    UDP_PORT = int(config["SERVER_CONFIG"]["UDP_PORT"])
    FILES["FILE_A"] = config["SERVER_CONFIG"]["FILE_A"]
    FILES["FILE_B"] = config["SERVER_CONFIG"]["FILE_B"]


def process_udp_request(data: bytes):
    """
    Processa uma requisição recebida via UDP, interpretando os dados
    recebidos e formatando uma resposta de acordo com o protocolo definido.

    Parameter
    ----------
    data : bytes
        os dados recebidos do cliente, em formato de bytes. Espera-se
        uma string separada por vírgulas, contendo informações do protocolo.

    Returns
    -------
    str
        uma string formatada com a resposta para o cliente. Caso o protocolo
        recebido seja inválido, uma mensagem
        de erro padrão será retornada.
    """
    converted = data.decode("utf-8").split(",")
    converted[-1] = converted[-1].strip()
    out = f"RESPONSE,TCP,{TCP_PORT},{converted[-1]}"

    if "UDP" in converted:
        out = "ERROR,PROTOCOLO INVALIDO,,"

    if converted[-1] not in FILES.values():
        out = "ERROR,ARQUIVO INEXISTENTE,,"

    return out


def process_tcp_request(data: bytes):
    """
    Processa  e valida a requisição enviado pelo cliente.

    Parameter
    ---------
    data : bytes
        um conjunto de bytes que representa a mensagem de requisição enviada pelo cliente.

    Returns
    -------
    bytes
        um conjunto de bytes que representa o arquivo solicitado pelo usuário. Retorna
        o tipo _None_ se a requisição não for encontrado.
    """
    converted = data.decode().split(",")
    converted[-1] = converted[-1].strip()
    out = None

    if converted[0] != "get":
        return out

    with open(f"./files/{converted[-1]}", 'rb') as file:
        out = file.read()

    return out


def handle_tcp_client(conn, addr):
    """
    Consome a mensagen de requisição vinda do cliente e envia o arquivo solicitado, caso
    não haja problemas no processo de validação e processamento da requisição.

    Parameters
    ----------
    conn
        é um novo socket que representa a conexão com o cliente. 
    addr
         é uma tupla que contém o endereço do cliente.
    """
    print(f"[SERVER] TCP Client connected from {addr}")

    with conn:
        data = None

        while not data:
            data = conn.recv(MAX_REQUEST_SIZE)

        processed_file = process_tcp_request(data)

        if processed_file is not None:
            conn.sendall(processed_file)
            print(f"[SERVER] File sent to {addr}.")

    print(f"[SERVER] TCP Client disconnected from {addr}")


def tcp_protocol():
    """
    Cria uma thread para cada cliente que estabelece uma conexão com o servidor.
    """
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind(("0.0.0.0", TCP_PORT))
    tcp_sock.listen(5)

    while True:
        conn, addr = tcp_sock.accept()
        client_thread = threading.Thread(
            target=handle_tcp_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()


def udp_protocol():
    """
    Inicia o servidor UDP que ficará escutando na porta configurada,
    recebendo mensagens e respondendo conforme a lógica do protocolo.
    """
    print(f"[SERVER] Listening via UDP on port {UDP_PORT}")
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(("0.0.0.0", UDP_PORT))

    while True:
        data, addr = udp_sock.recvfrom(MAX_REQUEST_SIZE)

        if not data:
            continue

        protocol_message = data.decode("utf-8")
        print(f"[SERVER] Received via UDP from {addr}: {protocol_message}")

        client_request = process_udp_request(data)
        udp_sock.sendto(str.encode(client_request), addr)


def init_protocol(method):
    """
    Inicia uma thread que vai executar um método relacionado ao protocolo
    de interesse.

    Parameter
    ---------
    method
        uma referência ao método relacionado a um método.
    """
    protocol_thread = threading.Thread(target=method)
    protocol_thread.daemon = True
    protocol_thread.start()


def main():
    load_config()

    init_protocol(udp_protocol)
    init_protocol(tcp_protocol)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nServer has been closed.")


if __name__ == "__main__":
    main()
