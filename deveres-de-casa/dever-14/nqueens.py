"""Problema das N-Rainhas.

Posicionar N rainhas em um tabuleiro NxN de modo que nenhuma ataque
outra. Problema clássico de constraint satisfaction.

REPRESENTAÇÃO:
    Indivíduo é uma **permutação** de [0, 1, ..., N-1]:

        individuo[i] = c  ⟺  rainha da linha i está na coluna c

    Por construção da permutação, garantimos:

    - 1 rainha por linha (índice é a linha)
    - 1 rainha por coluna (permutação não repete valores)

    Logo os **únicos conflitos possíveis são diagonais**.

FITNESS:
    Número de pares de rainhas em conflito diagonal. MENOR = MELHOR.
    Zero = solução exata.

COMPLEXIDADE DA FITNESS:
    O(n²) — conta C(n, 2) pares.

Reference:
    Bell, J. & Stevens, B. (2009). "A survey of known results and
    research areas for n-queens." Discrete Mathematics, 309(1), 1-31.
"""

from __future__ import annotations

import random

from operadores import Individuo


def gerar_individuo_aleatorio(n: int) -> Individuo:
    """Gera uma permutação aleatória de [0..n-1].

    Args:
        n: Número de rainhas (e dimensão do tabuleiro).

    Returns:
        Permutação aleatória.
    """
    individuo = list(range(n))
    random.shuffle(individuo)
    return individuo


def gerar_populacao_pedagogica(
    tamanho: int,
    n: int,
    num_swaps: int | None = None,
) -> list[Individuo]:
    """Inicializa população 'controladamente ruim' para fins didáticos.

    Cada indivíduo começa como a permutação identidade ``[0, 1, ..., n-1]``
    (TODAS as rainhas na diagonal principal = pior caso, C(n,2) conflitos),
    e então aplica ``num_swaps`` trocas aleatórias.

    Garante que NENHUM indivíduo inicial seja uma solução por sorte —
    útil em demos para mostrar a evolução do AG em vez de "Geração 0:
    SOLUÇÃO!" quando a população aleatória já continha uma solução.

    Args:
        tamanho: Número de indivíduos.
        n: Tamanho do problema.
        num_swaps: Quantos swaps aplicar à identidade. Se None, usa
            ``max(2, n // 3)`` (suficiente para diversidade sem resolver
            o problema).

    Returns:
        População inicial.
    """
    if num_swaps is None:
        num_swaps = max(2, n // 3)

    populacao = []
    for _ in range(tamanho):
        ind = list(range(n))
        for _ in range(num_swaps):
            i, j = random.sample(range(n), 2)
            ind[i], ind[j] = ind[j], ind[i]
        populacao.append(ind)
    return populacao


def contar_conflitos(individuo: Individuo) -> int:
    """Conta pares de rainhas em conflito diagonal.

    Duas rainhas ``(i, individuo[i])`` e ``(j, individuo[j])`` se atacam
    diagonalmente quando:

        |individuo[i] - individuo[j]| == |i - j|

    (diferença das colunas == diferença das linhas → mesma diagonal).

    Args:
        individuo: Permutação representando posições das rainhas.

    Returns:
        Número de pares em conflito diagonal. Zero = solução.

    Complexity:
        O(n²) — testa C(n, 2) pares.

    Example:
        >>> contar_conflitos([0, 1, 2, 3])  # todas na diagonal
        6
        >>> contar_conflitos([3, 1, 7, 5, 0, 2, 4, 6])  # solucao conhecida
        0
    """
    n = len(individuo)
    conflitos = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos


def fitness(individuo: Individuo) -> int:
    """Fitness = número de conflitos. MENOR = MELHOR. Zero = solução.

    Alias semântico para :func:`contar_conflitos` — usado pelo AG.
    """
    return contar_conflitos(individuo)


def listar_pares_em_conflito(individuo: Individuo) -> list[tuple[int, int]]:
    """Retorna lista de pares ``(linha_i, linha_j)`` em conflito.

    Usado pela visualização para destacar as linhas vermelhas no tabuleiro.

    Args:
        individuo: Permutação representando posições das rainhas.

    Returns:
        Lista de pares (i, j) onde rainhas i e j se atacam diagonalmente.
    """
    n = len(individuo)
    pares = []
    for i in range(n):
        for j in range(i + 1, n):
            if abs(individuo[i] - individuo[j]) == abs(i - j):
                pares.append((i, j))
    return pares
