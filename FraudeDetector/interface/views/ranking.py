import time
import pandas as pd
from algorithms.anomalias import ranking_nos_ativos
from interface.svg_utils import desenhar_grafo_svg

def exibir_ranking(grafo, st):
    tipo = st.selectbox("Tipo", ["envio", "recebimento"])
    top_n = st.number_input("Top N", min_value=1, value=10)
    inicio = time.time()
    ranking = ranking_nos_ativos(grafo, tipo=tipo, top_n=top_n)
    tempo_exec = time.time() - inicio
    st.write(f"Top {top_n} nós mais ativos em {tipo}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(V log V), onde V = número de nós (ordenação)")
    st.dataframe(pd.DataFrame([[no.id, qtd] for no, qtd in ranking], columns=["ID", "Qtd Transações"]))
    if ranking:
        idx = st.number_input("Visualizar nó de índice:", min_value=0, max_value=len(ranking)-1, value=0)
        no, _ = ranking[idx]
        if tipo == "envio":
            destinos = set(a.destino.id for a in no.transacoes_saida)
            arestas = [(no.id, dest) for dest in destinos]
            svg = desenhar_grafo_svg([no.id] + list(destinos), arestas, destaque=[no.id])
        else:
            origens = set(a.origem.id for a in no.transacoes_entrada)
            arestas = [(orig, no.id) for orig in origens]
            svg = desenhar_grafo_svg([no.id] + list(origens), arestas, destaque=[no.id])
        st.markdown(svg, unsafe_allow_html=True) 