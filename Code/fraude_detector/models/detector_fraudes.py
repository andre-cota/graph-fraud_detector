from .grafo import Grafo


class DetectorFraudes:
    def __init__(self, grafo: Grafo):
        self.grafo = grafo

    def detectar_Ciclos(self, contas: Grafo.contas):
        visitados = set()
        pilha = set()

        def dfs(id_conta):
            visitados.add(id_conta)
            pilha.add(id_conta)

            for vizinho in self.grafo.getVizinhos(id_conta):
                if vizinho not in visitados:
                    if dfs(vizinho):
                        return True
                elif vizinho in pilha:
                    return True #Ciclo detectado
                
            pilha.remove(id_conta)
            return False
        
        for conta in contas:
            if conta.id not in visitados:
                if dfs(conta.id):
                    return True # Ciclo detectado
        return False

    def contas_Suspeitas(self, contas):
        suspeitas = []

        for conta in contas:
            grau_saida = self.grafo.getGrauSaida(conta.id)
            grau_entrada = self.grafo.getGrauEntrada(conta.id)
            vizinhos = self.grafo.getVizinhanca(conta.id)

            if grau_saida > 10 and grau_saida > grau_entrada * 3:
                suspeitas.append(conta)
            elif len(set(vizinhos)) > 10:
                suspeitas.append(conta)

        return suspeitas  # lista de contas suspeitas

    def buscar_Anomalias(self, transacoes: Grafo.transacoes):
        # Anomalias:
        # - Valor muito alto
        # - Transações fora do horário comercial (08:00 às 18:00)

        anomalias = []

        for transacao in transacoes:
            if (
                transacao.valor > 100000 or
                transacao.data.hour < 8 or transacao.data.hour > 18 or
                transacao.tipo not in ['PIX', 'TED', 'DOC']
            ):
                anomalias.append(transacao)

            if anomalias == []:
                print("Nenhuma anomalia encontrada.")
                return

        return anomalias  # lista de transações suspeitas
        

