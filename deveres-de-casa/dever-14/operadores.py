"""Operadores genéticos: seleção, crossover, mutação.

Todos os operadores trabalham com **permutações** (lista de inteiros
distintos). São genéricos — funcionam para N-Rainhas, Knight's Tour,
Dominação por Rainhas e qualquer problema cuja solução seja uma
permutação.

Funções:
    selecao_torneio: Sorteia k indivíduos, retorna o melhor.
    crossover_ox: Order Crossover (preserva validade da permutação).
    mutacao_swap: Troca dois índices.
    mutacao_inversao: Reverte um segmento (melhor para problemas tipo tour).
"""

from __future__ import annotations

import random
from collections.abc import Callable

# Type alias para legibilidade
Individuo = list[int]
FitnessFn = Callable[[Individuo], float]


def selecao_torneio(
    populacao: list[Individuo],
    fitness_fn: FitnessFn,
    k: int = 3,
) -> Individuo:
    """Seleção por torneio.

    Sorteia ``k`` indivíduos da população e retorna o de menor fitness
    (assumindo MENOR = MELHOR). Quanto maior o ``k``, mais pressão
    seletiva (favorece os bons, menos diversidade).

    Args:
        populacao: Lista de indivíduos.
        fitness_fn: Função que retorna a fitness de um indivíduo.
        k: Tamanho do torneio. Default 3.

    Returns:
        O indivíduo de menor fitness dentre os ``k`` sorteados.

    Raises:
        ValueError: Se ``k`` > tamanho da população.

    Example:
        >>> pop = [[0,1,2,3], [3,2,1,0], [1,3,0,2]]
        >>> selecao_torneio(pop, fitness_fn=sum, k=2)  # retorna o de menor soma
    """
    if k > len(populacao):
        raise ValueError(f"k={k} excede tamanho da populacao ({len(populacao)})")
    competidores = random.sample(populacao, k)
    return min(competidores, key=fitness_fn)


def crossover_ox(pai_a: Individuo, pai_b: Individuo) -> Individuo:
    """Order Crossover (OX) — gera filho preservando validade da permutação.

    Algoritmo:
        1. Sorteia dois pontos de corte ``i, j`` (com ``i < j``).
        2. Filho recebe ``pai_a[i:j]`` (segmento preservado).
        3. Resto do filho é preenchido pela ordem de ``pai_b`` (a partir
           do índice ``j``, com wrap-around), pulando valores já presentes
           no segmento herdado de ``pai_a``.

    Necessário porque crossover ingênuo (ex.: dividir e juntar) geraria
    permutações inválidas com elementos repetidos.

    Args:
        pai_a: Primeiro pai (permutação).
        pai_b: Segundo pai (mesma cardinalidade de ``pai_a``).

    Returns:
        Filho — permutação válida combinando elementos dos pais.

    Raises:
        ValueError: Se os pais tiverem tamanhos diferentes.

    Example:
        >>> random.seed(0)
        >>> crossover_ox([0,1,2,3,4,5], [3,5,0,2,4,1])  # doctest: +SKIP
        [3, 5, 0, 2, 4, 1]  # exato depende do random
    """
    if len(pai_a) != len(pai_b):
        raise ValueError(f"Pais com tamanhos diferentes: {len(pai_a)} != {len(pai_b)}")

    n = len(pai_a)
    if n <= 1:
        return list(pai_a)

    i, j = sorted(random.sample(range(n), 2))
    if i == j:
        return list(pai_a)

    filho: list[int | None] = [None] * n
    filho[i:j] = pai_a[i:j]

    # Ordem do pai_b a partir do indice j (wrap-around)
    valores_b_em_ordem = pai_b[j:] + pai_b[:j]
    a_inserir = [v for v in valores_b_em_ordem if v not in filho]

    posicoes_vazias = list(range(j, n)) + list(range(0, i))
    for pos, valor in zip(posicoes_vazias, a_inserir, strict=False):
        filho[pos] = valor

    # Type narrowing: nesse ponto todos os None foram preenchidos
    return [v for v in filho if v is not None]


def mutacao_swap(individuo: Individuo, taxa: float = 0.3) -> Individuo:
    """Mutação por troca de dois índices aleatórios.

    Com probabilidade ``taxa``, sorteia dois índices ``i, j`` e troca
    ``individuo[i]`` com ``individuo[j]``. Mantém a permutação válida.

    Taxa relativamente alta (0.3) é necessária em problemas com muitos
    mínimos locais (ex.: N-Rainhas). Mais mutação = mais exploração =
    melhor escape de mínimos.

    Args:
        individuo: Permutação a mutar.
        taxa: Probabilidade de aplicar a mutação. Em [0, 1].

    Returns:
        Cópia do indivíduo com possível mutação aplicada.

    Example:
        >>> random.seed(0)
        >>> mutacao_swap([0, 1, 2, 3], taxa=1.0)  # doctest: +SKIP
        [0, 3, 2, 1]  # exato depende do random
    """
    resultado = list(individuo)
    if random.random() < taxa:
        i, j = random.sample(range(len(resultado)), 2)
        resultado[i], resultado[j] = resultado[j], resultado[i]
    return resultado


def mutacao_inversao(individuo: Individuo, taxa: float = 0.3) -> Individuo:
    """Mutação por inversão: reverte um segmento aleatório.

    Para problemas tipo TOUR (Knight's Tour, TSP), inversão preserva muito
    mais estrutura que swap simples:

    - **Inversão de [i..j]:** apenas 2 transições mudam (em ``i-1 -> i``
      e ``j -> j+1``). As transições internas ao segmento são apenas
      invertidas, não destruídas.
    - **Swap de ``i`` e ``j``:** até 4 transições mudam (vizinhos de
      cada índice). Mais disruptivo.

    Por isso inversão converge melhor em problemas de caminho.

    Args:
        individuo: Permutação a mutar.
        taxa: Probabilidade de aplicar a mutação. Em [0, 1].

    Returns:
        Cópia do indivíduo com possível inversão aplicada.

    Reference:
        Lin, S. (1965). "Computer solutions of the traveling salesman
        problem." Bell System Technical Journal, 44, 2245-2269.
    """
    resultado = list(individuo)
    if random.random() < taxa:
        i, j = sorted(random.sample(range(len(resultado)), 2))
        resultado[i : j + 1] = resultado[i : j + 1][::-1]
    return resultado
