import time
import pandas as pd
from algorithms.anomalias import pares_recorrentes
from interface.svg_utils import desenhar_grafo_svg

def exibir_pares_recorrentes(grafo, st):
    inicio = time.time()
    limite = st.number_input("Limite mínimo de transações entre o par", min_value=2, value=3)
    pares = pares_recorrentes(grafo, limite=limite)
    tempo_exec = time.time() - inicio
    st.write(f"Total de pares recorrentes: {len(pares)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(E), onde E = número de transações (arestas)")
    st.dataframe(pd.DataFrame(pares, columns=["Origem", "Destino", "Qtd Transações"]))
    if pares:
        idx = st.number_input("Visualizar par de índice:", min_value=0, max_value=len(pares)-1, value=0)
        origem, destino, _ = pares[idx]
        nos_par = [origem, destino]
        arestas_par = [(origem, destino)]
        svg = desenhar_grafo_svg(nos_par, arestas_par, destaque=nos_par)
        st.markdown(svg, unsafe_allow_html=True) 