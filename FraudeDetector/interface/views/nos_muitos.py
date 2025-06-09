import time
import pandas as pd
from algorithms.anomalias import nos_com_muitos_envios, nos_com_muitos_recebimentos
from interface.svg_utils import desenhar_grafo_svg

def exibir_nos_muitos(grafo, st):
    tipo = st.selectbox("Tipo", ["envio", "recebimento"])
    limite = st.number_input("Limite mínimo", min_value=1, value=20)
    inicio = time.time()
    if tipo == "envio":
        nos = nos_com_muitos_envios(grafo, limite=limite)
    else:
        nos = nos_com_muitos_recebimentos(grafo, limite=limite)
    tempo_exec = time.time() - inicio
    st.write(f"Total de nós com mais de {limite} {tipo}s: {len(nos)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(V), onde V = número de nós")
    if tipo == "envio":
        st.dataframe(pd.DataFrame([[no.id, len(no.transacoes_saida)] for no in nos], columns=["ID", "Qtd Envios"]))
    else:
        st.dataframe(pd.DataFrame([[no.id, len(no.transacoes_entrada)] for no in nos], columns=["ID", "Qtd Recebimentos"]))
    if nos:
        idx = st.number_input("Visualizar nó de índice:", min_value=0, max_value=len(nos)-1, value=0)
        no = nos[idx]
        if tipo == "envio":
            destinos = set(a.destino.id for a in no.transacoes_saida)
            arestas = [(no.id, dest) for dest in destinos]
            svg = desenhar_grafo_svg([no.id] + list(destinos), arestas, destaque=[no.id])
        else:
            origens = set(a.origem.id for a in no.transacoes_entrada)
            arestas = [(orig, no.id) for orig in origens]
            svg = desenhar_grafo_svg([no.id] + list(origens), arestas, destaque=[no.id])
        st.markdown(svg, unsafe_allow_html=True) 