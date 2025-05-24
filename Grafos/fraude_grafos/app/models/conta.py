class Conta:
    def __init__(self, id_conta: str):
        self.id = id_conta
        self.transacoes_saida = []
        self.transacoes_entrada = []
        self.pontuacao = 0 
        self.risco = 0.0
        self.participa_em_ciclo = False

    def adicionar_transacao_saida(self, transacao):
        self.transacoes_saida.append(transacao)

    def adicionar_transacao_entrada(self, transacao):
        self.transacoes_entrada.append(transacao)

    def adicionar_pontuacao(self, pontos: int):
        self.pontuacao += pontos
        self.calcular_risco()

    def calcular_risco(self):
        if self.pontuacao >= 10:
            self.risco = 1.0
        elif self.pontuacao >= 5:
            self.risco = 0.6
        else:
            self.risco = 0.2

    def get_risco(self) -> float:
        return self.risco

    def get_nivel_risco(self) -> str:
        if self.risco >= 1.0:
            return "Alto"
        elif self.risco >= 0.6:
            return "Médio"
        else:
            return "Baixo"

    def __str__(self):
        return f"Conta({self.id}, Risco: {self.risco:.2f}, Nível: {self.get_nivel_risco()})"
