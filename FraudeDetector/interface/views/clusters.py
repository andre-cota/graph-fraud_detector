import time
import pandas as pd
from algorithms.anomalias import encontrar_clusters
from interface.svg_utils import desenhar_grafo_svg

def exibir_clusters(grafo, st):
    inicio = time.time()
    tamanho_min = st.number_input("Tamanho mínimo do cluster", min_value=2, value=3)
    clusters = encontrar_clusters(grafo, tamanho_min=tamanho_min)
    tempo_exec = time.time() - inicio
    st.write(f"Total de clusters encontrados: {len(clusters)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(V + E) para Kosaraju, onde V = nós e E = arestas")
    st.dataframe(pd.DataFrame([[i+1, len(cluster), [no.id for no in cluster]] for i, cluster in enumerate(clusters)], columns=["Cluster", "Tamanho", "IDs dos Nós"]))
    if clusters:
        idx = st.number_input("Visualizar cluster de índice:", min_value=0, max_value=len(clusters)-1, value=0)
        cluster = clusters[idx]
        nos_cluster = [no.id for no in cluster]
        arestas_cluster = []
        for no in cluster:
            for aresta in no.transacoes_saida:
                if aresta.destino in cluster:
                    arestas_cluster.append((no.id, aresta.destino.id))
        svg = desenhar_grafo_svg(nos_cluster, arestas_cluster, destaque=nos_cluster)
        st.markdown(svg, unsafe_allow_html=True) 