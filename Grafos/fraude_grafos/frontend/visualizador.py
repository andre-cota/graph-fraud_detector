import networkx as nx
import matplotlib.pyplot as plt
import random

class VisualizadorGrafo:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.max_nodes = 50  # Limite de nós para visualização

    def criar_grafo_fraudes(self, transacoes_suspeitas, amostragem=True):
        """Cria o grafo a partir das transações suspeitas com amostragem"""
        self.grafo.clear()
        
        # Se amostragem está ativada e temos muitas transações
        if amostragem and len(transacoes_suspeitas) > self.max_nodes:
            print(f"\nAmostrando {self.max_nodes} transações para visualização...")
            transacoes_amostra = random.sample(transacoes_suspeitas, self.max_nodes)
        else:
            transacoes_amostra = transacoes_suspeitas

        # Adiciona as transações da amostra
        for transacao in transacoes_amostra:
            origem = transacao.conta_origem.id
            destino = transacao.conta_destino.id
            valor = transacao.valor
            
            self.grafo.add_node(origem)
            self.grafo.add_node(destino)
            self.grafo.add_edge(origem, destino, weight=valor)

    def exibir_grafo(self):
        try:
            plt.clf()
            plt.figure(figsize=(50, 15))
            
            # Aumenta o parâmetro k para maior distanciamento e mais iterações
            pos = nx.spring_layout(
                self.grafo, 
                k=50,          
                iterations=200  
            )
            
            # Desenha as arestas
            nx.draw_networkx_edges(
                self.grafo,
                pos,
                edge_color='red',
                width=1.0,
                alpha=0.5,
                arrows=True,
                arrowsize=15,
                arrowstyle='->',
                min_source_margin=20,    
                min_target_margin=20     
            )
            
            # Desenha os nós
            nx.draw_networkx_nodes(
                self.grafo,
                pos,
                node_color='lightblue',
                node_size=300,           
                alpha=0.9,
                linewidths=1,
                edgecolors='blue'
            )
            
            # Adiciona os rótulos
            nx.draw_networkx_labels(
                self.grafo,
                pos,
                font_size=6,
                font_weight='bold',
                bbox=dict(
                    facecolor='white',
                    edgecolor='none',
                    alpha=0.7,
                    pad=0.5
                )
            )
            
            plt.title("Grafo de Transações Suspeitas", fontsize=16, pad=20)
            plt.axis('off')
            plt.tight_layout()
            plt.show(block=True)
        
        except Exception as e:
            print(f"Erro ao exibir grafo: {str(e)}")

    def get_estatisticas(self):
        return {
            'num_contas': self.grafo.number_of_nodes(),
            'num_transacoes': self.grafo.number_of_edges(),
            'grau_medio': sum(dict(self.grafo.degree()).values()) / max(1, self.grafo.number_of_nodes()),
            'densidade': nx.density(self.grafo)
        }

    def salvar_grafo(self, caminho):
        plt.savefig(caminho, bbox_inches='tight')
        plt.close()