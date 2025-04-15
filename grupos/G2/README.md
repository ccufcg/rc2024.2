# ProjetoRedes
Implementação em Python do Protocolo de Transferência de Arquivos Personalizado – FTCP

## Equipe

- Mikael Brasileiro Ferreira de Almeida Amaral
- Cristian Alves da Silva
- Victor Ribeiro Miranda
- João Victor Cosme Melo

## Visão Geral do Projeto

O objetivo principal é desenvolver um cliente e um servidor que se comunicam através de um protocolo próprio (FTCP). A negociação inicial ocorre via UDP, onde o cliente requisita um arquivo (`a.txt` ou `b.txt`) e especifica o protocolo de transferência (obrigatoriamente TCP nesta versão). O servidor responde com a porta TCP designada para a transferência. Em seguida, o cliente estabelece uma conexão TCP nessa porta, solicita o arquivo, o recebe e confirma o recebimento antes de encerrar a conexão.

## Entregáveis

A entrega final do projeto consiste nos itens detalhados na tabela abaixo. Certifique-se de que todos os itens listados para o repositório Git estejam presentes e atualizados na branch principal (`main` ou `master`) antes da data final.

| Item # | Descrição                                      | Forma de Entrega                  |
| :----- | :--------------------------------------------- | :-------------------------------- |
| 1      | **Código Fonte** (Cliente e Servidor)          | Repositório Git (este)            |
| 2      | **Arquivos de Teste** (`a.txt`, `b.txt` e `foto.png`)      | Repositório Git (este)            |
| 3      | **Arquivo de Configuração** (`config.ini`)     | Repositório Git (este)            |
| 4      | **Arquivo de Captura de Tráfego** (`.pcapng`) | Repositório Git (este)            |
| 5      | **Relatório de Análise** (PDF ou Markdown)   | Google Classroom (1 por equipe)   |

## Como Executar (Exemplo Básico)

1.  **Configuração:** Certifique-se de que o arquivo `config.ini` está presente na mesma pasta dos scripts e configurado corretamente com as portas desejadas e os caminhos para os arquivos `a.txt`,`b.txt` e `foto.png`.
2.  **Iniciar o Servidor:**
    
    ```bash
    python servidor_ftcp.py
    ```
3.  **Executar o Cliente (em outro terminal):**
    ```bash
    python cliente_ftcp.py a.txt
    ```
