import socket
from multiprocessing import Process, Lock,Manager
from .stream_handler import StreamHandler,StreamType  
from .stream_handler.stream_socket_utils import * 

class ServerSocketError (Exception):
    def __init__(self, typeError:int = 0) -> None:
        banner = f"[ServerSocketError {typeError}] "
        self.errors = ["Erro não especificado", "Erro de conexão do socket"]
        fnMsg = banner + self.errors[typeError]
        super().__init__(fnMsg)
        pass

class ServerSocket():
    _addcmd = "0".encode("ascii")
    _listcmd = "1".encode("ascii")
    _modcmd = "2".encode("ascii")
    _rmcmd = "3".encode("ascii")
    _addminioncmd = "9".encode("ascii")
    def __init__(self, ip:int, porta:int) -> None:
        self.reg_list = open("./.registerlist", "a+b")
        self.s = socket.create_server((ip,porta), family=socket.AF_INET)
        self.num_repl = 0 
        self.round_robin = 0

    def close_connection(self,c:socket):
        c.shutdown(socket.SHUT_RDWR)
        c.close()

    def send_header_to_minion(self, header, m:socket):
        for msg in header:
            if type(msg) is str:
                socket_send_str(m, msg)
            elif type(msg) is int:
                socket_send_int(m, msg)
            else:
                m.send(msg)

    def send_to_minion(self, msg, m):
        try:
            m.send(msg)
        except BrokenPipeError as e:
            pass
    
    def existe_em_registro(self, chave:str, decoder:str = 'ascii'):
        self.reg_list.seek(0)
        for line in self.reg_list:
            nome_arq = line.decode(decoder).split(",")[0]
            if chave == nome_arq:
                return True
        return False
        

    def add_cmd(self,c):
        nome_arq = socket_recv_str(c) 
        if self.existe_em_registro(nome_arq):
            self.close_connection(c)
            return
        tam_arq = socket_rect_int(c)
        num_repl = socket_rect_int(c)
        minion_msg = [self._addcmd]
        minion_msg.append(nome_arq)
        minion_msg.append(tam_arq)
        pipe = StreamHandler(streamType=StreamType.Pipe, tam_arq=tam_arq)
        if len(self.minion_list) <= num_repl:
            process_list = [Process(target=self.send_header_to_minion, args=(minion_msg,m)) for (hs,m) in self.minion_list]
            registro = f"{nome_arq},"
            for (hs,m) in self.minion_list:
                registro = registro + hs + ","
            registro = registro + "\n"
            self.reg_list.write(registro.encode('ascii'))
            for p in process_list:
                p.start()
            for p in process_list:
                p.join()
            for j in pipe:
                msg = c.recv(j)
                print(f"Mensagem do client: {msg}")
                #SEND STREAM 
                process_list = [Process(target=self.send_to_minion, args=(msg,m)) for (hs,m) in self.minion_list]
                for p in process_list:
                    p.start()
                for p in process_list:
                    p.join()
        else:
            servers_list = [self.minion_list[i%len(self.minion_list)] for i in range(self.round_robin, num_repl)] 
            registro = f"{nome_arq},"
            for (hs,m) in servers_list:
                registro = registro + hs + ","
                p = Process(target=self.send_header_to_minion, args=(minion_msg,m))
                p.start()
            registro = registro + "\n"
            self.reg_list.write(registro.encode('ascii'))
            for (hs,m) in servers_list:
                p.join()
            for j in pipe:
                msg = c.recv(j)
                for (hs,m) in servers_list:
                    p = Process(target=self.send_to_minion, args=(minion_msg,m))
                    p.start()
                for (hs,m) in servers_list:
                    p.join()

    def list_cmd(self, c:socket):
        self.reg_list.seek(0)
        lista_reg = self.reg_list.read()
        lista_reg = lista_reg.splitlines()
        socket_send_int(len(lista_reg))
        for linha in lista_reg:
            socket_send_str(c, linha)
        self.reg_list.seek(0)

    def mod_cmd(self, c:socket):
        nome_arq = socket_recv_str(c)
        num_repl = socket_rect_int(c)
        minion_msg = [self._modcmd]
        minion_msg.append(nome_arq)
        minion_msg.append(num_repl)

        if not self.existe_em_registro(nome_arq):
            self.close_connection(c)
            return

        
        # Modify the number of replicas for the file in the registry
        #self.update_num_repl_in_registry(nome_arq, num_repl)

        # Send acknowledgment to the client
        c.send("OK".encode("ascii"))

        self.close_connection(c)
    
    def add_minion(self, c:socket, addr):
        hostnameminion = socket_recv_str(c)
        self.minion_list.append((hostnameminion,c))

    def start_server(self):
        self.s.listen(0)
        with Manager() as manager:
            self.minion_list = []
            while True:
                print(self.minion_list)
                c, addr = self.s.accept()
                fmsg = c.recv(1)
                print(fmsg)
                if fmsg == self._addcmd:
                    self.add_cmd(c)
                if fmsg == self._addminioncmd:
                    self.add_minion(c, addr)
                if fmsg == self._listcmd:
                    self.list_cmd(c)
                if fmsg == self._modcmd:
                    self.mod_cmd(c)



