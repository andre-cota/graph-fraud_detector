import time
import pandas as pd
from algorithms.anomalias import nos_com_burst_transacoes
from interface.svg_utils import desenhar_grafo_svg

def exibir_bursts(grafo, st):
    tipo = st.selectbox("Tipo", ["envio", "recebimento"])
    janela = st.number_input("Janela de tempo (horas)", min_value=1, value=24)
    limite = st.number_input("Limite mínimo de transações na janela", min_value=1, value=10)
    inicio = time.time()
    bursts = nos_com_burst_transacoes(grafo, tipo=tipo, janela_tempo_horas=janela, limite=limite)
    tempo_exec = time.time() - inicio
    st.write(f"Total de bursts detectados: {len(bursts)}")
    st.write(f"Tempo de execução: {tempo_exec:.4f} segundos")
    st.write("Complexidade: O(N log N) por nó (ordenação) + O(N) sliding window")
    st.dataframe(pd.DataFrame([[no.id, qtd, data_ini, data_fim] for no, qtd, data_ini, data_fim in bursts], columns=["ID", "Qtd Transações", "Início", "Fim"]))
    if bursts:
        idx = st.number_input("Visualizar burst de índice:", min_value=0, max_value=len(bursts)-1, value=0)
        no, qtd, data_ini, data_fim = bursts[idx]
        if tipo == "envio":
            transacoes = [a for a in no.transacoes_saida if data_ini <= a.data <= data_fim]
            nos_burst = [no.id] + [a.destino.id for a in transacoes]
            arestas_burst = [(no.id, a.destino.id) for a in transacoes]
        else:
            transacoes = [a for a in no.transacoes_entrada if data_ini <= a.data <= data_fim]
            nos_burst = [no.id] + [a.origem.id for a in transacoes]
            arestas_burst = [(a.origem.id, no.id) for a in transacoes]
        svg = desenhar_grafo_svg(list(set(nos_burst)), arestas_burst, destaque=[no.id])
        st.markdown(svg, unsafe_allow_html=True) 