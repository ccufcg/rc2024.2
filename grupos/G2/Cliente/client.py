"""Cliente para transferência de arquivos via UDP/TCP.

Realiza a negociação de porta via UDP e transfere arquivos via TCP.
Configurações do servidor são lidas de um arquivo `config.ini`.
"""

import socket
import os
import configparser
import sys

def negotiate_port(fName):
    """
    Negocia uma porta TCP com o servidor via UDP.

    Args:
        fName (str): Nome do arquivo solicitado.

    Returns:
        str: Porta TCP para conexão.
        str: "ERROR" se a negociação falhar.
        str: "FNF" se o arquivo requerido não existir

    Raises:
        Exception: Exceção genérica em caso de falha na comunicação UDP.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        message = "REQUEST,TCP,{}".format(fName)
        sock.sendto(message.encode(), (SERVER_ADDRESS, UDP_TRANSFER_PORT))
        
        try:
            resp, _ = sock.recvfrom(1024)
            parts = resp.decode().split(',')

            if parts[0] == 'RESPONSE':
                return parts[2]
            elif parts[1] == 'FNF':
                return parts[1]
            else:
                return "ERROR"
        except Exception as e:
                print("Erro no UDP: {}".format(e))
        
def request_file(sock_tcp, fName):
    """
    Solicita e recebe um arquivo via TCP através do comando 'get,{fName}
    O arquivo é então salvo em blocos de 1024 bytes
    Ao receber o arquivo inteiro é enviado um ack para o servidor. 

    Args:
        sock_tcp (socket.socket): Socket TCP conectado ao servidor.
        fName (str): Nome do arquivo a ser baixado.
    """
    lenFile = 0
    message = "get,{}".format(fName)
    try:
        sock_tcp.sendall(message.encode())
        with open(fName, 'wb') as file:
            while data := sock_tcp.recv(1024):
                lenFile += len(data)
                file.write(data)
        
    except socket.timeout:
        print("Timeout: Nenhum dado recebido.")
    except Exception as e:
        print(f"Erro no TCP: {e}")

    send_ack(sock_tcp, lenFile, fName)
    print("Download concluído com {} bytes".format(lenFile) if os.path.exists(fName) else "Falha no download")

def send_ack(sock_tcp, lenFile, fName):
    """
    Envia confirmação (ACK) ao servidor após o download.
    Descarta arquivos caso receba um arquivo vazio.
    Após o envio do ACK, fecha a conexão.

    Args:
        sock_tcp (socket.socket): Socket TCP conectado.
        lenFile (int): Tamanho do arquivo recebido em bytes.
        fName (str): Nome do arquivo.
    """
    if lenFile > 0:
        ackMessage = "ftcp_ack,{}".format(lenFile)
        sock_tcp.sendall(ackMessage.encode())
        print(ackMessage)
    elif os.path.isfile(fName):
        os.remove(fName)
        print("Problema no envio")

    print("Desconectando...")
    sock_tcp.close() 


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('../config.ini')

    SERVER_ADDRESS = config['SERVER_CONFIG']['SERVER_ADDRESS']
    UDP_TRANSFER_PORT = int(config['SERVER_CONFIG']['UDP_PORT'])

    
    if len(sys.argv) > 1:
        fName = sys.argv[1]
        TRANSFER_PORT = negotiate_port(fName)
    else:
        print("Adicione o nome do arquivo no formato: \033[34mpython client.py nome_arquivo\033[0m")
        TRANSFER_PORT = "ERROR"

    if TRANSFER_PORT != "ERROR" and TRANSFER_PORT != "FNF":
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.settimeout(5)  # Timeout de 5 segundos
        sock_tcp.connect((SERVER_ADDRESS, int(TRANSFER_PORT)))
        request_file(sock_tcp, fName)
    elif TRANSFER_PORT == "FNF":
        print("O arquivo requisitado não existe")
    else:
        print("Problema na negociação UDP")