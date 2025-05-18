from .transacao import Transacao
from .conta import Conta


class Grafo:
    def __init__(self, contas: list[Conta], transacoes: list[Transacao]):
        self.contas = contas.copy()        
        self.transacoes = transacoes.copy()

    def addConta(self, conta: Conta):
        if conta not in self.contas:
            self.contas.append(conta)
            return True
        return False

    def addTransacao(self, transacao: Transacao):
        ids_contas = {conta.id for conta in self.contas}  
        if (
            transacao.id_origem in ids_contas
            and transacao.id_destino in ids_contas
        ):
            self.transacoes.append(transacao)
            return True
        return False

    def getVizinhos(self, conta: Conta):
        vizinhos = []
        if conta not in self.contas:
            return vizinhos

        for transacao in self.transacoes:
            if transacao.id_origem == conta.id:
                vizinho = next(
                    (
                        conta_vizinha
                        for conta_vizinha in self.contas
                        if conta_vizinha.id == transacao.id_destino
                    ),
                    None
                )
                if vizinho and vizinho not in vizinhos:
                    vizinhos.append(vizinho)

            elif transacao.id_destino == conta.id:
                vizinho = next(
                    (
                        conta_vizinha
                        for conta_vizinha in self.contas
                        if conta_vizinha.id == transacao.id_origem
                    ),
                    None
                )
                if vizinho and vizinho not in vizinhos:
                    vizinhos.append(vizinho)
        return vizinhos
