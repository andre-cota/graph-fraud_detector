import csv
from collections import defaultdict
from app.models.conta import Conta
from app.models.transacao import Transacao

class DatasetLoader:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.contas = {} 
        self.transacoes = []
        
    def carregar_dados(self):
        with open(self.caminho_arquivo, newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            for linha in leitor:
                id_origem = linha['nameOrig']
                id_destino = linha['nameDest']
                valor = float(linha['amount'])
                tipo = linha['type']
                timestamp = linha['step']
                id_transacao = f"{id_origem}_{id_destino}_{timestamp}"

                # Cria contas se não existirem
                if id_origem not in self.contas:
                    self.contas[id_origem] = Conta(id_origem)
                if id_destino not in self.contas:
                    self.contas[id_destino] = Conta(id_destino)

                conta_origem = self.contas[id_origem]
                conta_destino = self.contas[id_destino]

                # Cria transação
                transacao = Transacao(id_transacao, conta_origem, conta_destino, valor, tipo, timestamp)
                self.transacoes.append(transacao)

                # Associa transação às contas
                conta_origem.adicionar_transacao_saida(transacao)
                conta_destino.adicionar_transacao_entrada(transacao)

        print(f"[INFO] Carregadas {len(self.contas)} contas e {len(self.transacoes)} transações.")
        return self.contas, self.transacoes


    def get_contas(self):
        return self.contas

    def get_transacoes(self):
        return self.transacoes
