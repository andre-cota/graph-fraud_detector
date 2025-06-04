from domain.grafo import Grafo, No

def encontrar_ciclos(grafo: Grafo, limite_tamanho=6, tamanho_min=3):
    ciclos = []

    def dfs(no_atual, caminho, visitados_local):
        if len(caminho) > limite_tamanho:
            return
        for aresta in no_atual.transacoes_saida:
            prox_no = aresta.destino
            if prox_no.id in caminho:
                ciclo = caminho[caminho.index(prox_no.id):] + [prox_no.id]
                if tamanho_min <= len(ciclo) <= limite_tamanho and ciclo not in ciclos:
                    ciclos.append(ciclo)
            elif prox_no.id not in visitados_local:
                dfs(prox_no, caminho + [prox_no.id], visitados_local | {prox_no.id})

    for no in grafo.nos:
        dfs(no, [no.id], {no.id})
    return ciclos


def encontrar_ciclos_fraude(grafo: Grafo, limite_tamanho=6, tamanho_min=3):
    ciclos = []

    def dfs(no_atual, caminho, visitados_local):
        if len(caminho) > limite_tamanho:
            return
        for aresta in no_atual.transacoes_saida:
            if not aresta.is_fraude:
                continue
            prox_no = aresta.destino
            if prox_no.id in caminho:
                ciclo = caminho[caminho.index(prox_no.id):] + [prox_no.id]
                if tamanho_min <= len(ciclo) <= limite_tamanho and ciclo not in ciclos:
                    ciclos.append(ciclo)
            elif prox_no.id not in visitados_local:
                dfs(prox_no, caminho + [prox_no.id], visitados_local | {prox_no.id})

    for no in grafo.nos:
        dfs(no, [no.id], {no.id})
    return ciclos
