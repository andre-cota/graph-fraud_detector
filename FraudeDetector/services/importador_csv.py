import csv
from datetime import datetime, timedelta
from domain.grafo import Grafo, No, Aresta

def importar_transacoes_csv(caminho_csv: str) -> Grafo:
    grafo = Grafo()
    nos_dict = {}
    data_base = datetime(2020, 1, 1)

    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)
        for linha in leitor:
            id_origem = linha['customer']
            id_destino = linha['merchant']
            valor = float(linha['amount'])
            data = data_base + timedelta(days=int(linha['step']))
            is_fraude = linha.get('fraud', '0') in ['1', 'True', 'true']

            if id_origem not in nos_dict:
                no_origem = No(id=id_origem)
                grafo.adicionar_no(no_origem)
                nos_dict[id_origem] = no_origem
            else:
                no_origem = nos_dict[id_origem]

            if id_destino not in nos_dict:
                no_destino = No(id=id_destino)
                grafo.adicionar_no(no_destino)
                nos_dict[id_destino] = no_destino
            else:
                no_destino = nos_dict[id_destino]

            aresta = Aresta(origem=no_origem, destino=no_destino, valor=valor, data=data, is_fraude=is_fraude)
            grafo.adicionar_aresta(aresta)

    return grafo


def importar_transacoes_csv_v2(caminho_csv: str) -> Grafo:
    grafo = Grafo()
    nos_dict = {}
    data_base = datetime(2020, 1, 1)

    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)
        for linha in leitor:
            id_origem = linha['nameOrig']
            id_destino = linha['nameDest']
            valor = float(linha['amount'])
            data = data_base + timedelta(days=int(linha['step']))
            is_fraude = linha.get('isFraud', '0') in ['1', 'True', 'true']
            tipo_transacao = linha.get('type', '')
            is_flagged_fraud = linha.get('isFlaggedFraud', '0') in ['1', 'True', 'true']
            oldbalanceOrg = float(linha.get('oldbalanceOrg', 0.0))
            newbalanceOrig = float(linha.get('newbalanceOrig', 0.0))
            oldbalanceDest = float(linha.get('oldbalanceDest', 0.0))
            newbalanceDest = float(linha.get('newbalanceDest', 0.0))

            if id_origem not in nos_dict:
                no_origem = No(id=id_origem, saldo=newbalanceOrig, tipo_conta='origem')
                grafo.adicionar_no(no_origem)
                nos_dict[id_origem] = no_origem
            else:
                no_origem = nos_dict[id_origem]
                no_origem.saldo = newbalanceOrig

            if id_destino not in nos_dict:
                no_destino = No(id=id_destino, saldo=newbalanceDest, tipo_conta='destino')
                grafo.adicionar_no(no_destino)
                nos_dict[id_destino] = no_destino
            else:
                no_destino = nos_dict[id_destino]
                no_destino.saldo = newbalanceDest

            aresta = Aresta(origem=no_origem, destino=no_destino, valor=valor, data=data, is_fraude=is_fraude)
            aresta.tipo_transacao = tipo_transacao
            aresta.is_flagged_fraud = is_flagged_fraud
            aresta.oldbalanceOrg = oldbalanceOrg
            aresta.newbalanceOrig = newbalanceOrig
            aresta.oldbalanceDest = oldbalanceDest
            aresta.newbalanceDest = newbalanceDest
            grafo.adicionar_aresta(aresta)

    return grafo


def importar_transacoes_csv_v3(caminho_csv: str) -> Grafo:
    """
    Importa CSV com campos: transaction_id,amount,merchant_type,device_type,label
    Modela device_type como nó origem, merchant_type como nó destino.
    """
    grafo = Grafo()
    nos_dict = {}
    data_base = datetime(2020, 1, 1)
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile)
        for i, linha in enumerate(leitor):
            id_origem = linha['device_type']
            id_destino = linha['merchant_type']
            valor = float(linha['amount'])
            data = data_base + timedelta(days=i)
            is_fraude = linha.get('label', '0') in ['1', 'True', 'true']

            if id_origem not in nos_dict:
                no_origem = No(id=id_origem)
                grafo.adicionar_no(no_origem)
                nos_dict[id_origem] = no_origem
            else:
                no_origem = nos_dict[id_origem]

            if id_destino not in nos_dict:
                no_destino = No(id=id_destino)
                grafo.adicionar_no(no_destino)
                nos_dict[id_destino] = no_destino
            else:
                no_destino = nos_dict[id_destino]

            aresta = Aresta(origem=no_origem, destino=no_destino, valor=valor, data=data, is_fraude=is_fraude)
            grafo.adicionar_aresta(aresta)
    return grafo