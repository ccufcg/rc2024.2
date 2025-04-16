"""
Servidor para negociação UDP e transferência TCP de arquivos.

Inicia threads para UDP (negociação de porta) e TCP (transferência).
Configurações são lidas de um arquivo `config.ini`.
"""

import socket
import threading
import configparser

def udp_negotiation():
    """
    Gerencia a negociação de porta via UDP. Escutando na porta 'UDP_TRANSFER_PORT'.
    Valida requisições no formato 'REQUEST,TCP,{fName}'.
    Responde com 'RESPONSE,TCP,{porta},{fName}' se o arquivo existir.
    Envia mensagem de erro para requisições inválidas ou se o arquivo não existir.

    Note:
        FNF = Arquivo não encontrado
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.bind((SERVER_ADDRESS, UDP_TRANSFER_PORT))
        print(f"Servidor UDP ouvindo na porta {UDP_TRANSFER_PORT}")
        while True:
            try:
                data, addr = udp_sock.recvfrom(1024)
                message = "ERROR,PROTOCOLO INVALIDO,,"
                decoded_data = data.decode().split(',')
                print(f"UDP recebido: {data.decode()}")

                if not data:
                    continue
                if len(decoded_data) != 3:
                    send_error_message(message, addr, udp_sock)
                    continue

                command,protocol,fName = decoded_data

                if command == "REQUEST" and protocol == "TCP" and (fName in AVAILABLE_FILES):
                    message = "RESPONSE,TCP,{0},{1}".format(TCP_TRANSFER_PORT, fName)
                    udp_sock.sendto(message.encode(), addr)
                    print("Porta enviada")
                elif fName not in AVAILABLE_FILES:
                    message = "ERROR,FNF,,"
                    send_error_message(message, addr, udp_sock)
                else:
                    send_error_message(message, addr, udp_sock)
                
            except Exception as e:
                    udp_sock.sendto(message.encode(), addr)
                    print(f"Erro no UDP: {e}")

def send_error_message(message, addr, udp_sock):
    """Envia uma mensagem de erro para um cliente via UDP.
    A mensagem deve seguir o protocolo definido, com 4 campos separados por vírgula


    Args:
        message (str): Mensagem de erro formatada para envio (ex: "ERROR,PROTOCOLO INVALIDO,,").
        addr (tuple): Endereço do cliente no formato (IP, porta).
        udp_sock (socket.socket): Socket UDP configurado para comunicação.
    """
    udp_sock.sendto(message.encode(), addr)
    print("Request inválido")

def send_file(fileName, conn):
    """
    Envia um arquivo via TCP.

    Args:
        fileName (str): Nome do arquivo a ser enviado.
        conn (socket.socket): Conexão TCP com o cliente.
    """
    try:
        with open(fileName, 'rb') as file:
            while data := file.read(1024):
                conn.send(data)
        print(f"Arquivo {fileName} enviado")
    except socket.timeout:
        print("Timeout: Nenhum dado recebido.")
    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")
    finally:
        conn.shutdown(socket.SHUT_WR)

def handle_tcp_client(conn, addr):
    """Gerencia a interação com um cliente TCP. 
    Processa comandos 'get,{fName}' para enviar arquivos
    'ftcp_ack' para encerrar a comunicação.

    Args:
        conn (socket.socket): Conexão TCP estabelecida.
        addr (tuple): Endereço (IP, porta) do cliente.
    """
    print(f"Cliente TCP conectado em: {addr}")
    try:
        while True:
            data = conn.recv(1024).decode().strip().split(",")  # Decodifica e remove espaços
            command = data[0]
            filename = data[1]

            if command == "get":
                send_file(filename, conn)  # Envia o arquivo

                ack_data = conn.recv(1024).decode().strip().split(',')
                if ack_data[0] == "ftcp_ack":
                    print(f"ACK recevido: {ack_data}")
                    return
                else:
                    print("ACK inválido ou não recebido")
                    return
            elif command == "ftcp_ack":
                print("ACK recebido sem contexto de envio")
            else:
                print(f"Comando inválido: {command}")

    except Exception as e:
        print(f"Erro no TCP: {e}")
    finally:
        print(f"Cliente TCP desconectado em: {addr}")
        conn.close()

def tcp_echo():
    """Escuta conexões TCP e inicia threads para clientes, utilizando a porta
    'TCP_TRANSFER_PORT', encontrada no config.ini. Suporta até 5 conexões simultâneas
    """
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind((SERVER_ADDRESS, TCP_TRANSFER_PORT))
    tcp_sock.listen(5)
    print(f"Servidor TCP ouvindo na porta {TCP_TRANSFER_PORT}")
    while True:
        conn, addr = tcp_sock.accept()
        client_thread = threading.Thread(target=handle_tcp_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    # Inicializando o Config Parser para ler as as configurações iniciais
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Armazenando as configurações iniciais
    SERVER_ADDRESS = config['SERVER_CONFIG']['SERVER_ADDRESS']
    UDP_TRANSFER_PORT = int(config['SERVER_CONFIG']['UDP_PORT'])
    TCP_TRANSFER_PORT = int(config['SERVER_CONFIG']['TCP_PORT'])

    # Armazenando arquivos disponíveis para envio
    AVAILABLE_FILES = dict(config.items('AVAILABLE_FILES')).values()

    # Iniciar thread para UDP
    udp_thread = threading.Thread(target=udp_negotiation)
    udp_thread.daemon = True
    udp_thread.start()

    # Iniciar thread para TCP
    tcp_thread = threading.Thread(target=tcp_echo)
    tcp_thread.daemon = True
    tcp_thread.start()

    print("Servidor rodando. Pressione Ctrl+C para encerrar.")

    try:
        # Mantém o programa principal em execução
        while True:
            pass
    except KeyboardInterrupt:
        print("Servidor encerrado.")