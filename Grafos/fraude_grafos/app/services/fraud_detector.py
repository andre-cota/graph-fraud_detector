import json
import os

class FraudeDetector:
    def __init__(self, contas, transacoes):
        self.contas = contas  
        self.transacoes = transacoes
        self.contas_suspeitas = set()
        self.transacoes_suspeitas = []

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

    def aplicar_regras(self):
        self.detectar_transacoes_suspeitas()
        self.detectar_transacoes_em_cascata()
        self.detectar_ciclos()

    def get_contas_suspeitas(self):
        return list(self.contas_suspeitas)

    def get_transacoes_suspeitas(self):
        return self.transacoes_suspeitas

    def exportar_resultados_json(self, caminho_saida='utils/contas_suspeitas.json'):
        
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        dados = []
        for conta in self.contas.values():
            dados.append({
                "id": conta.id,
                "pontuacao": conta.pontuacao,
                "risco": conta.get_risco(),
                "nivel_risco": conta.get_nivel_risco(),
                "qtd_transacoes_saida": len(conta.transacoes_saida),
                "qtd_transacoes_entrada": len(conta.transacoes_entrada),
            })
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)