import time
import pandas as pd
from algorithms.anomalias import hubs_recebimento
from interface.svg_utils import desenhar_grafo_svg

def exibir_hubs_recebimento(grafo, st):
    limite = st.number_input("Limite mínimo de origens únicas", min_value=1, value=10)
    inicio = time.time()
    hubs = hubs_recebimento(grafo, limite=limite)
    tempo_exec = time.time() - inicio
    st.write(f"Total de hubs de recebimento: {len(hubs)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(E), onde E = número de arestas")
    st.dataframe(pd.DataFrame([[no.id, qtd] for no, qtd in hubs], columns=["ID", "Qtd Origens Únicas"]))
    if hubs:
        idx = st.number_input("Visualizar hub de índice:", min_value=0, max_value=len(hubs)-1, value=0)
        no, _ = hubs[idx]
        origens = set(a.origem.id for a in no.transacoes_entrada)
        arestas = [(orig, no.id) for orig in origens]
        svg = desenhar_grafo_svg([no.id] + list(origens), arestas, destaque=[no.id])
        st.markdown(svg, unsafe_allow_html=True) 