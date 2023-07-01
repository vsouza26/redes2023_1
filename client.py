import socket
from client_socket_module import ClientSocket, ClientSocketError
from client_socket_module.exceptions_client import ClientExceptions
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
                        rec recupera arquivos do servidor
                        mod modifica propriedades de um dos arquivos no servidor""")
    parser.add_argument("-i", help="""Caminho do arquivo de entrada caso seja o comando ADD. Se for comando REM ou REC é o nome do arquivo a ser removido ou recuperado respectivamente""")
    parser.add_argument("-o", help="""Caminho do arquivo de saída.""")
    parser.add_argument("-n", help="""Número de réplicas do arquivo""", default=1)
    args = parser.parse_args()
    s = ClientSocket(args.ip, int(args.porta))
    s.connect()
    print("Conectado ao servidor")
except ClientSocketError as e:
    print(e)
    exit(1)
try:
    if args.comando == "add":
        if(not args.i):
            print("add malformado digite python3 client.py -h para ajuda.")
            exit(1)
        s.add(caminho=args.i, num_repl=int(args.n))
    elif args.comando == "list":
        s.list()
    elif args.comando == "rem":
        if(not args.i):
            print("remover malformado digite python3 client.py -h para ajuda.")
            exit(1)
        s.rem(nome = args.i)
    elif args.comando == "rec":
        if(not args.o or not args.i):
            print("recuperar malformado digite python3 client.py -h para ajuda.")
            exit(1) 
        s.rec(nome=args.i, saida=args.o)
    else:
        raise ClientExceptions(1)
except ClientExceptions as e:
    print(e)
    exit(1)
except Exception as e:
    print("Erro não tratado:")
    print(e)
    exit(1)
