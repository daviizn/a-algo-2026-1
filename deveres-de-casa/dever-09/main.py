"""
Implementação do algoritmo de Dijkstra para grafo direcionado com pesos.

Exibe a execução passo a passo (tabela de distâncias por nó visitado),
o caminho mínimo reconstruído e o custo total até o nó destino.
"""

import heapq
import math


# ── Constantes ───────────────────────────────────────────────────────────────

INFINITO = math.inf
VERTICE_ORIGEM = 0
VERTICE_DESTINO = 4


# ── Estrutura do grafo ───────────────────────────────────────────────────────

VERTICES = list(range(5))

# Lista de adjacência: {vértice: [(vizinho, peso), ...]}
GRAFO = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (4, 5)],
    3: [(4, 1)],
    4: [],
}


# ── Algoritmo ────────────────────────────────────────────────────────────────

def inicializar_dijkstra(
    vertices: list[int],
    origem: int,
) -> tuple[dict, dict]:
    """
    Inicializa as estruturas de distâncias e predecessores.

    Args:
        vertices: Lista de vértices do grafo.
        origem: Vértice de partida do algoritmo.

    Returns:
        Tupla (distancias, predecessores) com os valores iniciais.
    """
    distancias = {v: INFINITO for v in vertices}
    predecessores = {v: None for v in vertices}
    distancias[origem] = 0
    return distancias, predecessores


def dijkstra(
    grafo: dict,
    vertices: list[int],
    origem: int,
) -> tuple[dict, dict, list[dict]]:
    """
    Executa o algoritmo de Dijkstra e registra o histórico de passos.

    A cada nó extraído da fila de prioridade, um snapshot do estado
    atual das distâncias e predecessores é salvo no histórico.

    Args:
        grafo: Lista de adjacência {vértice: [(vizinho, peso)]}.
        vertices: Lista de todos os vértices do grafo.
        origem: Vértice inicial.

    Returns:
        Tupla (distancias, predecessores, historico) onde:
            - distancias é o dict de distâncias mínimas finais;
            - predecessores é o dict de predecessores finais;
            - historico é lista de dicts, cada um com as chaves
              'visitado', 'distancias' e 'predecessores'.
    """
    distancias, predecessores = inicializar_dijkstra(vertices, origem)
    visitados: set[int] = set()
    fila: list[tuple[float, int]] = [(0, origem)]
    historico: list[dict] = []

    while fila:
        dist_atual, u = heapq.heappop(fila)

        if u in visitados:
            continue

        visitados.add(u)

        historico.append({
            "visitado": u,
            "distancias": {**distancias},
            "predecessores": {**predecessores},
        })

        for v, peso in grafo.get(u, []):
            nova_dist = distancias[u] + peso
            if nova_dist < distancias[v]:
                distancias[v] = nova_dist
                predecessores[v] = u
                heapq.heappush(fila, (nova_dist, v))

    return distancias, predecessores, historico


def reconstruir_caminho(
    predecessores: dict,
    origem: int,
    destino: int,
) -> list[int]:
    """
    Reconstrói o caminho mínimo do destino até a origem via predecessores.

    Args:
        predecessores: Dicionário de predecessores gerado pelo Dijkstra.
        origem: Vértice de partida.
        destino: Vértice de chegada.

    Returns:
        Lista de vértices do caminho mínimo (origem → destino),
        ou lista vazia se não houver caminho.
    """
    caminho: list[int] = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    caminho.reverse()

    if caminho[0] != origem:
        return []

    return caminho


# ── Exibição ─────────────────────────────────────────────────────────────────

def formatar_distancia(valor: float) -> str:
    """
    Formata a distância para exibição no terminal.

    Args:
        valor: Valor numérico da distância.

    Returns:
        '∞' para infinito, inteiro como string caso contrário.
    """
    return "∞" if valor == INFINITO else str(int(valor))


def formatar_predecessor(pred) -> str:
    """
    Formata o predecessor para exibição no terminal.

    Args:
        pred: Vértice predecessor ou None.

    Returns:
        '-' para None, ou o vértice como string.
    """
    return "-" if pred is None else str(pred)


def imprimir_tabela(
    historico: list[dict],
    vertices: list[int],
) -> None:
    """
    Imprime a tabela de execução passo a passo no terminal.

    Cada linha representa o estado das distâncias e predecessores
    imediatamente após um vértice ser visitado.

    Args:
        historico: Lista de snapshots gerada pelo Dijkstra.
        vertices: Lista de vértices do grafo.
    """
    col = 10
    cabecalho = f"{'Passo (visitado)':<20}" + "".join(
        f"{'v' + str(v):^{col}}" for v in vertices
    )
    print(cabecalho)
    print("-" * len(cabecalho))

    for passo in historico:
        u = passo["visitado"]
        dists = passo["distancias"]
        preds = passo["predecessores"]

        label_d = f"visit. {u} — dist"
        label_p = f"visit. {u} — pred"

        linha_d = f"{label_d:<20}"
        linha_p = f"{label_p:<20}"

        for v in vertices:
            linha_d += f"{formatar_distancia(dists[v]):^{col}}"
            linha_p += f"{formatar_predecessor(preds[v]):^{col}}"

        print(linha_d)
        print(linha_p)
        print()


def imprimir_resultado(
    caminho: list[int],
    distancias: dict,
    destino: int,
) -> None:
    """
    Imprime o caminho mínimo e o custo total até o destino.

    Args:
        caminho: Lista de vértices do caminho mínimo.
        distancias: Dicionário de distâncias finais.
        destino: Vértice de chegada.
    """
    if not caminho:
        print(f"Não há caminho até o vértice {destino}.")
        return

    caminho_str = " → ".join(str(v) for v in caminho)
    custo = formatar_distancia(distancias[destino])
    print(f"Caminho mínimo : {caminho_str}")
    print(f"Custo total    : {custo}")


# ── Ponto de entrada ─────────────────────────────────────────────────────────

def main() -> None:
    """Executa o Dijkstra e exibe tabela, caminho e custo mínimo."""
    distancias, predecessores, historico = dijkstra(
        grafo=GRAFO,
        vertices=VERTICES,
        origem=VERTICE_ORIGEM,
    )

    imprimir_tabela(historico, VERTICES)

    caminho = reconstruir_caminho(
        predecessores=predecessores,
        origem=VERTICE_ORIGEM,
        destino=VERTICE_DESTINO,
    )

    imprimir_resultado(caminho, distancias, VERTICE_DESTINO)


if __name__ == "__main__":
    main()