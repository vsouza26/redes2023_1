import socket
import argparse
from server_socket_module import ServerSocket, ServerSocketError
try:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--ip", help="Ip da interface em que deve escutar", default="localhost")
    parser.add_argument("--porta", help="Porta em que deve escutar", default=9999)
    args = parser.parse_args()
    s = ServerSocket(args.ip, int(args.porta))
    s.start_server()
except ServerSocketError as e:
    print(e)
