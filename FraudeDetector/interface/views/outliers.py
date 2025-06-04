import time
import pandas as pd
from algorithms.anomalias import transacoes_outliers
from interface.svg_utils import desenhar_grafo_svg

def exibir_outliers(grafo, st):
    tipo_analise = st.selectbox("Tipo de outlier", ["global", "por nó (envio)", "por nó (recebimento)"])
    n_std = st.number_input("Nº de desvios padrão", min_value=1, value=3)
    inicio = time.time()
    if tipo_analise == "global":
        outliers = transacoes_outliers(grafo, n_std=n_std, por_no=False)
    elif tipo_analise == "por nó (envio)":
        outliers = transacoes_outliers(grafo, n_std=n_std, por_no=True, tipo="envio")
    else:
        outliers = transacoes_outliers(grafo, n_std=n_std, por_no=True, tipo="recebimento")
    tempo_exec = time.time() - inicio
    st.write(f"Total de outliers: {len(outliers)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(E), onde E = número de transações")
    st.dataframe(pd.DataFrame([[a.origem.id, a.destino.id, a.valor] for a in outliers], columns=["Origem", "Destino", "Valor"]))
    if outliers:
        idx = st.number_input("Visualizar outlier de índice:", min_value=0, max_value=len(outliers)-1, value=0)
        a = outliers[idx]
        svg = desenhar_grafo_svg([a.origem.id, a.destino.id], [(a.origem.id, a.destino.id)], destaque=[a.origem.id, a.destino.id])
        st.markdown(svg, unsafe_allow_html=True) 