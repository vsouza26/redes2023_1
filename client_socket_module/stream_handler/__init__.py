import os
from enum import Enum

class StreamType(Enum):
    Generator = 0
    Pipe = 1
    Consumer = 2

class StreamError(Exception):
    """Erros relacionados a classe StreamHandler"""
    def __init__(self, typeError:int = 0) -> None:
        banner = "[StreamError {}] ".format(typeError)
        self.errors = ["Erro não especificado",
                       "Erro de inserção",
                       "Erro ao tentar encontrar arquivo",
                       "Erro pois arquivo já existe (o stream é do tipo consumer mesmo?)",
                       "Erro ao criar a classe (o tipo de stream é um tipo válido)?",
                       "Erro ao tentar criar consumer (o tamanho do consumer foi especificado?)",]
        finalMsg = banner + self.errors[typeError]
        super().__init__(finalMsg)

class StreamEnd(Exception):
    def __init__(self):
        super().__init__("fim da stream")

class StreamHandler():
    """Classe para lidar com geração, piping e consumo de stream"""
    def __init__(self, *, tamBuffer:int = 4096, caminho:str = "", streamType:StreamType, tam_arq:int=0) -> None:
        try:
            self.streamType = streamType
            if (self.streamType is StreamType.Consumer or self.streamType is StreamType.Generator):
                try:
                    if self.streamType is StreamType.Generator:
                        try:
                            self.fileSize = os.path.getsize(caminho)
                            self.tamBuffer = tamBuffer 
                            self.fds = open(caminho, "rb")
                            self.readFromFile = 0
                            return
                        except FileNotFoundError as e:
                            raise StreamError(2)
                    else:
                        try:
                            if tam_arq == 0:
                                raise StreamError(5)
                            self.fds = open(caminho, "xb")
                            self.tamBuffer = tamBuffer 
                            self.fileSize = tam_arq 
                            self.readFromFile = 0
                            return
                        except FileExistsError as e:
                           raise StreamError(3) 
                        except StreamError as e:
                            raise e
                except Exception as e:
                    raise (e) 
            if self.streamType is not StreamType.Pipe\
                    and self.streamType is not StreamType.Generator\
                    and self.streamType is not StreamType.Consumer:
                raise StreamError(4)
            self.tamBuffer = tamBuffer 
            self.readFromFile = 0
            self.fileSize = tam_arq
        except StreamError as e:
            raise e

    def __iter__(self):
        return self
    
    def _size_remaining(self) -> None:
        return self.fileSize-self.readFromFile

    def size_next_buffer(self):
        return self.tamBuffer if self._size_remaining()%self.tamBuffer == 0 else self._size_remaining()%self.tamBuffer

    def consume_next(self, buffer:bytes, tam:int):
        bufferArray = bytearray(buffer)
        bufferArray = bufferArray[0:tam]
        for i in bufferArray:
            self.fds.write(int.to_bytes(i, 1, 'little'))

    def send_next(self, tam_a_enviar) -> None:
        try:
            if (tam_a_enviar <= 0):
                raise StreamEnd
            return self.fds.read(tam_a_enviar)
        except StreamEnd as e:
            raise e
     
    def __next__(self):
        try:
            file_remaining = self._size_remaining()
            print(f"file_remaining: {file_remaining}")
            if (file_remaining <= 0):
                raise StreamEnd
            sizeToRead = self.size_next_buffer() 
            self.readFromFile += sizeToRead
            return sizeToRead
        except StreamEnd:
            if hasattr(self, "fds"):
               self.fds.close()
            raise StopIteration()


