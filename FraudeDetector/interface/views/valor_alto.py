import time
import pandas as pd
from algorithms.anomalias import transacoes_valor_alto
from interface.svg_utils import desenhar_grafo_svg

def exibir_valor_alto(grafo, st):
    valor_min = st.number_input("Valor mínimo", min_value=0.0, value=10000.0)
    inicio = time.time()
    trans = transacoes_valor_alto(grafo, valor_minimo=valor_min)
    tempo_exec = time.time() - inicio
    st.write(f"Total de transações acima de {valor_min}: {len(trans)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(E), onde E = número de transações")
    st.dataframe(pd.DataFrame([[a.origem.id, a.destino.id, a.valor] for a in trans], columns=["Origem", "Destino", "Valor"]))
    if trans:
        idx = st.number_input("Visualizar transação de índice:", min_value=0, max_value=len(trans)-1, value=0)
        a = trans[idx]
        svg = desenhar_grafo_svg([a.origem.id, a.destino.id], [(a.origem.id, a.destino.id)], destaque=[a.origem.id, a.destino.id])
        st.markdown(svg, unsafe_allow_html=True) 