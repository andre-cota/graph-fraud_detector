import time
from services.importador_csv import importar_transacoes_csv, importar_transacoes_csv_v3

CAMINHO_CSV_KAGGLE = 'data/bs140513_032310.csv'
CAMINHO_CSV_NOVO = 'data/fraud_detection.csv'

def testar_kaggle():
    print('Iniciando importação do CSV Kaggle...')
    inicio = time.time()
    grafo = importar_transacoes_csv(CAMINHO_CSV_KAGGLE)
    fim = time.time()
    tempo_execucao = fim - inicio
    print(f'Importação concluída em {tempo_execucao:.2f} segundos.')
    print(f'Total de nós (contas e comerciantes): {len(grafo.nos)}')
    print(f'Total de arestas (transações): {len(grafo.arestas)}')
    total_fraudes = sum(1 for a in grafo.arestas if a.is_fraude)
    print(f'Total de transações fraudulentas: {total_fraudes}')
    print(f'Percentual de fraudes: {(total_fraudes/len(grafo.arestas)*100):.2f}%')

def testar_novo():
    print('\nIniciando importação do CSV Novo...')
    inicio = time.time()
    grafo = importar_transacoes_csv_v3(CAMINHO_CSV_NOVO)
    fim = time.time()
    tempo_execucao = fim - inicio
    print(f'Importação concluída em {tempo_execucao:.2f} segundos.')
    print(f'Total de nós (device_type e merchant_type): {len(grafo.nos)}')
    print(f'Total de arestas (transações): {len(grafo.arestas)}')
    total_fraudes = sum(1 for a in grafo.arestas if a.is_fraude)
    print(f'Total de transações fraudulentas: {total_fraudes}')
    print(f'Percentual de fraudes: {(total_fraudes/len(grafo.arestas)*100):.2f}%')

if __name__ == '__main__':
    testar_kaggle()
    testar_novo() 