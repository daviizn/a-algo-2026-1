"""
Módulo para cálculo da função recursiva F(n) = 2F(n-1) + n².

Caso base: F(1) = 2

A fórmula fechada equivalente é:
    F(n) = 13 * 2^(n-1) - n^2 - 4n - 6

Derivação:
    - Solução homogênea de F(n) = 2F(n-1): c * 2^n
    - Solução particular para n² (tentativa An² + Bn + C):
        A = -1, B = -4, C = -6
    - Solução geral: F(n) = c * 2^n - n^2 - 4n - 6
    - Caso base F(1) = 2: c * 2 - 1 - 4 - 6 = 2 → c = 13/2
    - Simplificando: F(n) = 13 * 2^(n-1) - n^2 - 4n - 6

Complexidade recursiva: O(2^n) — evite valores muito grandes de n.
Complexidade da fórmula fechada: O(1).
"""

import math


BASE_CASE_VALUE = 2
BASE_CASE_N = 1


def calcular_f_recursivo(n):
    """
    Calcula F(n) usando recursão, definida por:

        F(n) = 2 * F(n-1) + n²
        F(1) = 2

    Args:
        n (int): Valor inteiro positivo para o qual F(n) será calculado.

    Returns:
        int: O valor de F(n).

    Raises:
        ValueError: Se n for menor que 1.

    Examples:
        >>> calcular_f_recursivo(1)
        2
        >>> calcular_f_recursivo(2)
        8
        >>> calcular_f_recursivo(3)
        25
        >>> calcular_f_recursivo(5)
        157
    """
    if n < BASE_CASE_N:
        raise ValueError(f"n deve ser maior ou igual a {BASE_CASE_N}.")

    if n == BASE_CASE_N:
        return BASE_CASE_VALUE

    return 2 * calcular_f_recursivo(n - 1) + n ** 2


def calcular_f_fechada(n):
    """
    Calcula F(n) usando a fórmula fechada derivada da recorrência:

        F(n) = 13 * 2^(n-1) - n^2 - 4n - 6

    Obtida resolvendo F(n) = 2F(n-1) + n² com F(1) = 2.
    Utiliza math.pow para o cálculo da potência.

    Complexidade: O(1).

    Args:
        n (int): Valor inteiro positivo para o qual F(n) será calculado.

    Returns:
        int: O valor de F(n).

    Raises:
        ValueError: Se n for menor que 1.

    Examples:
        >>> calcular_f_fechada(1)
        2
        >>> calcular_f_fechada(2)
        8
        >>> calcular_f_fechada(3)
        25
        >>> calcular_f_fechada(5)
        157
    """
    if n < BASE_CASE_N:
        raise ValueError(f"n deve ser maior ou igual a {BASE_CASE_N}.")

    resultado = 13 * math.pow(2, n - 1) - n ** 2 - 4 * n - 6
    return int(resultado)


def solicitar_n():
    """
    Solicita ao usuário um valor inteiro positivo para n.

    Continua pedindo entrada até receber um valor válido (inteiro >= 1).

    Returns:
        int: O valor de n fornecido pelo usuário.
    """
    while True:
        entrada = input("\nDigite o valor de n (inteiro positivo): ")
        try:
            n = int(entrada)
            if n < BASE_CASE_N:
                print(f"Erro: n deve ser maior ou igual a {BASE_CASE_N}. Tente novamente.")
            else:
                return n
        except ValueError:
            print("Erro: entrada inválida. Por favor, digite um número inteiro.")


def main():
    """
    Função principal que solicita n ao usuário e exibe F(n) pelos dois métodos.

    Calcula F(n) de forma recursiva e pela fórmula fechada, comparando
    os resultados para verificação.

    """
    print("=== Cálculo da Função Recursiva F(n) = 2F(n-1) + n² ===")

    n = solicitar_n()

    resultado_recursivo = calcular_f_recursivo(n)
    resultado_fechada = calcular_f_fechada(n)

    print(f"\nF({n}) pela recursão: {resultado_recursivo}")
    print(f"F({n}) pela fórmula fechada: {resultado_fechada}")

if __name__ == "__main__":
    main()