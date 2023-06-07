import socket
from multiprocessing import Process  
class ServerSocketError (Exception):
    def __init__(self, type:int = 0) -> None:
        self.errors = ["Erro 0: Erro não especificado", "Erro 1: Erro de conexão do socket"]
        super().__init__(self.errors[type])
        pass

class ServerSocket():
    def __init__(self, ip:int, port:int) -> None:
        self.s = socket.create_server((ip,port), family=socket.AF_INET)

    def handle_command(self, c):
        fmsg = c.recv(1)
        fmsg = fmsg.decode("ascii")
        print(fmsg)
        if fmsg == "0":
            len_nome_arq = c.recv(8)
            len_nome_arq = int.from_bytes(len_nome_arq, 'little') 
            nome_arq = c.recv(len_nome_arq)
            nome_arq = nome_arq.decode("ascii") 
            print(nome_arq)
            c.shutdown(socket.SHUT_RDWR)
            c.close()
    
    def start_server(self):
        self.s.listen(256)
        while True:
            c, addr = self.s.accept()
            p = Process(target=self.handle_command, args=(c,))
            p.start()


