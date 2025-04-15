# Relatorio do Grupo ( G2 )

 - Copiando config.ini
- Iniciando o servidor: servidor.py
 - Servidor iniciado com PID: 31106
 - Saída do servidor salva em: server_output_G2.log

## Arquivos do Grupo

- Arquivo a.txt - Bytes: 10, KBytes: 0
- Arquivo b.txt - Bytes: 5312, KBytes: 8

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
	 - Transferido 10 bytes via TCP
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,10
	 - mensagem hex : 667463705f61636b2c3130
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
	 - Transferido 5312 bytes via TCP
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,5312
	 - mensagem hex : 667463705f61636b2c35333132
Fim
```
Servidor encerrado.

## Comentarios
