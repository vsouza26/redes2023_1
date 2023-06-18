import socket
import os
from multiprocessing import Process  
from .stream_handler import StreamHandler,StreamType,StreamError
from .stream_handler.stream_socket_utils import * 
import os

class MinionSocketError (Exception):
    def __init__(self, typeError:int = 0, cmd:str = "") -> None:
        banner = f"[MinionSocketError {typeError}] "
        self.errors = ["Erro não especificado", 
                       "Erro de conexão do socket", 
                       "Comando do servidor não existente: "]
        fnMsg = banner + self.errors[typeError] + cmd
        super().__init__(fnMsg)
        pass

class MinionSocket():
    _addcmd = "0".encode("ascii")
    _listcmd = "1".encode("ascii")
    _modcmd = "2".encode("ascii")
    _rmcmd = "3".encode("ascii")
    _reccmd = "4".encode("ascii")
    _addminioncmd = "9".encode("ascii")
    def __init__(self, ip:str, porta:int, diretorio:str) -> None:
        try:
            os.mkdir(f"./{diretorio}")
        except FileExistsError as e:
            pass
        except Exception as e:
            raise e
        self.diretorio = diretorio
        self.addr = (ip,porta)
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close_connection(self,c:socket):
        c.shutdown(socket.SHUT_RDWR)
        c.close()

    def add_cmd(self) -> None:
        try:
            nome_arq = socket_recv_str(self.c)
            tam_arq = socket_rect_int(self.c) 
            consumer = StreamHandler(caminho=f"./{self.diretorio}/{nome_arq}",streamType=StreamType.Consumer, tam_arq=tam_arq)
            print(f"Tamanho do arquivo: {tam_arq}\nNome do arquivo: {nome_arq}")
            for i in consumer:
                msg = self.c.recv(i)
                print(msg)
                consumer.consume_next(msg, i) 
        except StreamError as e:
            print(e)

    def start_connection(self) -> None:
        self.c.send(self._addminioncmd)
        socket_send_str(self.c, socket.gethostname())
        

    def handle_command(self) -> None:
        while True:
            try:
                cmd = self.c.recv(1)
                if cmd == self._addcmd:
                    print("add comando recebido")
                    self.add_cmd()
                elif cmd == self._rmcmd:
                    print("remove command received")
                    self.RemoveCommand()
                else:
                    raise MinionSocketError(2)
            except MinionSocketError as e:
                print(e)
                raise e

    def connect_to_master(self):
        self.c.connect(self.addr)
        self.start_connection()
        try:
            self.handle_command()
        except MinionSocketError as e:
            raise e
    
    def RemoveCommand(self):
        try:
            nome_arq = socket_recv_str(self.c)
            os.remove(f'./{self.diretorio}/{nome_arq}')
        except:
            print("deu merda aqui")




