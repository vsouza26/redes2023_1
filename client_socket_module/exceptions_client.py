class ClientExceptions(Exception):
    def __init__(self, type:int = 0):
        self.error = ["ClientException Erro 0: Erro do cliente não específico",
                       "ClientException Erro 1: Erro de seleção de comando"]
        super().__init__(self.error[type])
    pass
