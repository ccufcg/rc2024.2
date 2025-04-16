import socket
import sys
import time

def main():
    if len(sys.argv) != 4:
        print("Uso: cliente.py <servidor> <porta_udp> <arquivo>")
        return
        
    servidor = sys.argv[1]
    porta_udp = int(sys.argv[2])
    arquivo = sys.argv[3]

 
    TIMEOUT = 30

    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(TIMEOUT)
        
        start_time = time.time()
        mensagem = f"REQUEST,TCP,{arquivo}"
        udp_socket.sendto(mensagem.encode(), (servidor, porta_udp))
        
        try:
            resposta, _ = udp_socket.recvfrom(1024)
            tempo_resposta = time.time() - start_time
            print(f"Resposta UDP recebida em {tempo_resposta:.2f}s")
            
            partes = resposta.decode().split(',')
            
            if partes[0] == 'ERROR':
                print(f"Erro: {partes[1]}")
                return
                
            if partes[0] != 'RESPONSE':
                print("Resposta inválida do servidor")
                return
                
            porta_tcp = int(partes[2])
            arquivo = partes[3]
            
        except socket.timeout:
            print(f"Timeout: Nenhuma resposta UDP recebida em {TIMEOUT} segundos")
            return
            
    except Exception as e:
        print(f"Erro na negociação: {e}")
        return
    finally:
        udp_socket.close()

    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(TIMEOUT)
        
        # Conexão TCP
        start_time = time.time()
        try:
            tcp_socket.connect((servidor, porta_tcp))
            tempo_conexao = time.time() - start_time
            print(f"Conectado ao TCP em {tempo_conexao:.2f}s")
        except socket.timeout:
            print(f"Timeout: Não foi possível conectar ao TCP em {TIMEOUT} segundos")
            return
        

        try:
            comando = f"get,{arquivo}"
            tcp_socket.sendall(comando.encode())
        except socket.timeout:
            print("Timeout no envio da solicitação")
            return
            

        dados = b''
        try:
            while True:
                parte = tcp_socket.recv(4096)
                if not parte:
                    break
                dados += parte
        except socket.timeout:
            print(f"Timeout: Transferência incompleta após {TIMEOUT} segundos sem dados")
            return
            
      
        try:
            ack_msg = f"ftcp_ack,{len(dados)}"
            tcp_socket.sendall(ack_msg.encode())
            print(f"[CLIENTE] ACK enviado: {ack_msg}")
        except socket.timeout:
            print("Timeout no envio do ACK")
            return
            
   
        with open(arquivo, 'wb') as f:
            f.write(dados)
            
        print(f"[CLIENTE] Arquivo {arquivo} recebido ({len(dados)} bytes)")
        
    except Exception as e:
        print(f"Erro na transferência: {e}")
    finally:
        tcp_socket.close()

if __name__ == "__main__":
    main()
