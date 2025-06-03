import json
import os
import random
import networkx as nx
import matplotlib.pyplot as plt

class FraudeDetector:
    def __init__(self, grafo, transacoes):
        self.grafo = grafo
        self.transacoes = transacoes
        self.contas = {}
        self.contas_suspeitas = set()
        self.transacoes_suspeitas = []

    def aplicar_regras(self):
        self.detectar_transacoes_suspeitas_grafo()
        self.detectar_transacoes_em_cascata_grafos()
        self.detectar_ciclos_grafos()

        print(f"\nTotal de transações suspeitas: {len(self.transacoes_suspeitas)}")
        print(f"Total de contas suspeitas: {len(self.contas_suspeitas)}")

    def detectar_transacoes_suspeitas_grafo(self, limite_valor=100000):
        for transacao in self.transacoes:
            if float(transacao.valor) > limite_valor:
                self.transacoes_suspeitas.append(transacao)
                transacao.conta_origem.adicionar_pontuacao(2)
                transacao.conta_destino.adicionar_pontuacao(1)


    def detectar_transacoes_suspeitas(self, limite_valor=100000):
        for transacao in self.transacoes:
            if transacao.valor > limite_valor:
                self.transacoes_suspeitas.append(transacao)
                transacao.conta_origem.adicionar_pontuacao(2)
                transacao.conta_destino.adicionar_pontuacao(1)

    def detectar_transacoes_em_cascata(self, profundidade_max=3):
        visitadas = set()

        def dfs(conta, profundidade, caminho):
            if profundidade > profundidade_max:
                return
            for transacao in conta.transacoes_saida:
                prox = transacao.conta_destino
                if prox in caminho:
                    continue
                novo_caminho = caminho + [prox]
                if profundidade >= 2:
                    self.contas_suspeitas.update(novo_caminho)
                    self.transacoes_suspeitas.append(transacao)
                    for c in novo_caminho:
                        c.adicionar_pontuacao(1)
                dfs(prox, profundidade + 1, novo_caminho)

        for conta in self.contas.values():
            dfs(conta, 1, [conta])

    def detectar_transacoes_em_cascata_grafos(self, profundidade_max=3):
        visitados = set()

        def dfs(conta_id, profundidade):
            if profundidade >= profundidade_max:
                return

            visitados.add(conta_id)
            vizinhos = self.grafo.get_vizinhos(conta_id)

            if len(vizinhos) > 5:  # Muitos vizinhos é suspeito
                self.contas_suspeitas.add(conta_id)

            for vizinho in vizinhos:
                if vizinho not in visitados:
                    self.contas_suspeitas.add(vizinho)
                    dfs(vizinho, profundidade + 1)

        for conta_id in self.grafo.get_grafo().keys():
            if conta_id not in visitados:
                dfs(conta_id, 0)

    def detectar_ciclos(self, limite_ciclo=4):
        """
        Detecta ciclos no grafo de transações entre contas.
        Um ciclo é identificado quando uma sequência de transações retorna à conta de origem.
        O limite_ciclo define o tamanho máximo do caminho a ser considerado como ciclo.
        """
        def dfs(origem, atual, caminho, visitados):
            if len(caminho) > limite_ciclo:
                return
            for transacao in atual.transacoes_saida:
                prox = transacao.conta_destino
                if prox == origem and len(caminho) >= 2:
                    ciclo = caminho + [prox]
                    self.contas_suspeitas.update(ciclo)
                    self.transacoes_suspeitas.append(transacao)
                    for conta in ciclo:
                        conta.adicionar_pontuacao(3)
                    return
                if prox not in visitados:
                    dfs(origem, prox, caminho + [prox], visitados | {prox})

        for conta in self.contas.values():
            dfs(conta, conta, [conta], {conta})

    def detectar_ciclos_grafos(self):
        """Detecta ciclos que podem indicar lavagem de dinheiro"""
        visitados = set()
        stack = set()

        def dfs_ciclo(conta_id):
            if conta_id in stack:
                self.contas_suspeitas.add(conta_id)
                return True

            if conta_id in visitados:
                return False

            visitados.add(conta_id)
            stack.add(conta_id)

            for vizinho in self.grafo.get_vizinhos(conta_id):
                if dfs_ciclo(vizinho):
                    self.contas_suspeitas.add(vizinho)

            stack.remove(conta_id)
            return False

        for conta_id in self.grafo.get_grafo().keys():
            if conta_id not in visitados:
                dfs_ciclo(conta_id)

    def visualizar_grafo_fraudes(self, max_nodes=5000):
        G = nx.DiGraph()
        
        # Seleciona amostra de transações
        transacoes_amostra = self._selecionar_amostra_transacoes(max_nodes)
        
        # Constrói o grafo
        self._construir_grafo_visualizacao(G, transacoes_amostra)
        
        # Configura e exibe a visualização
        self._configurar_visualizacao(G)

    def _selecionar_amostra_transacoes(self, max_nodes):
        if len(self.transacoes_suspeitas) > max_nodes:
            print(f"\nVisualizando amostra de {max_nodes} transações das {len(self.transacoes_suspeitas)} detectadas...")
            return random.sample(self.transacoes_suspeitas, max_nodes)
        return self.transacoes_suspeitas

    def _construir_grafo_visualizacao(self, G, transacoes):
        for transacao in transacoes:
            origem = transacao.conta_origem.id
            destino = transacao.conta_destino.id
            
            G.add_node(origem)
            G.add_node(destino)
            G.add_edge(origem, destino, weight=transacao.valor)

    def _configurar_visualizacao(self, G):
        plt.figure(figsize=(12, 8))
        pos = nx.kamada_kawai_layout(G)

        # Desenha nós
        nx.draw_networkx_nodes(G, pos,
                             node_color='lightblue',
                             node_size=100,
                             alpha=0.6)

        # Desenha arestas
        nx.draw_networkx_edges(G, pos,
                             edge_color='red',
                             arrows=True,
                             arrowsize=10,
                             width=0.5,
                             alpha=0.4)

        # Adiciona labels se houver poucos nós
        if G.number_of_nodes() <= 50:
            self._adicionar_labels(G, pos)

        plt.title(f"Amostra de Transações Suspeitas ({G.number_of_nodes()} nós)")
        plt.axis('off')
        self._adicionar_estatisticas(G)
        plt.show()

    def _adicionar_labels(self, G, pos):
        """Adiciona labels aos nós e arestas"""
        nx.draw_networkx_labels(G, pos, font_size=6)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {k: f'R${v:,.0f}' for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=5)

    def _adicionar_estatisticas(self, G):
        """Adiciona estatísticas ao gráfico"""
        info = (f"Amostra: {G.number_of_nodes()} contas de {len(self.contas_suspeitas)}\n"
                f"Total na amostra: {G.number_of_edges()} transações")
        plt.figtext(0.02, 0.02, info, fontsize=8)

    def exportar_resultados_json(self, caminho_saida='utils/contas_suspeitas.json'):
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        dados = self._preparar_dados_exportacao()
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def _preparar_dados_exportacao(self):
        return [{
            "id": conta.id,
            "pontuacao": conta.pontuacao,
            "risco": conta.get_risco(),
            "nivel_risco": conta.get_nivel_risco(),
            "qtd_transacoes_saida": len(conta.transacoes_saida),
            "qtd_transacoes_entrada": len(conta.transacoes_entrada)
        } for conta in self.contas.values()]

    def get_contas_suspeitas(self):
        return list(self.contas_suspeitas)

    def get_transacoes_suspeitas(self):
        return self.transacoes_suspeitas