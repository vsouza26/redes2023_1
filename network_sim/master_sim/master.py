import socket
addr = ("", 9999)
try:
    s = socket.create_server(addr, family=socket.AF_INET)
    string_tst = "Olá do servidor".encode()
    s.listen(10)
    print("Servidor está ouvindo")
    while True:
        c, addr = s.accept()
        c.send(string_tst)
        c.close()
        break
except socket.error as e:
    print("Houve um erro na geração do socket")
    print(e)
