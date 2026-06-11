"""Módulo para resolução do Problema da Soma de Subconjuntos.

Este módulo implementa uma solução baseada em backtracking para encontrar
um subconjunto de números inteiros cuja soma seja exatamente um valor alvo,
demonstrando as convenções PEP 8 e PEP 257.
"""

import random
import time
from typing import List, Optional

# ==========================================
# Constantes em SCREAMING_SNAKE_CASE
# ==========================================
TARGET_PEQUENO = 16
CONJUNTO_PEQUENO = [2, 4, 6, 10]

TARGET_MEDIO = 0
CONJUNTO_MEDIO = [-5, -2, 1, 3, 7, 12, 15, 21]

TAMANHO_GRANDE = 30
VALOR_MINIMO_RANDOM = 10000
VALOR_MAXIMO_RANDOM = 99999


class SubsetSumSolver:
    """Classe responsável por resolver o Problema da Soma de Subconjuntos.

    Utiliza a abordagem de backtracking para explorar o espaço de busca e
    encontrar o primeiro subconjunto válido que atenda à condição da soma.
    """

    def __init__(self, conjunto: List[int], alvo: int):
        """Inicializa o solucionador com um conjunto e um valor alvo.

        Args:
            conjunto (List[int]): Lista de números inteiros disponíveis.
            alvo (int): Valor exato que a soma do subconjunto deve atingir.
        """
        self.conjunto = conjunto
        self.alvo = alvo

    def encontrar_subconjunto(self) -> Optional[List[int]]:
        """Encontra um subconjunto cuja soma seja igual ao alvo definido.

        Returns:
            Optional[List[int]]: Uma lista contendo os elementos do subconjunto
            que somam o alvo, ou None se nenhuma combinação for encontrada.
        """
        # Variáveis e métodos em snake_case
        return self._backtrack(0, 0, [])

    def _backtrack(
        self, indice: int, soma_atual: int, subconjunto_atual: List[int]
    ) -> Optional[List[int]]:
        """Executa a busca recursiva (backtracking) nas ramificações.

        Método protegido designado pelo underscore inicial (_).

        Args:
            indice (int): Posição atual sendo avaliada no conjunto.
            soma_atual (int): Soma dos elementos atualmente incluídos.
            subconjunto_atual (List[int]): Elementos escolhidos até o momento.

        Returns:
            Optional[List[int]]: O subconjunto válido ou None se falhar.
        """
        if soma_atual == self.alvo and len(subconjunto_atual) > 0:
            return subconjunto_atual

        if indice == len(self.conjunto):
            return None

        # Ramificação 1: INCLUIR o elemento atual
        incluir = self._backtrack(
            indice + 1,
            soma_atual + self.conjunto[indice],
            subconjunto_atual + [self.conjunto[indice]],
        )
        if incluir is not None:
            return incluir

        # Ramificação 2: EXCLUIR o elemento atual
        excluir = self._backtrack(indice + 1, soma_atual, subconjunto_atual)
        if excluir is not None:
            return excluir

        return None


def executar_testes():
    """Executa os cenários de teste demonstrando o funcionamento da classe."""
    # Cenário 1: Tamanho Pequeno
    solver_pequeno = SubsetSumSolver(CONJUNTO_PEQUENO, TARGET_PEQUENO)
    resultado_pequeno = solver_pequeno.encontrar_subconjunto()
    print(f"Pequeno (n=4): {resultado_pequeno}")

    # Cenário 2: Tamanho Médio
    solver_medio = SubsetSumSolver(CONJUNTO_MEDIO, TARGET_MEDIO)
    resultado_medio = solver_medio.encontrar_subconjunto()
    print(f"Médio (n=8): {resultado_medio}")

    # Cenário 3: Tamanho Grande
    conjunto_grande = [
        random.randint(VALOR_MINIMO_RANDOM, VALOR_MAXIMO_RANDOM)
        for _ in range(TAMANHO_GRANDE)
    ]
    target_grande = sum(conjunto_grande[:5])
    
    solver_grande = SubsetSumSolver(conjunto_grande, target_grande)

    inicio = time.time()
    resultado_grande = solver_grande.encontrar_subconjunto()
    fim = time.time()

    print(
        f"Grande (n={TAMANHO_GRANDE}): Subconjunto encontrado "
        f"em {fim - inicio:.4f} segundos."
    )


if __name__ == "__main__":
    executar_testes()