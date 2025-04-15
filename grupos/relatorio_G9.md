# Relatorio do Grupo ( G9 )

 - Copiando config.ini
- Iniciando o servidor: servidor_ftcp.py
 - Servidor iniciado com PID: 31372
 - Saída do servidor salva em: server_output_G9.log

## Arquivos do Grupo

- Arquivo a.txt - Bytes: Arquivo não encontrado, KBytes: Arquivo não encontrado
- Arquivo b.txt - Bytes: Arquivo não encontrado, KBytes: Arquivo não encontrado

## Execucao do cliente

### get a.txt
```
Inciando Negociacao
	 - Utilizando  127.0.0.1:30001 (UDP)
	 - Mensagem : REQUEST,TCP,a.txt
	 - HEX UDP: 524551554553542c5443502c612e747874
	 - Resposta UDP: 466f726d61746f206465206d656e736167656d20696e76c3a16c69646f2028746f6f206d616e792076616c75657320746f20756e7061636b2028657870656374656420322929
	 - Messagem decodificada : Formato de mensagem inválido (too many values to unpack (expected 2))
Erro no UDP: list index out of range
```
### get b.txt
```
Inciando Negociacao
	 - Utilizando  127.0.0.1:30001 (UDP)
	 - Mensagem : REQUEST,TCP,b.txt
	 - HEX UDP: 524551554553542c5443502c622e747874
	 - Resposta UDP: 466f726d61746f206465206d656e736167656d20696e76c3a16c69646f2028746f6f206d616e792076616c75657320746f20756e7061636b2028657870656374656420322929
	 - Messagem decodificada : Formato de mensagem inválido (too many values to unpack (expected 2))
Erro no UDP: list index out of range
```
Servidor encerrado.

## Comentarios
