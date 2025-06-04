import time
import pandas as pd
from algorithms.detecao_ciclos import encontrar_ciclos
from interface.svg_utils import desenhar_grafo_svg

def exibir_ciclos(grafo, st):
    inicio = time.time()
    ciclos = encontrar_ciclos(grafo, limite_tamanho=6, tamanho_min=3)
    tempo_exec = time.time() - inicio
    st.write(f"Total de ciclos encontrados: {len(ciclos)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(V + E) por busca, potencialmente exponencial para todos os ciclos (DFS recursivo)")
    st.dataframe(pd.DataFrame(ciclos, columns=["Caminho dos Nós"]))
    if ciclos:
        idx = st.number_input("Visualizar ciclo de índice:", min_value=0, max_value=len(ciclos)-1, value=0)
        ciclo = ciclos[idx]
        nos_ciclo = ciclo[:-1]
        arestas_ciclo = [(nos_ciclo[i], nos_ciclo[i+1]) for i in range(len(nos_ciclo)-1)] + [(nos_ciclo[-1], ciclo[-1])]
        svg = desenhar_grafo_svg(nos_ciclo, arestas_ciclo, destaque=nos_ciclo)
        st.markdown(svg, unsafe_allow_html=True) 