import socket
addr = ("", 9999)
try:
    s = socket.create_server(addr, family=socket.AF_INET)
    string_tst = "Olá do servidor".encode()
    s.listen(1)
    print("Servidor está ouvindo")
    while True:
        c, addr = s.accept()
        buffersize = c.recv(8)
        value = int.from_bytes(buffersize, 'little')
        print(value)
        print(f"Socket em comunicação com {addr}")
        buffersize = c.recv(8)
        if len(buffersize) == 0:
            c.shutdown(socket.SHUT_RDWR)
            c.close()
            print("Quer terminar")
except socket.error as e:
    print("Houve um erro na geração do socket")
    print(e)
