import socket
from client_socket_module import ClientSocket, ClientSocketError
import random
import os
import argparse
try:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("ip", help="IP do servidor master")
    parser.add_argument("porta", help="Porta do servidor master")
    parser.add_argument("comando", help="""Comandos:
                        add adiciona arquivo
                        list lista os arquivos já adicionados
                        rem remove arquivos do servidor
                        recp recupera arquivos do servidor
                        mod modifica propriedades de um dos arquivos no servidor""")
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-i", help="""Caminho do arquivo de entrada. Disponível apenas para o comando ADD.""")
    group1.add_argument("-o", help="""Caminho do arquivo de saída.""")
    parser.add_argument("-n", help="""Número de réplicas do arquivo""")
    args = parser.parse_args()
    s = ClientSocket(args.ip, int(args.porta))
    s.connect()
    print("Conectado ao servidor")
except ClientSocketError as e:
    print(e)
    exit(1)
while True:
    cmd = input('')
    if cmd == "CLOSE":
        print("Fechando a conexão")
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        exit(1)
        

