from services.importador_csv import importar_transacoes_csv, importar_transacoes_csv_v3, importar_transacoes_csv_v2
from algorithms.detecao_ciclos import encontrar_ciclos, encontrar_ciclos_fraude
from algorithms.anomalias import nos_com_muitos_envios, nos_com_muitos_recebimentos, transacoes_valor_alto, nos_com_burst_transacoes, transacoes_outliers, ranking_nos_ativos, hubs_envio, hubs_recebimento, encontrar_clusters, pares_recorrentes

CAMINHO_CSV_KAGGLE = 'data/bs140513_032310.csv'
CAMINHO_CSV_NOVO = 'data/fraud_detection.csv'
CAMINHO_CSV_V2 = 'data/paysim.csv'
CAMINHO_CSV_V4 = 'data/dataset_teste_fraude.csv'

def rodar_algoritmos(grafo, nome_dataset):
    print(f'\n==============================')
    print(f'Análise para: {nome_dataset}')
    print(f'==============================')
    print(f'Total de nós: {len(grafo.nos)}')
    print(f'Total de arestas: {len(grafo.arestas)}')
    total_fraudes = sum(1 for a in grafo.arestas if a.is_fraude)
    print(f'Total de transações fraudulentas: {total_fraudes}')
    print(f'Percentual de fraudes: {(total_fraudes/len(grafo.arestas)*100):.2f}%')

    print('\n--- Detecção de Ciclos (qualquer transação) ---')
    ciclos = encontrar_ciclos(grafo, limite_tamanho=6, tamanho_min=3)
    print(f'Total de ciclos encontrados: {len(ciclos)}')
    for i, ciclo in enumerate(ciclos[:5]):
        print(f'Ciclo {i+1}: {ciclo}')
    if len(ciclos) > 5:
        print('...')

    print('\n--- Detecção de Ciclos (apenas fraudes) ---')
    ciclos_fraude = encontrar_ciclos_fraude(grafo, limite_tamanho=6, tamanho_min=3)
    print(f'Total de ciclos fraudulentos encontrados: {len(ciclos_fraude)}')
    for i, ciclo in enumerate(ciclos_fraude[:5]):
        print(f'Ciclo Fraude {i+1}: {ciclo}')
    if len(ciclos_fraude) > 5:
        print('...')

    print('\n--- Nós com muitos envios ---')
    nos_envio = nos_com_muitos_envios(grafo, limite=20)
    for no in nos_envio[:5]:
        print(f'No {no.id} enviou {len(no.transacoes_saida)} transações')
    if len(nos_envio) > 5:
        print('...')

    print('\n--- Nós com muitos recebimentos ---')
    nos_receb = nos_com_muitos_recebimentos(grafo, limite=20)
    for no in nos_receb[:5]:
        print(f'No {no.id} recebeu {len(no.transacoes_entrada)} transações')
    if len(nos_receb) > 5:
        print('...')

    print('\n--- Transações de valor alto ---')
    transacoes_altas = transacoes_valor_alto(grafo, valor_minimo=10000)
    for aresta in transacoes_altas[:5]:
        print(f'{aresta.origem.id} -> {aresta.destino.id} | Valor: {aresta.valor}')
    if len(transacoes_altas) > 5:
        print('...')

    print('\n--- Burst de envios em 24h (>=10 transações) ---')
    bursts_envio = nos_com_burst_transacoes(grafo, tipo='envio', janela_tempo_horas=24, limite=10)
    print(f'Total de bursts de envio encontrados: {len(bursts_envio)}')
    for no, qtd, data_ini, data_fim in bursts_envio[:5]:
        print(f'No {no.id} enviou {qtd} transações entre {data_ini} e {data_fim}')
    if len(bursts_envio) > 5:
        print('...')

    print('\n--- Burst de recebimentos em 24h (>=10 transações) ---')
    bursts_receb = nos_com_burst_transacoes(grafo, tipo='recebimento', janela_tempo_horas=24, limite=10)
    print(f'Total de bursts de recebimento encontrados: {len(bursts_receb)}')
    for no, qtd, data_ini, data_fim in bursts_receb[:5]:
        print(f'No {no.id} recebeu {qtd} transações entre {data_ini} e {data_fim}')
    if len(bursts_receb) > 5:
        print('...')

    print('\n--- Outliers globais (valor muito acima da média do sistema) ---')
    outliers_globais = transacoes_outliers(grafo, n_std=3, por_no=False)
    print(f'Total de outliers globais encontrados: {len(outliers_globais)}')
    for aresta in outliers_globais[:5]:
        print(f'{aresta.origem.id} -> {aresta.destino.id} | Valor: {aresta.valor}')
    if len(outliers_globais) > 5:
        print('...')

    print('\n--- Outliers por nó (envio) ---')
    outliers_por_no_envio = transacoes_outliers(grafo, n_std=3, por_no=True, tipo='envio')
    for aresta in outliers_por_no_envio[:5]:
        print(f'{aresta.origem.id} -> {aresta.destino.id} | Valor: {aresta.valor}')
    if len(outliers_por_no_envio) > 5:
        print('...')

    print('\n--- Outliers por nó (recebimento) ---')
    outliers_por_no_receb = transacoes_outliers(grafo, n_std=3, por_no=True, tipo='recebimento')
    for aresta in outliers_por_no_receb[:5]:
        print(f'{aresta.origem.id} -> {aresta.destino.id} | Valor: {aresta.valor}')
    if len(outliers_por_no_receb) > 5:
        print('...')

    print('\n--- Ranking de nós mais ativos (envio) ---')
    ranking_envio = ranking_nos_ativos(grafo, tipo='envio', top_n=5)
    for no, qtd in ranking_envio:
        print(f'No {no.id} enviou {qtd} transações')

    print('\n--- Ranking de nós mais ativos (recebimento) ---')
    ranking_receb = ranking_nos_ativos(grafo, tipo='recebimento', top_n=5)
    for no, qtd in ranking_receb:
        print(f'No {no.id} recebeu {qtd} transações')

    print('\n--- Hubs de envio (>=10 destinos únicos) ---')
    hubs_env = hubs_envio(grafo, limite=10)
    print(f'Total de hubs de envio encontrados: {len(hubs_env)}')
    for no, qtd_dest in hubs_env[:5]:
        print(f'No {no.id} enviou para {qtd_dest} destinos únicos')
    if len(hubs_env) > 5:
        print('...')

    print('\n--- Hubs de recebimento (>=10 origens únicas) ---')
    hubs_rec = hubs_recebimento(grafo, limite=10)
    print(f'Total de hubs de recebimento encontrados: {len(hubs_rec)}')
    for no, qtd_ori in hubs_rec[:5]:
        print(f'No {no.id} recebeu de {qtd_ori} origens únicas')
    if len(hubs_rec) > 5:
        print('...')

    print('\n--- Clusters (componentes fortemente conectados, >=3 nós) ---')
    clusters = encontrar_clusters(grafo, tamanho_min=3)
    print(f'Total de clusters encontrados: {len(clusters)}')
    for i, cluster in enumerate(clusters[:5]):
        print(f'Cluster {i+1} (tamanho {len(cluster)}): {[no.id for no in cluster]}')
    if len(clusters) > 5:
        print('...')

    print('\n--- Pares recorrentes (>=3 transações entre o mesmo par) ---')
    pares = pares_recorrentes(grafo, limite=3)
    print(f'Total de pares recorrentes encontrados: {len(pares)}')
    for i, (origem, destino, qtd) in enumerate(pares[:5]):
        print(f'Par {i+1}: {origem} -> {destino} ({qtd} transações)')
    if len(pares) > 5:
        print('...')

def main():
    grafo_kaggle = importar_transacoes_csv(CAMINHO_CSV_KAGGLE)
    rodar_algoritmos(grafo_kaggle, '1° - Fraud Detection on Bank Payments')

    grafo_teste = importar_transacoes_csv(CAMINHO_CSV_V4)
    rodar_algoritmos(grafo_teste, '2° - Dataset de Teste')

    grafo_novo = importar_transacoes_csv_v3(CAMINHO_CSV_NOVO)
    rodar_algoritmos(grafo_novo, '3° - Fraud Detection in Transactions Dataset')

    grafo_v2 = importar_transacoes_csv_v2(CAMINHO_CSV_V2)
    rodar_algoritmos(grafo_v2, '4° - Novo Formato com Campos Adicionais')

if __name__ == '__main__':
    main()
