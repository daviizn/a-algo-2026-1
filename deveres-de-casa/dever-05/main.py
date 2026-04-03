"""
Dever de Casa - Cálculo de Complexidade
========================================
Análise de complexidade para:
1. Algoritmo de ordenação Merge Sort
2. Multiplicação de matrizes
3. Recorrências via Teorema Mestre
"""

import math


# =============================================================================
# 1. MERGE SORT
# =============================================================================

def merge_sort(lista: list) -> list:
    """Ordena uma lista usando o algoritmo Merge Sort.

    Complexidade:
        - Recorrência: T(n) = 2T(n/2) + n
        - Pelo Teorema Mestre: a=2, b=2, f(n)=n
          log_b(a) = log_2(2) = 1  =>  n^1 = n = f(n)  =>  Caso 2
        - Resultado: T(n) = Θ(n log n)

    Args:
        lista: Lista de elementos comparáveis a ser ordenada.

    Returns:
        Nova lista com os elementos em ordem crescente.

    Examples:
        >>> merge_sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])

    return _merge(esquerda, direita)


def _merge(esquerda: list, direita: list) -> list:
    """Combina duas sublistas ordenadas em uma única lista ordenada.

    Args:
        esquerda: Sublista ordenada da esquerda.
        direita: Sublista ordenada da direita.

    Returns:
        Lista resultante da combinação ordenada.
    """
    resultado = []
    i = j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


# =============================================================================
# 2. MULTIPLICAÇÃO DE MATRIZES
# =============================================================================

def multiplicar_matrizes(matriz_a: list[list[float]],
                         matriz_b: list[list[float]]) -> list[list[float]]:
    """Realiza a multiplicação de duas matrizes pelo método clássico.

    Complexidade:
        - Três laços aninhados de tamanho n cada
        - T(n) = Θ(n³)

    Args:
        matriz_a: Matriz de dimensão m x n.
        matriz_b: Matriz de dimensão n x p.

    Returns:
        Matriz resultado de dimensão m x p.

    Raises:
        ValueError: Se o número de colunas de A for diferente do número
            de linhas de B.

    Examples:
        >>> a = [[1, 2], [3, 4]]
        >>> b = [[5, 6], [7, 8]]
        >>> multiplicar_matrizes(a, b)
        [[19, 22], [43, 50]]
    """
    linhas_a = len(matriz_a)
    colunas_a = len(matriz_a[0])
    linhas_b = len(matriz_b)
    colunas_b = len(matriz_b[0])

    if colunas_a != linhas_b:
        raise ValueError(
            f"Dimensões incompatíveis: A tem {colunas_a} colunas "
            f"e B tem {linhas_b} linhas."
        )

    resultado = [[0.0] * colunas_b for _ in range(linhas_a)]

    for i in range(linhas_a):           # O(n)
        for j in range(colunas_b):      # O(n)
            for k in range(colunas_a):  # O(n)
                resultado[i][j] += matriz_a[i][k] * matriz_b[k][j]

    return resultado


# =============================================================================
# 3. ANÁLISE DE RECORRÊNCIAS PELO TEOREMA MESTRE
# =============================================================================

def analisar_recorrencia(a: int, b: int, descricao_f: str,
                         exp_f: float) -> dict:
    """Analisa uma recorrência T(n) = aT(n/b) + f(n) pelo Teorema Mestre.

    O Teorema Mestre compara f(n) = n^exp_f com n^(log_b(a)):
        - Caso 1: f(n) = O(n^(log_b(a) - ε))  =>  T(n) = Θ(n^log_b(a))
        - Caso 2: f(n) = Θ(n^log_b(a))         =>  T(n) = Θ(n^log_b(a) · log n)
        - Caso 3: f(n) = Ω(n^(log_b(a) + ε))  =>  T(n) = Θ(f(n))

    Args:
        a: Número de subproblemas (a >= 1).
        b: Fator de redução do tamanho (b > 1).
        descricao_f: Descrição textual de f(n), ex: "sqrt(n)", "n", "n^2".
        exp_f: Expoente de n em f(n), ex: 0.5 para sqrt(n), 1 para n.

    Returns:
        Dicionário com os campos:
            - 'log_b_a': valor de log_b(a)
            - 'caso': caso do Teorema Mestre (1, 2 ou 3)
            - 'complexidade': string com a complexidade resultante

    Examples:
        >>> analisar_recorrencia(2, 4, "sqrt(n)", 0.5)
        {'log_b_a': 0.5, 'caso': 2, 'complexidade': 'Θ(n^0.5 · log n)'}
    """
    log_b_a = math.log(a, b)
    epsilon = exp_f - log_b_a  # positivo => caso 3, zero => caso 2, neg => caso 1

    if abs(epsilon) < 1e-9:
        caso = 2
        complexidade = f"Θ(n^{log_b_a:.4g} · log n)"
    elif epsilon < 0:
        caso = 1
        complexidade = f"Θ(n^{log_b_a:.4g})"
    else:
        caso = 3
        complexidade = f"Θ({descricao_f})"

    return {
        "log_b_a": log_b_a,
        "caso": caso,
        "complexidade": complexidade,
    }


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

def demonstrar_merge_sort() -> None:
    """Demonstra o funcionamento e a complexidade do Merge Sort."""
    print("=" * 60)
    print("1. MERGE SORT")
    print("=" * 60)
    print("Recorrência : T(n) = 2T(n/2) + n")
    print("Teorema Mestre: a=2, b=2, f(n)=n")
    print(f"  log_b(a)  = log_2(2) = {math.log(2, 2):.1f}")
    print("  f(n) = n^1 = n^log_b(a)  =>  Caso 2")
    print("Complexidade: Θ(n log n)\n")

    lista_exemplo = [38, 27, 43, 3, 9, 82, 10]
    ordenada = merge_sort(lista_exemplo)
    print(f"  Entrada : {lista_exemplo}")
    print(f"  Saída   : {ordenada}\n")


def demonstrar_multiplicacao_matrizes() -> None:
    """Demonstra o funcionamento e a complexidade da multiplicação de matrizes."""
    print("=" * 60)
    print("2. MULTIPLICAÇÃO DE MATRIZES")
    print("=" * 60)
    print("Três laços aninhados de tamanho n")
    print("Complexidade: Θ(n³)\n")

    a = [[1, 2, 3],
         [4, 5, 6]]
    b = [[7,  8],
         [9,  10],
         [11, 12]]

    resultado = multiplicar_matrizes(a, b)
    print("  Matriz A (2x3):")
    for linha in a:
        print(f"    {linha}")
    print("  Matriz B (3x2):")
    for linha in b:
        print(f"    {linha}")
    print("  Resultado A×B (2x2):")
    for linha in resultado:
        print(f"    {linha}\n")


def demonstrar_recorrencias() -> None:
    """Analisa as três recorrências pelo Teorema Mestre."""
    print("=" * 60)
    print("3. RECORRÊNCIAS (Teorema Mestre)")
    print("=" * 60)

    recorrencias = [
        (2, 4, "sqrt(n)", 0.5,  "T(n) = 2T(n/4) + √n"),
        (2, 4, "n",       1.0,  "T(n) = 2T(n/4) + n"),
        (16, 4, "n^2",    2.0,  "T(n) = 16T(n/4) + n²"),
    ]

    for a, b, desc_f, exp_f, enunciado in recorrencias:
        analise = analisar_recorrencia(a, b, desc_f, exp_f)
        print(f"  Recorrência : {enunciado}")
        print(f"  Parâmetros  : a={a}, b={b}, f(n)={desc_f}")
        print(f"  log_{b}({a})    = {analise['log_b_a']:.4g}")
        print(f"  Caso        : {analise['caso']}")
        print(f"  Complexidade: {analise['complexidade']}\n")


def main() -> None:
    """Ponto de entrada principal — executa todas as demonstrações."""
    demonstrar_merge_sort()
    demonstrar_multiplicacao_matrizes()
    demonstrar_recorrencias()


if __name__ == "__main__":
    main()