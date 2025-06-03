import sys
from pathlib import Path
import time

projeto_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(projeto_root))

from app.services.dataset_loader import DatasetLoader
from app.services.fraud_detector import FraudeDetector
from app.services.graph_builder import GraphBuilder
from frontend.visualizador import VisualizadorGrafo

def executar_metodo_antigo():
    tempo_total_inicio = time.time()
    
    try:
        tempo_carga_inicio = time.time()
        loader = DatasetLoader('grafos2025/Grafos/fraude_grafos/app/data/paysim.csv')
        contas, transacoes = loader.carregar_dados()
        tempo_carga = time.time() - tempo_carga_inicio
        
        tempo_grafo_inicio = time.time()
        builder = GraphBuilder(contas, transacoes)
        builder.construir_grafo()
        tempo_grafo = time.time() - tempo_grafo_inicio
        
        tempo_deteccao_inicio = time.time()
        detector = FraudeDetector(builder, transacoes)
        detector.aplicar_regras()
        fraudes_detectadas = detector.get_transacoes_suspeitas()
        tempo_deteccao = time.time() - tempo_deteccao_inicio
        
        visualizador = VisualizadorGrafo()
        visualizador.criar_grafo_fraudes(fraudes_detectadas, amostragem=True)
        print("\nGerando visualização do grafo (amostra)...")
        visualizador.exibir_grafo()
        
        tempo_total = time.time() - tempo_total_inicio
        return tempo_carga, tempo_grafo, tempo_deteccao, tempo_total, len(fraudes_detectadas)
        
    except Exception as e:
        print(f"Erro durante execução: {e}")
        return 0, 0, 0, 0, 0

def executar_metodo_novo():
    """Executa método novo: carrega dados, constrói grafo e detecta fraudes simultaneamente"""
    tempo_total_inicio = time.time()
    
    tempo_carga_inicio = time.time()
    loader = DatasetLoader('grafos2025/Grafos/fraude_grafos/app/data/paysim.csv')
    contas, transacoes, builder = loader.carregar_dados_e_cria_grafo()  # Recebe o builder
    tempo_carga = time.time() - tempo_carga_inicio
    
    tempo_deteccao_inicio = time.time()
    detector = FraudeDetector(builder, transacoes)  # Passa o builder ao invés do grafo
    detector.aplicar_regras()
    fraudes_detectadas = detector.get_transacoes_suspeitas()
    tempo_deteccao = time.time() - tempo_deteccao_inicio
    
    tempo_total = time.time() - tempo_total_inicio
    return tempo_carga, 0, tempo_deteccao, tempo_total, len(fraudes_detectadas)

def executar_comparacao(num_execucao):
    """Executa uma comparação e mostra resultados detalhados"""
    print(f"\n=== EXECUÇÃO #{num_execucao} ===")
    
    print("\n=== MÉTODO ANTIGO ===")
    carga_antigo, grafo_antigo, deteccao_antigo, total_antigo, fraudes_antigo = executar_metodo_antigo()
    print(f"Tempo de carregamento: {carga_antigo:.2f} segundos")
    print(f"Tempo de construção do grafo: {grafo_antigo:.2f} segundos")
    print(f"Tempo de detecção de fraudes: {deteccao_antigo:.2f} segundos")
    print(f"Tempo total: {total_antigo:.2f} segundos")
    print(f"Fraudes detectadas: {fraudes_antigo}")
    
    print("\n=== MÉTODO NOVO ===")
    carga_novo, grafo_novo, deteccao_novo, total_novo, fraudes_novo = executar_metodo_novo()
    print(f"Tempo de processamento: {carga_novo:.2f} segundos")
    print(f"Tempo de detecção de fraudes: {deteccao_novo:.2f} segundos")
    print(f"Tempo total: {total_novo:.2f} segundos")
    print(f"Fraudes detectadas: {fraudes_novo}")
    
    print("\n=== COMPARATIVO DA EXECUÇÃO ===")
    print(f"{'':20} {'Método Antigo':>15} {'Método Novo':>15} {'Diferença':>15}")
    print("-" * 65)
    print(f"{'Carregamento:':20} {carga_antigo:>14.2f}s {carga_novo:>14.2f}s {carga_antigo-carga_novo:>14.2f}s")
    print(f"{'Construção Grafo:':20} {grafo_antigo:>14.2f}s {grafo_novo:>14.2f}s {grafo_antigo:>14.2f}s")
    print(f"{'Detecção Fraudes:':20} {deteccao_antigo:>14.2f}s {deteccao_novo:>14.2f}s {deteccao_antigo-deteccao_novo:>14.2f}s")
    print(f"{'Tempo Total:':20} {total_antigo:>14.2f}s {total_novo:>14.2f}s {total_antigo-total_novo:>14.2f}s")
    
    return {
        'execucao': num_execucao,
        'carga_antigo': carga_antigo,
        'grafo_antigo': grafo_antigo,
        'deteccao_antigo': deteccao_antigo,
        'total_antigo': total_antigo,
        'fraudes_antigo': fraudes_antigo,
        'carga_novo': carga_novo,
        'grafo_novo': grafo_novo,
        'deteccao_novo': deteccao_novo,
        'total_novo': total_novo,
        'fraudes_novo': fraudes_novo
    }


def exibir_resumo(resultados):
    """Exibe apenas o resumo final das execuções"""
    print("\n=== RESULTADOS DAS EXECUÇÕES ===")
    print(f"{'Exec':^5} {'Método Antigo':^12} {'Método Novo':^12} {'Diferença':^10}")
    print("-" * 41)
    
    for r in resultados:
        diferenca = r['total_antigo'] - r['total_novo']
        print(f"{r['execucao']:^5} {r['total_antigo']:>11.2f}s {r['total_novo']:>11.2f}s {diferenca:>9.2f}s")
    
    print("-" * 41)
    media_antigo = sum(r['total_antigo'] for r in resultados) / len(resultados)
    media_novo = sum(r['total_novo'] for r in resultados) / len(resultados)
    diferenca_media = media_antigo - media_novo
    
    print(f"{'Média':^5} {media_antigo:>11.2f}s {media_novo:>11.2f}s {diferenca_media:>9.2f}s")

def main():
    resultados = []
    num_execucoes = 1
    intervalo = 3
    
    print(f"\nIniciando {num_execucoes} execuções com intervalo de {intervalo} segundos...")
    
    for i in range(num_execucoes):
        resultados.append(executar_comparacao(i + 1))
        if i < num_execucoes - 1:
            print(f"\nAguardando {intervalo} segundos para próxima execução...")
            time.sleep(intervalo)
    
    exibir_resumo(resultados)

if __name__ == "__main__":
    main()