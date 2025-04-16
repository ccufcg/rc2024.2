# Relatorio do Grupo ( G8 )

 - Copiando config.ini
- Iniciando o servidor: servidor_ftcp.py
 - Servidor iniciado com PID: 31358
 - Saída do servidor salva em: server_output_G8.log

## Arquivos do Grupo

- Arquivo a.txt - Bytes: Arquivo não encontrado, KBytes: Arquivo não encontrado
- Arquivo b.txt - Bytes: Arquivo não encontrado, KBytes: Arquivo não encontrado

> Os arquivos não encontrados não chegou a ser um problema. Trata-se apenas que os arquivos não estavam no local esperados (não a desconto de pontuação)


## Execucao do cliente

### get a.txt
```
Inciando Negociacao
	 - Utilizando  127.0.0.1:30001 (UDP)
	 - Mensagem : REQUEST,TCP,a.txt
	 - HEX UDP: 524551554553542c5443502c612e747874
	 - Resposta UDP: 524553504f4e53452c5443502c33303030322c612e747874
	 - Messagem decodificada : RESPONSE,TCP,30002,a.txt
Transferencia do arquivo
	 - via TCP em 127.0.0.1:30002
	 - Enviando mensagem TCP: get,a.txt
Timeout: Dado não recebido.
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,118
	 - mensagem hex : 667463705f61636b2c313138
Fim
```
### get b.txt
```
Inciando Negociacao
	 - Utilizando  127.0.0.1:30001 (UDP)
	 - Mensagem : REQUEST,TCP,b.txt
	 - HEX UDP: 524551554553542c5443502c622e747874
	 - Resposta UDP: 524553504f4e53452c5443502c33303030322c622e747874
	 - Messagem decodificada : RESPONSE,TCP,30002,b.txt
Transferencia do arquivo
	 - via TCP em 127.0.0.1:30002
	 - Enviando mensagem TCP: get,b.txt
Timeout: Dado não recebido.
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,5007
	 - mensagem hex : 667463705f61636b2c35303037
Fim
```
Servidor encerrado.

## Comentarios

O protocolo implementado pelo grupo pode ser utilizado pelo cliente de referência e foi capaz de ;

- ✅ Realiza a etapa de neogociação
- ✅ Transfere os arquivos via TCP
- ✅ Encerra a conexão TCP com os parametros corretos


> 📌 **Explicação** : do `Timeout: Dado não recebido`, na verdade os dados foram transmitidos corretamente o erro acontece em razão de como os dados são enviados `conn.sendall(saida)` (no trecho do codigo abaixo) pode gerar esse tipo de problema dentro de uma thread. **Tal fato não gera a penalização na nota**. Entrega completa

```python
def tcp_client(conn, addr):
    print(f"TCP Client conectado com {addr}")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            decoded_data = data.decode('utf-8')
            print(f"TCP recebido com {addr}: {decoded_data}")
            arquivo = decoded_data.split(',')[1]
            if arquivo in files:
                with open(files[arquivo], mode='rb') as file:
                    saida = file.read()
            else:
                 break

            conn.sendall(saida)
            res = conn.recv(1024).decode('utf-8')
            print(f"TCP recebido com {addr}: {res}")

    print(f"TCP Client desconectado com {addr}")
```

> 🔔 **Importante** : Caso algum dos comentarios esteja presente no código me enviem um e-mail apontando para eu rever a correção.
