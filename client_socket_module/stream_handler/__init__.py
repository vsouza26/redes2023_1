import os

class StreamError(Exception):
    """Erros relacionados a classe StreamHandler"""
    def __init__(self, typeError:int = 0) -> None:
        banner = "[StreamError {}] ".format(typeError)
        self.errors = ["Erro não especificado",
                       "Erro de inserção"]
        finalMsg = banner + self.errors[typeError]
        super().__init__(finalMsg)

class StreamEnd(Exception):
    def __init__(self):
        super().__init__("fim da stream")

class StreamHandler():
    """Classe para lidar com geração de e consumo de stream"""
    def __init__(self, *, tamBuffer:int = 4096, caminho:str) -> None:
        try:
            self.caminho = caminho
            self.tamBuffer = tamBuffer 
            self.fds = open(self.caminho, "rb")
            self.fileSize = os.path.getsize(caminho)
            self.readFromFile = 0
        except FileNotFoundError as e:
            raise e

    def _sizeRemaining(self) -> None:
        return self.fileSize-self.readFromFile

    def next(self) -> None:
        try:
            fileRemaning = self._sizeRemaining()
            if (fileRemaning <= 0):
                raise StreamEnd
            sizeToRead = self.tamBuffer if fileRemaning%self.tamBuffer == 0 else fileRemaning%self.tamBuffer
            self.readFromFile += sizeToRead
            print("File remaining: {}\nSize to Read: {}".format(fileRemaning, sizeToRead))
            return self.fds.read(sizeToRead)
        except StreamError as e:
            self.fds.close()
            raise e 

s = StreamHandler(caminho="./teste", tamBuffer=5) 
while True:
    try:
        print("::BLOCK::")
        msg = s.next()
        print(msg)
    except StreamError as e:
        print("Houve um erro com a leitura")
    except StreamEnd as e:
        print("Arquivo acabou")
        exit(0)


