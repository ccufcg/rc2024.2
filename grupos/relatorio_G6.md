# Relatorio do Grupo ( G6 )

 - Copiando config.ini
- Iniciando o servidor: server.py
 - Servidor iniciado com PID: 31262
 - Saída do servidor salva em: server_output_G6.log

## Arquivos do Grupo

- Arquivo a.txt - Bytes: 12, KBytes: 0
- Arquivo b.txt - Bytes: 6611, KBytes: 8

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
	 - Transferido 12 bytes via TCP
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,12
	 - mensagem hex : 667463705f61636b2c3132
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
	 - Transferido 6611 bytes via TCP
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,6611
	 - mensagem hex : 667463705f61636b2c36363131
Fim
```
Servidor encerrado.

## Comentarios

O protocolo implementado pelo grupo pode ser utilizado pelo cliente de referência e foi capaz de ;

- ✅ Realiza a etapa de neogociação
- ✅ Transfere os arquivos via TCP
- ✅ Encerra a conexão TCP com os parametros corretos


O grupo atendeu a todas as especificações do protocolo.
