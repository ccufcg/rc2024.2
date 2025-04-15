import socket
import threading
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
TCP_PORT = int(config['SERVER_CONFIG']['TCP_PORT'])
UDP_PORT = int(config['SERVER_CONFIG']['UDP_PORT'])
FILE_A = config['SERVER_CONFIG']['FILE_A']
FILE_B = config['SERVER_CONFIG']['FILE_B']

FILES = {
    "a.txt": FILE_A,
    "b.txt": FILE_B
}

def handle_tcp_transfer(conn, addr):
    print(f"[TCP] Conexão estabelecida com {addr}")
    try:
        request = conn.recv(1024).decode('utf-8').strip()
        if not request.startswith("get,"):
            conn.close()
            return

        _, filename = request.split(",", 1)
        filepath = FILES.get(filename)

        if not filepath or not os.path.exists(filepath):
            conn.close()
            return

        # Envia arquivo
        with open(filepath, "rb") as f:
            total_sent = 0
            while True:
                data = f.read(1024)
                if not data:
                    break
                conn.sendall(data)
                total_sent += len(data)

        conn.shutdown(socket.SHUT_WR)
        ack = conn.recv(1024).decode('utf-8')
        if ack.startswith("ftcp_ack"):
            print(f"[TCP] ACK recebido: {ack}")
    except Exception as e:
        print(f"[ERRO TCP] {e}")
    finally:
        conn.close()
        print(f"[TCP] Conexão encerrada com {addr}")

def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', TCP_PORT))
    sock.listen(5)
    print(f"[TCP] Servidor ouvindo na porta {TCP_PORT}")
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_tcp_transfer, args=(conn, addr), daemon=True).start()

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    print(f"[UDP] Servidor ouvindo na porta {UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode('utf-8').strip()
        print(f"[UDP] Recebido de {addr}: {msg}")
        parts = msg.split(',')

        if len(parts) != 3 or parts[0] != "REQUEST":
            response = "ERROR,FORMATO INVALIDO,,"
        else:
            _, protocolo, arquivo = parts
            if protocolo != "TCP":
                response = "ERROR,PROTOCOLO INVALIDO,,"
            elif arquivo not in FILES or not os.path.exists(FILES[arquivo]):
                response = "ERROR,ARQUIVO INEXISTENTE,,"
            else:
                response = f"RESPONSE,TCP,{TCP_PORT},{arquivo}"

        sock.sendto(response.encode('utf-8'), addr)
        print(f"[UDP] Enviado para {addr}: {response}")

if __name__ == '__main__':
    threading.Thread(target=udp_server, daemon=True).start()
    threading.Thread(target=tcp_server, daemon=True).start()

    print("Servidor FTCP rodando. Pressione Ctrl+C para encerrar.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Servidor encerrado.")

