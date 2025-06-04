# FraudeDetector

Ferramenta de Processamento de Dados com Grafos para Detecção de Fraudes em Redes de Transações Financeiras.

## Estrutura do Projeto

- `domain/`: Modelos de grafo, nó e aresta.
- `services/`: Serviços de importação de dados.
- `algorithms/`: Algoritmos de análise e detecção.
- `tests/`: Scripts de teste e avaliação.
- `data/`: Dados de entrada (CSVs).

## Funcionalidades e Algoritmos

### 1. Importação de Dados
- **Função:** `importar_transacoes_csv(caminho_csv)`
- **Descrição:** Lê um arquivo CSV de transações, cria os nós (clientes e comerciantes) e as arestas (transações) no grafo.
- **Campos esperados:** `step`, `customer`, `age`, `gender`, `zipcodeOri`, `merchant`, `zipMerchant`, `category`, `amount`, `fraud`

### 2. Detecção de Ciclos
- **Função:** `encontrar_ciclos(grafo, limite_tamanho=6, tamanho_min=3)`
- **Descrição:** Encontra ciclos no grafo de transações, com tamanho mínimo e máximo configuráveis. Útil para identificar movimentações circulares.
- **Função:** `encontrar_ciclos_fraude(grafo, limite_tamanho=6, tamanho_min=3)`
- **Descrição:** Encontra ciclos compostos apenas por transações marcadas como fraude.

### 3. Detecção de Anomalias
- **Função:** `nos_com_muitos_envios(grafo, limite=10)`
- **Descrição:** Identifica nós que enviam mais transações do que o limite definido.
- **Função:** `nos_com_muitos_recebimentos(grafo, limite=10)`
- **Descrição:** Identifica nós que recebem mais transações do que o limite definido.
- **Função:** `transacoes_valor_alto(grafo, valor_minimo=10000)`
- **Descrição:** Lista transações com valor acima do limite definido.
- **Função:** `nos_com_burst_transacoes(grafo, tipo='envio'|'recebimento', janela_tempo_horas=24, limite=10)`
- **Descrição:** Detecta nós que enviam ou recebem muitas transações em uma janela de tempo (ex: 10 transações em 24h).
- **Objetivo:** Identificar nós (contas ou comerciantes) que enviam ou recebem muitas transações em um curto período de tempo (ex: 10 transações em 1 hora ou 1 dia).
Por quê?
Esse comportamento pode indicar movimentação suspeita, lavagem de dinheiro ou ataques automatizados.
Como fazer:
Para cada nó, obtenha a lista de transações enviadas (ou recebidas).
Ordene as transações por data/hora.
Percorra a lista com uma janela deslizante (sliding window):
Para cada transação, conte quantas transações ocorrem dentro do intervalo de tempo desejado (ex: 1 dia).
Se o número de transações dentro desse intervalo for maior que um limite (ex: 10), marque o nó como suspeito e armazene o período.
Parâmetros configuráveis:
Tamanho da janela de tempo (ex: 1 hora, 1 dia).
Limite mínimo de transações para considerar como “burst”.
- **Função:** `transacoes_outliers(grafo, n_std=3, por_no=False, tipo='envio')`
- **Descrição:** Detecta transações com valores muito acima do padrão, usando média e desvio padrão. Pode ser feita análise global (todas as transações) ou por nó (envio ou recebimento).
- **Objetivo:** Identificar transações com valores muito acima do padrão, que podem indicar tentativas de fraude ou lavagem de dinheiro.
Como fazer:
Cálculo global:
Calcule a média e o desvio padrão dos valores de todas as transações do grafo.
Considere como outlier qualquer transação cujo valor seja maior que (média + N * desvio padrão), onde N é um parâmetro (ex: 3).
Cálculo por nó (opcional):
Para cada nó, calcule a média e o desvio padrão dos valores das transações enviadas (ou recebidas).
Considere como outlier qualquer transação daquele nó que ultrapasse o limite local.
Parâmetros configuráveis:
N (fator multiplicador do desvio padrão, ex: 2 ou 3).
Se a análise é global ou por nó.
Vantagens:
Detecta valores atípicos mesmo em contextos onde o valor absoluto não é suficiente (ex: um nó que normalmente faz transações pequenas, mas de repente faz uma muito grande).
- **Função:** `ranking_nos_ativos(grafo, tipo='envio'|'recebimento', top_n=10)`
- **Descrição:** Retorna os top N nós mais ativos em envio ou recebimento de transações, ordenados do mais para o menos ativo.
- **Objetivo:** Listar os nós (contas ou comerciantes) que mais enviam ou recebem transações, ordenando do mais ativo para o menos ativo.
Por quê?
Identifica “hubs” de movimentação, que podem ser contas de lavagem, laranjas ou pontos de concentração de fraude.
Ajuda a visualizar a estrutura da rede e priorizar investigações.
Como fazer:
Para cada nó, conte o número de transações enviadas e recebidas.
Ordene os nós pelo número de transações (envio ou recebimento).
Retorne os top N nós mais ativos.
Parâmetros configuráveis:
Tipo de ranking: envio ou recebimento.
Quantidade de nós a retornar (top N).
- **Função:** `hubs_envio(grafo, limite=10)`
- **Descrição:** Retorna nós que enviam para muitos destinos únicos (potenciais hubs de redistribuição ou lavagem).
- **Função:** `hubs_recebimento(grafo, limite=10)`
- **Descrição:** Retorna nós que recebem de muitas origens únicas (potenciais hubs de coleta ou lavagem).
- **Objetivo:** Encontrar nós que concentram muitas transações de diferentes origens (para recebimento) ou diferentes destinos (para envio).
Esses nós podem ser “laranjas”, contas de lavagem ou pontos de redistribuição de dinheiro.
Como fazer:
Para cada nó, conte:
Envio: Quantos destinos únicos ele envia dinheiro.
Recebimento: Quantas origens únicas ele recebe dinheiro.
Considere como “hub” os nós que têm um número de origens/destinos únicos acima de um limite (ex: 10).
Retorne os nós e a quantidade de origens/destinos únicos.
Parâmetros configuráveis:
Tipo de análise: envio (destinos únicos) ou recebimento (origens únicas).
Limite mínimo de origens/destinos únicos para considerar como hub.
- **Função:** `encontrar_clusters(grafo, tamanho_min=3)`
- **Descrição:** Encontra clusters (componentes fortemente conectados) no grafo, usando o algoritmo de Kosaraju. Cada cluster é um grupo de nós altamente conectados entre si.
- **Objetivo:** Identificar grupos de nós que estão mais conectados entre si do que com o restante do grafo.
Esses clusters podem indicar grupos de contas agindo em conjunto, como quadrilhas ou redes de lavagem.
Como fazer (sem bibliotecas externas):
Usar um algoritmo simples de busca por componentes fortemente conectados (SCC) para grafos dirigidos.
Cada componente fortemente conectado é um cluster: todos os nós do cluster podem alcançar uns aos outros por algum caminho.
O algoritmo clássico para isso é o de Kosaraju ou Tarjan.
Parâmetros configuráveis:
Tamanho mínimo do cluster para ser considerado relevante (ex: clusters com pelo menos 3 nós).
- **Função:** `pares_recorrentes(grafo, limite=3)`
- **Descrição:** Retorna pares de contas (origem, destino) que realizam transações recorrentes entre si, acima do limite definido. Pode indicar movimentação circular ou relações suspeitas.
- **Objetivo:** Identificar pares de contas (origem, destino) que realizam transações entre si de forma recorrente.
Esse padrão pode indicar movimentação circular, lavagem de dinheiro, ou relações suspeitas.
Como fazer:
Para cada aresta (transação), conte quantas vezes o par (origem, destino) aparece no grafo.
Considere como recorrente os pares que aparecem mais de um limite (ex: 3 vezes).
Retorne a lista de pares recorrentes e a quantidade de transações entre eles.
Parâmetros configuráveis:
Limite mínimo de transações para considerar o par como recorrente.

## Como Executar os Testes

1. Coloque o arquivo CSV de dados em `data/`.
2. Execute os scripts de teste a partir da raiz do projeto:
   ```bash
   python -m tests.test_importacao
   python -m tests.test_algoritmos
   ```

## Próximos Passos
- Aprimorar algoritmos de análise (outliers, hubs, clusters, recorrência).
- Implementar interface gráfica para visualização dos resultados.

---
Sempre que uma nova funcionalidade for implementada, ela será documentada nesta seção!
