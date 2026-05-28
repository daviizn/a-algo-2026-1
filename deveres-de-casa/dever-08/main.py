import heapq


# Grafo representado como lista de adjacência
GRAFO = {
    'A': [('B', 4), ('C', 4)],
    'B': [('A', 4), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 5), ('E', 6)],
    'D': [('B', 5), ('C', 5), ('E', 3), ('F', 4)],
    'E': [('C', 6), ('D', 3), ('F', 2)],
    'F': [('D', 4), ('E', 2)],
}

CIDADE_INICIAL = 'A'


def prim(grafo, inicio):
    """Executa o Algoritmo de Prim para encontrar a Árvore Geradora Mínima.

    Percorre o grafo a partir do nó inicial, expandindo sempre pela
    aresta de menor custo que conecta um nó visitado a um não visitado,
    utilizando uma fila de prioridade (min-heap).

    Args:
        grafo (dict): Dicionário de listas de adjacência no formato
            {cidade: [(vizinho, peso), ...]}.
        inicio (str): Identificador do nó de partida.

    Returns:
        tuple: Uma tupla (mst_arestas, custo_total) onde:
            - mst_arestas (list[tuple]): Lista de arestas da MST no
              formato (origem, destino, custo).
            - custo_total (int): Soma dos pesos das arestas da MST.
    """
    visitados = set()
    mst_arestas = []
    custo_total = 0

    # (custo, cidade_destino, cidade_origem)
    fila_prioridade = [(0, inicio, None)]

    while fila_prioridade:
        custo, cidade_atual, cidade_origem = heapq.heappop(fila_prioridade)

        if cidade_atual in visitados:
            continue

        visitados.add(cidade_atual)

        if cidade_origem is not None:
            mst_arestas.append((cidade_origem, cidade_atual, custo))
            custo_total += custo

        for vizinho, peso in grafo[cidade_atual]:
            if vizinho not in visitados:
                heapq.heappush(fila_prioridade, (peso, vizinho, cidade_atual))

    return mst_arestas, custo_total


def exibir_resultado(mst_arestas, custo_total):
    """Exibe no terminal as arestas da MST e o custo total da rede.

    Args:
        mst_arestas (list[tuple]): Lista de arestas no formato
            (origem, destino, custo).
        custo_total (int): Custo total da Árvore Geradora Mínima em km.

    Returns:
        None
    """
    separador = '=' * 50

    print(separador)
    print(' ALGORITMO DE PRIM — Rede de Fibra Óptica')
    print(separador)
    print('\n Arestas da Árvore Geradora Mínima:\n')

    for origem, destino, custo in mst_arestas:
        print(f'   {origem} --> {destino} : {custo} km')

    print(f'\n Custo total da rede: {custo_total} km')
    print(separador)


def main():
    """Ponto de entrada do programa.

    Executa o Algoritmo de Prim sobre o grafo de polos tecnológicos
    definido em GRAFO, partindo de CIDADE_INICIAL, e exibe o resultado.

    Returns:
        None
    """
    mst_arestas, custo_total = prim(GRAFO, CIDADE_INICIAL)
    exibir_resultado(mst_arestas, custo_total)


if __name__ == '__main__':
    main()