# Relatorio do Grupo ( G3 )

 - Copiando config.ini
- Iniciando o servidor: serverTCP.py
 - Servidor iniciado com PID: 31150
 - Saída do servidor salva em: server_output_G3.log

## Arquivos do Grupo

- Arquivo a.txt - Bytes: 21, KBytes: 0
- Arquivo b.txt - Bytes: 9246, KBytes: 12

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
	 - Transferido 21 bytes via TCP
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,21
	 - mensagem hex : 667463705f61636b2c3231
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
	 - Transferido 9246 bytes via TCP
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,9246
	 - mensagem hex : 667463705f61636b2c39323436
Fim
```
Servidor encerrado.

## Comentarios

O protocolo implementado pelo grupo pode ser utilizado pelo cliente de referência e foi capaz de ;

- ✅ Realiza a etapa de neogociação
- ✅ Transfere os arquivos via TCP
- ✅ Encerra a conexão TCP com os parametros corretos


O grupo atendeu a todas as especificações do protocolo.
