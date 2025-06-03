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
        # Inicializa o grafo com todas as contas
        for conta in self.contas.values():
            self.grafo[conta.id] = []

        # Adiciona as conexões
        for transacao in self.transacoes:
            origem_id = transacao.conta_origem.id
            destino_id = transacao.conta_destino.id
            self.grafo[origem_id].append(destino_id)
        
        print(f"Grafo construído com {len(self.grafo)} contas")
        return self

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
