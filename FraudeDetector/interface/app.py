import streamlit as st
from services.importador_csv import importar_transacoes_csv, importar_transacoes_csv_v2, importar_transacoes_csv_v3
import os

from views.ciclos import exibir_ciclos
from views.ciclos_fraude import exibir_ciclos_fraude
from views.clusters import exibir_clusters
from views.pares import exibir_pares_recorrentes
from views.bursts import exibir_bursts
from views.hubs_envio import exibir_hubs_envio
from views.hubs_recebimento import exibir_hubs_recebimento
from views.ranking import exibir_ranking
from views.outliers import exibir_outliers
from views.valor_alto import exibir_valor_alto
from views.nos_muitos import exibir_nos_muitos

st.set_page_config(page_title="FraudeDetector", layout="wide")
st.title("FraudeDetector - Análise de Fraudes em Grafos de Transações")

st.sidebar.header("Configurações")
data_dir = "data"
files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
file_csv = st.sidebar.selectbox("Selecione o arquivo de transações:", files)

formato = st.sidebar.selectbox(
    "Formato do arquivo:",
    [
        "Fraud Detection on Bank Payments",
        "Fraud Detection in Transactions Dataset",
        "Fraud Detection in Paysim Transactions Dataset",
    ]
)

@st.cache_data(show_spinner=True)
def carregar_grafo(caminho, formato):
    if formato == "Fraud Detection on Bank Payments":
        return importar_transacoes_csv(os.path.join(data_dir, caminho))
    elif formato == "Fraud Detection in Transactions Dataset":
        return importar_transacoes_csv_v3(os.path.join(data_dir, caminho))
    else:
        return importar_transacoes_csv_v2(os.path.join(data_dir, caminho))

grafo = carregar_grafo(file_csv, formato)
st.sidebar.success(f"Grafo carregado com {len(grafo.nos)} nós e {len(grafo.arestas)} transações.")

analise = st.sidebar.selectbox(
    "Escolha a análise:",
    [
        "Ciclos",
        "Ciclos (apenas fraudes)",
        "Clusters",
        "Pares recorrentes",
        "Burst temporal",
        "Hubs de envio",
        "Hubs de recebimento",
        "Ranking de nós ativos",
        "Outliers",
        "Transações de valor alto",
        "Nós com muitos envios/recebimentos"
    ]
)

st.header(f"Análise: {analise}")

if analise == "Ciclos":
    exibir_ciclos(grafo, st)
elif analise == "Ciclos (apenas fraudes)":
    exibir_ciclos_fraude(grafo, st)
elif analise == "Clusters":
    exibir_clusters(grafo, st)
elif analise == "Pares recorrentes":
    exibir_pares_recorrentes(grafo, st)
elif analise == "Burst temporal":
    exibir_bursts(grafo, st)
elif analise == "Hubs de envio":
    exibir_hubs_envio(grafo, st)
elif analise == "Hubs de recebimento":
    exibir_hubs_recebimento(grafo, st)
elif analise == "Ranking de nós ativos":
    exibir_ranking(grafo, st)
elif analise == "Outliers":
    exibir_outliers(grafo, st)
elif analise == "Transações de valor alto":
    exibir_valor_alto(grafo, st)
elif analise == "Nós com muitos envios/recebimentos":
    exibir_nos_muitos(grafo, st)
