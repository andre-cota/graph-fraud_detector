class Script:
    def __init__(self):
        self.arquivo = 'grafos2025/Grafos/fraude_grafos/app/data/paysim.csv'
        self.total_fraudes = 0
        self.total_linhas = 0
        self.contas_fraude = []

    def analisa_arquivo(self):
        try:
            with open(self.arquivo, 'r') as arquivo:
                cabeçalho = arquivo.readline().strip().split(',')
                indice_fraude = cabeçalho.index('isFraud')

                for num_linha, linha in enumerate(arquivo, start=2):
                    dados = linha.strip().split(',')
                    if dados[indice_fraude] == '1':
                        self.total_fraudes += 1
                        self.contas_fraude.append(num_linha)
                    self.total_linhas += 1

            return self.gerar_relatorio()
        except FileNotFoundError:
            return f"Arquivo {self.arquivo} não encontrado."
        except Exception as e:
            return f"Erro ao processar o arquivo: {str(e)}"

    def gerar_relatorio(self):
        relatorio = {
            "total_fraudes": self.total_fraudes,
            "total_linhas": self.total_linhas,
            "porcentagem_fraudes": (self.total_fraudes / self.total_linhas) * 100 if self.total_linhas > 0 else 0,
            "contas_fraude": self.contas_fraude
        }
        return relatorio


if __name__ == "__main__":
    script = Script()
    resultado = script.analisa_arquivo()

    print("\nRelatório de Análise de Fraudes:")
    print("-" * 30)
    print(f"Total de fraudes: {resultado['total_fraudes']}")
    print(f"Total de linhas: {resultado['total_linhas']}")
    print(f"Porcentagem de fraudes: {resultado['porcentagem_fraudes']:.2f}%")
    print("\nPrimeiras linhas com fraude:")
    print(resultado['contas_fraude'][:10])

    um_porcento_linhas = int(resultado['total_linhas'] * 0.01)
    fraudes = int(resultado['total_fraudes'] * 0.01) 

    print("\nAnálise para 1% dos dados:")
    print("-" * 30)
    print(f"Número de linhas (1%): {um_porcento_linhas}")
    print(f"Número esperado de fraudes (1%): {fraudes}")
    
    print("\nPrimeiras linhas com fraude:")
    print(resultado['contas_fraude'][:10])
