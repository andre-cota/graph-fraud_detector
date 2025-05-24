class Transacao:
    def __init__(self, id_transacao, conta_origem, conta_destino, valor, tipo, timestamp):
        self.id = id_transacao
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor = valor
        self.tipo = tipo
        self.timestamp = timestamp

    def __str__(self):
        return f"Transacao({self.id}, {self.conta_origem.id} -> {self.conta_destino.id}, R${self.valor:.2f}, {self.tipo})"
