from multiprocessing import Lock
class StreamMeta(type):
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]

class StreamHandler(metaclass=StreamMeta):
    def __init__(self, *, bufferSize:int = 4096, caminho:str, preReadBuffer:int = 10) -> None:
        self.caminho = caminho
        self.fds = open(self.caminho, "r")

    def next(self):
        return 




streamhandler1 = StreamHandler("Teste")
streamhandler2 = StreamHandler("PPE")
print(streamhandler1.caminho)
