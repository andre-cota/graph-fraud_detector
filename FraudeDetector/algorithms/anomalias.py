from domain.grafo import Grafo, No
from datetime import timedelta
import statistics
from collections import defaultdict

def nos_com_muitos_envios(grafo: Grafo, limite=10):
    return [no for no in grafo.nos if len(no.transacoes_saida) > limite]

def nos_com_muitos_recebimentos(grafo: Grafo, limite=10):
    return [no for no in grafo.nos if len(no.transacoes_entrada) > limite]

def transacoes_valor_alto(grafo: Grafo, valor_minimo=10000):
    return [aresta for aresta in grafo.arestas if aresta.valor >= valor_minimo]

def nos_com_burst_transacoes(grafo: Grafo, tipo='envio', janela_tempo_horas=24, limite=10):
    """
    Detecta nós com burst de transações em uma janela de tempo.
    Retorna lista de tuplas: (no, qtd_transacoes, data_inicio, data_fim)
    """
    resultado = []
    janela = timedelta(hours=janela_tempo_horas)
    for no in grafo.nos:
        if tipo == 'envio':
            transacoes = sorted(no.transacoes_saida, key=lambda a: a.data)
        else:
            transacoes = sorted(no.transacoes_entrada, key=lambda a: a.data)
        n = len(transacoes)
        i = 0
        while i < n:
            j = i
            while j < n and (transacoes[j].data - transacoes[i].data) <= janela:
                j += 1
            qtd = j - i
            if qtd >= limite:
                resultado.append((no, qtd, transacoes[i].data, transacoes[j-1].data))
                i = j
            else:
                i += 1
    return resultado

def transacoes_outliers(grafo: Grafo, n_std=3, por_no=False, tipo='envio'):
    """
    Detecta transações outliers por desvio padrão.
    Se por_no=False, faz análise global. Se por_no=True, faz análise por nó (envio ou recebimento).
    Retorna lista de arestas (transações) consideradas outliers.
    """
    outliers = []
    if not por_no:
        valores = [a.valor for a in grafo.arestas]
        if len(valores) < 2:
            return []
        media = statistics.mean(valores)
        std = statistics.stdev(valores)
        limite = media + n_std * std
        outliers = [a for a in grafo.arestas if a.valor > limite]
    else:
        for no in grafo.nos:
            if tipo == 'envio':
                transacoes = no.transacoes_saida
            else:
                transacoes = no.transacoes_entrada
            valores = [a.valor for a in transacoes]
            if len(valores) < 2:
                continue
            media = statistics.mean(valores)
            std = statistics.stdev(valores)
            limite = media + n_std * std
            outliers.extend([a for a in transacoes if a.valor > limite])
    return outliers

def ranking_nos_ativos(grafo: Grafo, tipo='envio', top_n=10):
    """
    Retorna os top_n nós mais ativos em envio ou recebimento de transações.
    Retorna lista de tuplas: (no, quantidade de transações)
    """
    if tipo == 'envio':
        ranking = sorted([(no, len(no.transacoes_saida)) for no in grafo.nos], key=lambda x: x[1], reverse=True)
    else:
        ranking = sorted([(no, len(no.transacoes_entrada)) for no in grafo.nos], key=lambda x: x[1], reverse=True)
    return ranking[:top_n]

def hubs_envio(grafo: Grafo, limite=10):
    """
    Retorna nós que enviam para muitos destinos únicos.
    Lista de tuplas: (no, qtd_destinos_unicos)
    """
    resultado = []
    for no in grafo.nos:
        destinos = set(a.destino.id for a in no.transacoes_saida)
        if len(destinos) >= limite:
            resultado.append((no, len(destinos)))
    return resultado

def hubs_recebimento(grafo: Grafo, limite=10):
    """
    Retorna nós que recebem de muitas origens únicas.
    Lista de tuplas: (no, qtd_origens_unicas)
    """
    resultado = []
    for no in grafo.nos:
        origens = set(a.origem.id for a in no.transacoes_entrada)
        if len(origens) >= limite:
            resultado.append((no, len(origens)))
    return resultado

def encontrar_clusters(grafo: Grafo, tamanho_min=3):
    """
    Encontra clusters (componentes fortemente conectados) usando Kosaraju.
    Retorna lista de clusters (cada cluster é uma lista de nós).
    """
    visitado = set()
    ordem = []
    def dfs1(no):
        visitado.add(no)
        for aresta in no.transacoes_saida:
            if aresta.destino not in visitado:
                dfs1(aresta.destino)
        ordem.append(no)
    for no in grafo.nos:
        if no not in visitado:
            dfs1(no)
    transposto = {no: [] for no in grafo.nos}
    for no in grafo.nos:
        for aresta in no.transacoes_saida:
            transposto[aresta.destino].append(no)
    visitado.clear()
    clusters = []
    def dfs2(no, componente):
        visitado.add(no)
        componente.append(no)
        for vizinho in transposto[no]:
            if vizinho not in visitado:
                dfs2(vizinho, componente)
    for no in reversed(ordem):
        if no not in visitado:
            componente = []
            dfs2(no, componente)
            if len(componente) >= tamanho_min:
                clusters.append(componente)
    return clusters

def pares_recorrentes(grafo: Grafo, limite=3):
    """
    Retorna lista de pares (id_origem, id_destino, quantidade) com transações recorrentes entre si.
    """
    contagem = defaultdict(int)
    for aresta in grafo.arestas:
        par = (aresta.origem.id, aresta.destino.id)
        contagem[par] += 1
    recorrentes = [(origem, destino, qtd) for (origem, destino), qtd in contagem.items() if qtd >= limite]
    recorrentes.sort(key=lambda x: x[2], reverse=True)
    return recorrentes
