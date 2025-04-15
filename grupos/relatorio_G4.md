# Relatorio do Grupo ( G4 )

 - Copiando config.ini
- Iniciando o servidor: servidor_ftcp.py
 - Servidor iniciado com PID: 31219
 - Saída do servidor salva em: server_output_G4.log

## Arquivos do Grupo

- Arquivo a.txt - Bytes: 9, KBytes: 0
- Arquivo b.txt - Bytes: 9, KBytes: 0

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
Timeout: Nenhum dado recebido.
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,9
	 - mensagem hex : 667463705f61636b2c39
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
Timeout: Nenhum dado recebido.
Finalizando Conexao TCP
	 - mensagem txt : ftcp_ack,9
	 - mensagem hex : 667463705f61636b2c39
Fim
```
Servidor encerrado.

## Comentarios
