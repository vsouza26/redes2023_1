import socket
from .stream_handler import StreamHandler, StreamType
from .stream_handler.stream_socket_utils import *
class ClientSocketError (Exception):
    def __init__(self, typeError:int = 0):
        banner = f"[ClientSocketError {typeError}] "
        self.error =  ["Erro não especificado", "Erro de conexão do socket"] 
        fnMsg = banner + self.error[typeError]
        super().__init__(fnMsg)

class ClientSocket():
    _addcmd = "0".encode("ascii")
    _listcmd = "1".encode("ascii")
    _modcmd = "2".encode("ascii")
    _rmcmd = "3".encode("ascii")
    _reccmd = "4".encode("ascii")
    def __init__(self, ip:int, port:int) -> None: 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,port)
    
    def connect(self):
        try:
            self.s.connect(self.addr)
        except socket.error as e:
            raise ClientSocketError(1)
    
    def shtdnw_close(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def add(self, caminho:str, num_repl:int) -> None:
        self.s.send(self._addcmd)
        streamFile = StreamHandler(streamType=StreamType.Generator, caminho=caminho)
        print(caminho)
        print(streamFile.fileSize)
        nome_arq = caminho.split("/")[-1]
        socket_send_str(self.s, nome_arq)
        socket_send_int(self.s, streamFile.fileSize)
        socket_send_int(self.s, num_repl)
        for i in streamFile:
            self.s.send(streamFile.send_next(i))
        self.shtdnw_close()

    def rem(self, nome):
        self.s.send(self._rmcmd)
        socket_send_str(self.s, nome)

    def rec(self, nome, saida):
        self.s.send(self._reccmd)
        socket_send_str(self.s, nome)
        tam = socket_rect_int(self.s)
        if(not tam):
            print("Arquivo não encontrado")
            return
        sh =  StreamHandler(caminho=saida, tam_arq=tam, streamType=StreamType.Consumer)
        for i in sh:
            sh.consume_next(self.s.recv(i), i)
        self.shtdnw_close()

    def list(self):
        self.s.send(self._listcmd)
        lista = []
        tam_lista = socket_rect_int(self.s)
        for i in range(0,tam_lista):
            lista.append(socket_recv_str(self.s))
        print(lista)
        self.shtdnw_close()

    def mod(self, caminho:str, num_repl:int=1):
        
        self.s.send(self._modcmd)
        #streamFile = StreamHandler(streamType=StreamType.Generator, caminho=caminho)
        nome_arq = caminho.split("/")[-1]
        print(caminho)
        #print(streamFile.fileSize)
        print(nome_arq)
        print(num_repl)        
        socket_send_str(self.s, nome_arq)
        #socket_send_int(self.s, streamFile.fileSize)
        socket_send_int(self.s, num_repl)
        #for i in streamFile:
            #self.s.send(streamFile.send_next(i))
        self.shtdnw_close()

        

