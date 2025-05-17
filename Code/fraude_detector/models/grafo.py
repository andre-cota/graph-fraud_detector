from transacao import Transacao
from conta import Conta
class Grafo:
    def __init__(self, conta: list[Conta], transacao: list[Transacao]):
        self.conta = []
        self.transacao= []