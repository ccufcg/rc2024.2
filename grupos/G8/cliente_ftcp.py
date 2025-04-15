import socket
from configparser import ConfigParser
import sys


if len(sys.argv) < 2:
    print("Uso: python3 cliente_ftcp.py <nome_do_arquivo>")
    sys.exit(1)

arquive = sys.argv[1]

config = ConfigParser()
config.read('config.ini')

UDP_SERVER_PORT = config['SERVER_CONFIG']['UDP_PORT']
UDP_CLIENTE_PORT = config['CLIENTE_CONFIG']['UDP_PORT']


def udp():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('127.0.0.1', int(UDP_CLIENTE_PORT)))
    udp_sock.settimeout(5)
    print(f"UDP server listening on port {UDP_CLIENTE_PORT}")

    data = "REQUEST,TCP," + arquive
    udp_sock.sendto(data.encode('utf-8'), ('127.0.0.1', int(UDP_SERVER_PORT)))

    try:
        resposta, addr = udp_sock.recvfrom(1024)
        resposta = resposta.decode('utf-8')
        print(resposta)

        parte = resposta.split(',')
        verify(parte, arquive)


        tcp_port = int(parte[2])
        filename = parte[3].strip()
        tcp(tcp_port, filename)

    except socket.timeout as e:
        print("Timed out")
    except Exception as ex:
        print(ex)

def verify(response: list[str], arquive: str):
    if response[0] != "RESPONSE":
        raise Exception("ERROR,Resposta inesperada")
    elif response[1] != "TCP":
        raise Exception("ERROR,Protocolo Invalido")
    elif not response[2].isdigit():
        raise Exception("ERROR,Porta Invalida")
    elif response[3] != arquive:
        raise Exception("ERROR,Arquivo Invalido")

def tcp(tcp_port: int, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.connect(('127.0.0.1', tcp_port))
        print(f"Conectado ao servidor TCP na porta {tcp_port}")

        get_cmd = f"get,{filename}"
        tcp_sock.sendall(get_cmd.encode('utf-8'))
        data = tcp_sock.recv(10240)
        print(f"Conteúdo recebido:\n{data.decode('utf-8')}")

        ack = f"ftcp_ack,{len(data)}"
        tcp_sock.sendall(ack.encode('utf-8'))
        print("ACK enviado. Conexão encerrada.")

if __name__ == '__main__':
    udp()
