import socket
class ClientSocketError (Exception):
    def __init__(self, type:int = 0):
        self.error =  ["Erro 0: Erro não especificado", "Erro 1: Erro de conexão do socket"] 
        super().__init__(self.error[type])
    pass

class ClientSocket():
    def __init__(self, ip:int, port:int): 
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = (ip,port)
    
    def connect(self):
        try:
            self.s.connect(self.addr)
        except socket.error as e:
            raise ClientSocketError(1)
    
    def shtdnw_close(self):
        s.shutdown(socket.SHUT_RDWR)
        s.close()

