# Protocolo de Transferência de Arquivos Personalizado – FTCP

Este repositório contém a implementação do projeto **FTCP (File Transfer Custom Protocol)**, um sistema cliente-servidor para transferência de arquivos utilizando os protocolos TCP e UDP de forma customizada, conforme especificado nas instruções.

## Equipe

*   **Integrante 1:** Ana Beatriz Cavalcanti Marinho.
*   **Integrante 2:** Eurico Gabriel Vasconcelos Pereira.
*   **Integrante 3:** Maria Clara Silva Maia.
*   **Integrante 4:** Renaldo dos Santos Franca.

## Visão Geral do Projeto

O objetivo principal é desenvolver um cliente e um servidor que se comunicam através de um protocolo próprio (FTCP). A negociação inicial ocorre via UDP, onde o cliente requisita um arquivo (`a.txt` ou `b.txt`) e especifica o protocolo de transferência (obrigatoriamente TCP nesta versão). O servidor responde com a porta TCP designada para a transferência. Em seguida, o cliente estabelece uma conexão TCP nessa porta, solicita o arquivo, o recebe e confirma o recebimento antes de encerrar a conexão.

## Entregáveis

A entrega final do projeto consiste nos itens detalhados na tabela abaixo. 

| Item # | Descrição                                      | Forma de Entrega                        |
| :----- | :--------------------------------------------- | :---------------------------------------|
| 1      | **Código Fonte**                               | **[Cliente](./cliente_ftcp.py)**        |
| 2      | **Código Fonte**                               | **[Servidor](./servidor_ftcp.py)**      |
| 3      | **Arquivos de Teste**                          | **[Arquivos .txt](./files)**            |
| 4      | **Arquivo de Configuração**                    | **[Configuração](./config.ini)**        |
| 5      | **Arquivo de Captura de Tráfego**              |                   ---                   |
| 6      | **Relatório de Análise**                       |                   ---                   |


## Como Executar

1.  **Configuração:** Como arquivo `config.ini` presente na mesma pasta dos scripts e configurado com as portas desejadas e os caminhos para os arquivos `a.txt` e `b.txt`.
2.  **Iniciar o Servidor:**
    
    ```bash
    python servidor_ftcp.py
    ```
3.  **Executar o Cliente (em outro terminal):**
    ```bash
    python cliente_ftcp.py a.txt
    ```
