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
	 - Messagem decodificada : too many values to unpack (expected 2)
Erro no UDP: list index out of range
```
### get b.txt
```
Inciando Negociacao
	 - Utilizando  127.0.0.1:30001 (UDP)
	 - Mensagem : REQUEST,TCP,b.txt
	 - HEX UDP: 524551554553542c5443502c622e747874
	 - Resposta UDP: 466f726d61746f206465206d656e736167656d20696e76c3a16c69646f2028746f6f206d616e792076616c75657320746f20756e7061636b2028657870656374656420322929
	 - Messagem decodificada : too many values to unpack (expected 2)
Erro no UDP: list index out of range
```
Servidor encerrado.

## Comentarios

O protocolo implementado pelo grupo pode ser utilizado pelo cliente de referência e foi capaz de ;

- ❌ Realiza a etapa de neogociação
- ❌ Transfere os arquivos via TCP
- ❌ Encerra a conexão TCP com os parametros corretos

Adiconalmente, o grupo utiliza um pool de portas TCP para realizar a transferencia.

**Necessário ler o codigo para atribuir a nota** e rexecutar. Possivelmente o erro tenha acontecido por erro no arquivo de configuração e a Exception acontece na pois entre alinha 93 e 103.

> Os arquivos não encontrados não chegou a ser um problema. Trata-se apenas que os arquivos não estavam no local esperados (não a desconto de pontuação)