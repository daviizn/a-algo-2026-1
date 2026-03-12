import time
import sys

# Aumenta o limite máximo de chamadas recursivas para evitar erro  ao calcular fatoriais grandes (como 1000!)
sys.setrecursionlimit(2000)

# Função recursiva que calcula o fatorial de um número n
def fatorial(n):

    # Caso base da recursão:
    # quando n é 0 ou 1, o fatorial é 1
    if n == 0 or n == 1:
        return 1
    
    # Caso recursivo:
    # n! = n * (n-1)!
    # a função chama a si mesma com n-1
    return n * fatorial(n - 1)


# Lista de valores que serão usados para testar o algoritmo
valores = [10, 100, 500, 1000]

# Percorre cada valor da lista para medir o tempo de execução
for n in valores:

    # Marca o instante inicial da execução
    inicio = time.time()
    
    # Calcula o fatorial do número n
    resultado = fatorial(n)
    
    # Marca o instante final da execução
    fim = time.time()

    # Calcula o tempo total de execução
    tempo_execucao = fim - inicio
    
    # Exibe o valor de n testado
    print(f"n = {n}")

    # Exibe o tempo que o algoritmo levou para executar
    print(f"Tempo de execução: {tempo_execucao:.10f} segundos\n")