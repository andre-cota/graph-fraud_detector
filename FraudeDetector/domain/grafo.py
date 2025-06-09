from datetime import datetime
from typing import List, Optional

class No:
    def __init__(self, id: str, saldo: float = 0.0, tipo_conta: str = ""):
        self.id = id
        self.saldo = saldo
        self.tipo_conta = tipo_conta
        self.transacoes_saida: List['Aresta'] = []
        self.transacoes_entrada: List['Aresta'] = []

    def atualizar_saldo(self, valor: float):
        self.saldo += valor

class Aresta:
    def __init__(self, origem: No, destino: No, valor: float, data: datetime, is_fraude: bool = False):
        self.origem = origem
        self.destino = destino
        self.valor = valor
        self.data = data
        self.is_fraude = is_fraude

    def marcar_fraude(self):
        self.is_fraude = True

class Grafo:
    def __init__(self):
        self.nos: List[No] = []
        self.arestas: List[Aresta] = []

    def adicionar_no(self, no: No):
        self.nos.append(no)

    def buscar_no(self, id: str) -> Optional[No]:
        for no in self.nos:
            if no.id == id:
                return no
        return None

    def adicionar_aresta(self, aresta: Aresta):
        self.arestas.append(aresta)
        aresta.origem.transacoes_saida.append(aresta)
        aresta.destino.transacoes_entrada.append(aresta)