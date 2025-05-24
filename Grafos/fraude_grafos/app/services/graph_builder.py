class GraphBuilder:
    def __init__(self, contas, transacoes):
        """
        contas: dict de objetos Conta (id -> Conta)
        transacoes: lista de objetos Transacao
        """
        self.contas = contas
        self.transacoes = transacoes
        self.grafo = {} 

    def construir_grafo(self):
        """
        Constrói o grafo direcionado a partir das transações.
        """
        for transacao in self.transacoes:
            origem_id = transacao.conta_origem.id
            destino_id = transacao.conta_destino.id

            if origem_id not in self.grafo:
                self.grafo[origem_id] = []

            self.grafo[origem_id].append(destino_id)

    def get_vizinhos(self, id_conta):
        """
        Retorna os nós vizinhos (contas de destino) a partir de uma conta.
        """
        return self.grafo.get(id_conta, [])

    def get_grafo(self):
        """
        Retorna o grafo completo (dicionário de adjacência).
        """
        return self.grafo

    def exibir_grafo(self):
        """
        Exibe o grafo no terminal de forma legível.
        """
        print("Grafo de Transações:")
        for origem, destinos in self.grafo.items():
            print(f"{origem} -> {', '.join(destinos)}")
