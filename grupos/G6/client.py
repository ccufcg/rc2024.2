import socket
import configparser
import time

def validar_resposta_servidor(resposta):
    global arquivo_desejado
    comando, protocolo, porta_transferencia, nome_arquivo = resposta
    if comando != 'RESPONSE' or nome_arquivo != arquivo_desejado or protocolo != 'TCP':
        return False
    return True


def iniciar_conexao():
    # Negociação via UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(10)
        try:
            #Envia a requisição
            mensagem = f"REQUEST,TCP,{arquivo_desejado}"
            udp_socket.sendto(mensagem.encode(), (servidor, porta_udp))

            #Recebe a resosta da requisição
            resposta, _ = udp_socket.recvfrom(1024)
            resposta = resposta.decode("utf-8")
            print(f"[UDP] Resposta do servidor: {resposta}")
            resposta = resposta.split(",")
            
            if (len(resposta) != 4):
                print("[UDP] Resposta do servidor inválida:")
                return None
            elif (not validar_resposta_servidor(resposta)):
                print("[UDP] Resposta do servidor inválida")        
                return None
            else:    
                comando, protocolo, porta_transferencia, nome_arquivo = resposta
                porta_transferencia = int(porta_transferencia)
                print("[UDP] Resposta válida do servidor")
                return porta_transferencia
        except socket.timeout as e:
            print(f"[TCP] ERRO | TIMEOUT UDP: {e}")

def receber_dados(porta_transferencia):    
    
    # Transferência via TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.settimeout(10)
        try:
            
            tcp_socket.connect((servidor, porta_transferencia))
            print(f"[TCP] Conectado ao servidor na porta {porta_transferencia}")

            # Envia comando get
            comando = f"get,{arquivo_desejado}"
            tcp_socket.sendall(comando.encode("utf-8"))

            # Recebe dados do arquivo
            conteudo = b""
            while True:
                dados = tcp_socket.recv(1024)
                if not dados:
                    break
                
                if dados.decode().startswith("[TCP] ERROR"):
                    print(dados.decode())
                    return
                
                print(f"Recebido {len(dados)} bytes")
                conteudo += dados

            tamanho_recebido = len(conteudo)

            # Salva arquivo localmente
            with open(f"baixado_{arquivo_desejado}", "wb") as f:
                f.write(conteudo)

            print(f"[TCP] Arquivo recebido ({tamanho_recebido} bytes) e salvo como baixado_{arquivo_desejado}")

            # Envia ACK
            ack = f"[TCP] ftcp_ack,{tamanho_recebido}"
            tcp_socket.sendall(ack.encode("utf-8"))
            print(f"[TCP] ACK enviado: {ack}")
        
        except socket.timeout as e:
            print(f"[TCP] ERRO | TIMEOUT: {e}")
        except ConnectionRefusedError as e:
            print(f"[TCP] ERRO | Conexão recusada {e}")
        except Exception as e:
            print(f"[TCP] ERRO | Erro inesperado {e}")
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"[TCP] Conexão com {addr} encerrada durante envio: {e}")

    print("[TCP] Conexão encerrada.")

config = configparser.ConfigParser()
config.read("config.ini")
servidor = "127.0.0.1"

porta_udp = int(config["SERVER_CONFIG"]["UDP_PORT"])
arquivo_desejado = "b.txt"

porta_transferencia = iniciar_conexao()

if porta_transferencia != None:
    receber_dados(porta_transferencia)