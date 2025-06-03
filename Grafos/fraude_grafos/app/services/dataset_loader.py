import csv
from pathlib import Path
import sys
from app.models.conta import Conta
from app.models.transacao import Transacao
from app.services.graph_builder import GraphBuilder

projeto_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(projeto_root))


class DatasetLoader:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.contas = {}
        self.transacoes = []
        self.grafo = {}  

    def _adicionar_aresta(self, origem_id, destino_id):
        if origem_id not in self.grafo:
            self.grafo[origem_id] = []
        self.grafo[origem_id].append(destino_id)

    def carregar_dados_e_cria_grafo(self):
        """Carrega dados e constrói o grafo simultaneamente"""
        try:
           
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                total_linhas = sum(1 for _ in f)
            linhas_processar = max(1, int(total_linhas * 0.01))

            print(f"[INFO] Total de linhas: {total_linhas}")
            print(f"[INFO] Processando {linhas_processar} linhas (50% dos dados)")

            with open(self.caminho_arquivo, newline='', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile)
                for idx, linha in enumerate(leitor):
                    if idx >= linhas_processar:
                        break

                    # Extrai dados da linha
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
                    transacao = Transacao(
                        id_transacao,
                        conta_origem,
                        conta_destino,
                        valor,
                        tipo,
                        timestamp
                    )
                    self.transacoes.append(transacao)

                    # Adiciona aresta ao grafo durante o processamento
                    self._adicionar_aresta(id_origem, id_destino)

                    # Associa transação às contas
                    conta_origem.adicionar_transacao_saida(transacao)
                    conta_destino.adicionar_transacao_entrada(transacao)

                    if idx % 1000 == 0:
                        print(f"[INFO] Processadas {idx}/{linhas_processar} linhas...")
                        print(f"[INFO] Grafo atual: {len(self.grafo)} vértices")

            print(
                f"[INFO] Carregadas {len(self.contas)} contas e "
                f"{len(self.transacoes)} transações."
            )
            print(f"[INFO] Grafo final: {len(self.grafo)} vértices")

            builder = GraphBuilder(self.contas, self.transacoes)
            builder.construir_grafo()

            return self.contas, self.transacoes, builder

        except FileNotFoundError:
            print(f"[ERRO] Arquivo não encontrado: {self.caminho_arquivo}")
            raise
        except Exception as e:
            print(f"[ERRO] Erro ao carregar dados: {str(e)}")
            raise

    def carregar_dados(self):
        try:
            # Conta total de linhas para calcular 50%
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                total_linhas = sum(1 for _ in f)
            linhas_processar = max(1, int(total_linhas * 0.01))

            print(f"[INFO] Total de linhas: {total_linhas}")
            print(f"[INFO] Processando {linhas_processar} linhas (50% dos dados)")

            with open(self.caminho_arquivo, newline='', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile)
                for idx, linha in enumerate(leitor):
                    if idx >= linhas_processar:
                        break

                    # Extrai dados da linha
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
                    transacao = Transacao(
                        id_transacao,
                        conta_origem,
                        conta_destino,
                        valor,
                        tipo,
                        timestamp
                    )
                    self.transacoes.append(transacao)

                    # Associa transação às contas
                    conta_origem.adicionar_transacao_saida(transacao)
                    conta_destino.adicionar_transacao_entrada(transacao)

                    if idx % 1000 == 0:
                        print(f"[INFO] Processadas {idx}/{linhas_processar} linhas...")

            print(
                f"[INFO] Carregadas {len(self.contas)} contas e "
                f"{len(self.transacoes)} transações."
            )

            return self.contas, self.transacoes

        except FileNotFoundError:
            print(f"[ERRO] Arquivo não encontrado: {self.caminho_arquivo}")
            raise
        except Exception as e:
            print(f"[ERRO] Erro ao carregar dados: {str(e)}")
            raise

    def get_grafo(self):
        """Retorna o grafo construído"""
        return self.grafo

    def get_vizinhos(self, id_conta):
        """Retorna os vizinhos de uma conta no grafo"""
        return self.grafo.get(id_conta, [])
