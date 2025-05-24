from app.services.dataset_loader import DatasetLoader
from app.services.fraud_detector import FraudeDetector
from app.services.graph_builder import GraphBuilder

def main():
    
    loader = DatasetLoader('data/paysim.csv')
    contas, transacoes = loader.carregar_dados()

    detector = FraudeDetector(contas, transacoes)

    detector.aplicar_regras()

    detector.exportar_resultados_json('utils/contas_suspeitas.json')

    builder = GraphBuilder(contas, transacoes)
    builder.construir_grafo()
    builder.exibir_grafo()

    #print(f"\n{len(detector.get_contas_suspeitas())} contas suspeitas detectadas:")
    #for conta in detector.get_contas_suspeitas():
    #    print(f"- {conta.id}: Risco {conta.get_risco():.2f} ({conta.get_nivel_risco()})")

if __name__ == "__main__":
    main()
