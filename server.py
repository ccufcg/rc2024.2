import socket
import os
import configparser
import threading
import time

    
def validar_requisicao_tcp(mensagem, conn):
    
    mensagem = mensagem.split(",")
    
    if len(mensagem) != 2:
        raise ValueError("[TCP] ERROR | REQUISIÇÃO INVÁLIDA. Formato <comando> <nome_arquivo>")
    
    comando, nome_arquivo = mensagem
    if comando != 'get':
        raise ValueError("[TCP] ERROR | COMANDO INVÁLIDO")
    
    if nome_arquivo not in ['a.txt', 'b.txt']:
        raise ValueError("[TCP] ERROR | ARQUIVO INVÁLIDO")
    
    if not os.path.exists(nome_arquivo):
        raise ValueError("[TCP] ERROR | Erro no servidor, arquivo não existe!")
        
    return True
    
def enviar_dados(conn, addr, arquivo):
    time.sleep(2)
    with open(arquivo, "rb") as f:
            bytes_enviados = 0
            while True:
                dados = f.read(1024)
                if not dados:
                    break
                conn.sendall(dados)
                print(f"[TCP] {len(dados)} dados enviados para {addr}")
                
                bytes_enviados += len(dados)
        
            conn.shutdown(socket.SHUT_WR)
            print(f"[TCP] Enviado {bytes_enviados} bytes para {addr}")

def receber_ack(conn, addr):
    try:
        ack = conn.recv(1024).decode()
        print(f"[TCP] ACK recebido do cliente {addr}: {ack}")
    except Exception as e:
        print(f"[TCP] Erro ao receber ACK do cliente {addr}. Erro: {e}")
 
def handle_transfer(conn, addr):
    
    print(f"[TCP] Conexão estabelecida com {addr}")
    with conn:
        # Recebe o comando "get,arquivo"
        mensagem = conn.recv(1024).decode("utf-8")
        print(f"[TCP] Comando recebido: {mensagem} de {addr}")
        
        try:
            if validar_requisicao_tcp(mensagem, conn):       
                comando, arquivo = mensagem.split(",")
                # Envia o conteúdo do arquivo em segmentos
                enviar_dados(conn, addr, arquivo)
                receber_ack(conn, addr)
                            
        except ValueError as e:
            print(f"[TCP] ERROR | Erro: {e}")
            conn.sendall(str(e).encode("utf-8"))
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"[TCP] Conexão com {addr} encerrada durante envio: {e}")
        
        print(f"[TCP] Conexão encerrada com o cliente {addr}")

        
def handle_connection():
        
    while True:
        mensagem_codificada, endereco = udp_socket.recvfrom(1024)
        mensagem = mensagem_codificada.decode("utf-8")
        print(f"[UDP] Recebido de {endereco}: {mensagem}")
        
        requisicao = mensagem.split(",")
        if (len(requisicao) != 3):
            error = "ERROR, REQUISIÇÃO INVÁLIDA. FORMATO: <comando>,<protocolo>,<nome_arquivo>"
            udp_socket.sendto(error.encode("utf-8"), endereco)
            
        else:
            comando, protocolo, nome_arquivo = requisicao
            if mensagem.startswith("REQUEST,TCP,") and nome_arquivo in ['a.txt', 'b.txt']:
                resposta = f"RESPONSE,TCP,{TCP_PORT},{nome_arquivo}"
                udp_socket.sendto(resposta.encode(), endereco)
                print(f"[UDP] Enviado: {resposta} para {endereco}")
                
                conn, endereco_tcp = tcp_socket.accept()

                #Thread TCP
                tcp_thread = threading.Thread(target=handle_transfer,  args=(conn, endereco_tcp))
                tcp_thread.daemon = True
                tcp_thread.start()
                        
            else:   
                error = "ERROR, "
                if comando != "REQUEST":
                    error += "COMANDO INVÁLIDO,,"
                elif protocolo != "TCP":
                    error += "PROTOCOLO INVÁLIDO,,"
                else:
                    error += "ARQUIVO INVÁLIDO,,"
                print(f"[UDP] ERROR | Enviado para {endereco}: {error}")
                udp_socket.sendto(error.encode("utf-8"), endereco)

# Lê o arquivo de configuração
config = configparser.ConfigParser()
config.read("config.ini")

TCP_PORT = int(config["SERVER_CONFIG"]["TCP_PORT"])
UDP_PORT = int(config["SERVER_CONFIG"]["UDP_PORT"])
FILE_A = config["SERVER_CONFIG"]["FILE_A"]
FILE_B = config["SERVER_CONFIG"]["FILE_B"]

#Socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("0.0.0.0", UDP_PORT))

print(f"[UDP] Servidor ouvindo na porta {UDP_PORT}...")

#Socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(("0.0.0.0", TCP_PORT))
tcp_socket.listen(5)
print(f"[TCP] Servidor ouvindo na porta {TCP_PORT}...")


#Thread UDP
udp_thread = threading.Thread(target=handle_connection)
udp_thread.daemon = True
udp_thread.start()

print("SERVIDOR RODANDO")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("CONEXÃO COM SERVIDOR ENCERRADA")
    
