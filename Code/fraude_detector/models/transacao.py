from datetime import datetime


class Transacao:
    def __init__(
            self,
            id: int,
            valor: float,
            data: datetime,
            tipo: str,
            id_origem: int,
            id_destino: int
    ):
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.data = data
        self.id_origem = id_origem
        self.id_destino = id_destino
