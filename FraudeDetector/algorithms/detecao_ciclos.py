from domain.grafo import Grafo, No

def padronizar_ciclo(ciclo):
    # Garante que o ciclo sempre começa pelo menor id (para evitar duplicidade)
    min_idx = ciclo.index(min(ciclo))
    ciclo_pad = ciclo[min_idx:] + ciclo[:min_idx]
    return tuple(ciclo_pad)

def encontrar_ciclos(grafo: Grafo, limite_tamanho=6, tamanho_min=3):
    ciclos = set()

    def dfs(no_atual, caminho, visitados_local):
        if len(caminho) > limite_tamanho:
            return
        for aresta in no_atual.transacoes_saida:
            prox_no = aresta.destino
            if prox_no.id in caminho:
                ciclo = caminho[caminho.index(prox_no.id):] + [prox_no.id]
                if tamanho_min <= len(ciclo) <= limite_tamanho + 1:
                    ciclo_pad = padronizar_ciclo(ciclo)
                    ciclos.add(ciclo_pad)
            elif prox_no.id not in visitados_local:
                dfs(prox_no, caminho + [prox_no.id], visitados_local | {prox_no.id})

    for no in grafo.nos:
        dfs(no, [no.id], {no.id})
    return [list(c) for c in ciclos]


def encontrar_ciclos_fraude(grafo: Grafo, limite_tamanho=6, tamanho_min=3):
    ciclos = set()

    def dfs(no_atual, caminho, visitados_local):
        if len(caminho) > limite_tamanho:
            return
        for aresta in no_atual.transacoes_saida:
            if not aresta.is_fraude:
                continue
            prox_no = aresta.destino
            if prox_no.id in caminho:
                ciclo = caminho[caminho.index(prox_no.id):] + [prox_no.id]
                if tamanho_min <= len(ciclo) <= limite_tamanho + 1:
                    ciclo_pad = padronizar_ciclo(ciclo)
                    ciclos.add(ciclo_pad)
            elif prox_no.id not in visitados_local:
                dfs(prox_no, caminho + [prox_no.id], visitados_local | {prox_no.id})

    for no in grafo.nos:
        dfs(no, [no.id], {no.id})
    return [list(c) for c in ciclos]
