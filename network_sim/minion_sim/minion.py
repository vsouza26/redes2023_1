import socket
import argparse
from minion_socket_module import MinionSocket, MinionSocketError
try:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--ip", help="Ip da interface em que deve escutar", default="localhost")
    parser.add_argument("--porta", help="Porta em que deve escutar", default=9999)
    parser.add_argument("--pasta", help="Pasta onde guardar os arquivos", default="arquivos")
    args = parser.parse_args()
    s = MinionSocket(args.ip, int(args.porta), args.pasta)
    s.connect_to_master()
except MinionSocketError as e:
    print(e)
