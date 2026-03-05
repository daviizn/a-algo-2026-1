import random
import time

TAMANHOS_LISTA = [1000, 5000, 10000, 20000, 50000]
SEED_ALEATORIA = 42

def insertion_sort(lista):
    for i in range(1, len(lista)):
        valor_atual = lista[i]
        posicao = i - 1

        while posicao >= 0 and lista[posicao] > valor_atual:
            lista[posicao + 1] = lista[posicao]
            posicao -= 1

        lista[posicao + 1] = valor_atual

    return lista

def medir_tempo(funcao, dados):
    inicio = time.perf_counter()
    funcao(dados)
    fim = time.perf_counter()

    return fim - inicio

def gerar_lista(tamanho):
    return [random.randint(0, 1_000_000) for _ in range(tamanho)]

def executar_teste():
    random.seed(SEED_ALEATORIA)

    print("\nComparação de desempenho entre algoritmos de ordenação\n")
    print(f"{'Tamanho':>10} | {'Insertion':>12} | {'Timsort':>12} | {'Razão':>8}")
    print("-" * 55)

    for tamanho in TAMANHOS_LISTA:

        lista_base = gerar_lista(tamanho)

        dados1 = lista_base.copy()
        dados2 = lista_base.copy()

        tempo_insertion = medir_tempo(insertion_sort, dados1)
        tempo_timsort = medir_tempo(sorted, dados2)

        razao = tempo_insertion / tempo_timsort if tempo_timsort > 0 else 0

        print(
            f"{tamanho:>10} | "
            f"{tempo_insertion:>10.6f}s | "
            f"{tempo_timsort:>10.6f}s | "
            f"{razao:>6.1f}x"
        )

    print("-" * 55)
    print("Benchmark finalizado.\n")

if __name__ == "__main__":
    executar_teste()