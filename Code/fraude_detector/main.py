from datetime import datetime
from models.conta import Conta
from models.transacao import Transacao
from models.grafo import Grafo


def main():
    contas = [
        Conta(1, 1000.0, 'corrente'),
        Conta(2, 560.0, 'poupanca'),
        Conta(3, 600.0, 'corrente'),
    ]

    transacoes = [
        Transacao(1, 1300.0, datetime(2024, 5, 1), 'transferencia', 1, 2),
        Transacao(2, 30.0, datetime(2024, 5, 2), 'transferencia', 2, 3),
        Transacao(3, 53.0, datetime(2024, 5, 3), 'transferencia', 3, 1),
    ]

    grafo = Grafo(contas, transacoes)

    conta_exemplo = contas[2]
    vizinhos = grafo.getVizinhos(conta_exemplo)

    print(f"Vizinhos da conta {conta_exemplo.id}:")
    for conta in contas:
        vizinhos = grafo.getVizinhos(conta)
        print(f"Vizinhos da conta {conta.id}:")
        for vizinho in vizinhos:
            print(
                (
                    f"  -> Conta {vizinho.id}, saldo: {vizinho.saldo}, "
                    f"tipo: {vizinho.tipo}"
                )
            )


if __name__ == '__main__':
    main()
