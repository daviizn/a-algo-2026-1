"""
Dever de Casa 07 - O Desafio do Pronto-Socorro
==============================================
Simulação de um sistema de triagem hospitalar utilizando um Max-Heap
para priorizar o atendimento de pacientes conforme o nível de dor (1-10).

Funcionalidades:
    1. Cadastro de N pacientes com nível de dor.
    2. Processamento por prioridade via Max-Heap.
    3. Ajuste de prioridade de paciente já presente na fila
       (operações análogas a Decrease-Key e Increase-Key).
    4. Análise da complexidade das operações.

Análise de Complexidade:
    - inserir (push)                  : O(log n)
    - atender (extract-max)           : O(log n)
    - ajustar_prioridade (com índice) : O(log n)
    - localizar paciente por id       : O(1) usando dicionário auxiliar
                                        ou O(n) por busca linear no heap
    - construir heap a partir de lista: O(n)  (heapify bottom-up)

Observação:
    Em um array-heap puro, encontrar um elemento arbitrário é O(n).
    Para que o ajuste de chave seja O(log n) garantido, é necessário
    manter um mapa auxiliar (paciente_id -> índice no heap) atualizado
    a cada troca durante sift-up / sift-down. Essa estratégia é a
    adotada nesta implementação.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# =============================================================================
# CONSTANTES
# =============================================================================

NIVEL_DOR_MINIMO = 1
NIVEL_DOR_MAXIMO = 10


# =============================================================================
# MODELO DE PACIENTE
# =============================================================================

@dataclass
class Paciente:
    """Representa um paciente do pronto-socorro.

    Attributes:
        paciente_id: Identificador único do paciente (inteiro sequencial).
        nome: Nome do paciente.
        nivel_dor: Nível de dor relatado (1 a 10).
        ordem_chegada: Posição de chegada — desempata níveis de dor iguais
            preservando FIFO entre pacientes de mesma prioridade.
    """

    paciente_id: int
    nome: str
    nivel_dor: int
    ordem_chegada: int = field(default=0)

    def __post_init__(self) -> None:
        """Valida o nível de dor no momento da criação."""
        if not (NIVEL_DOR_MINIMO <= self.nivel_dor <= NIVEL_DOR_MAXIMO):
            raise ValueError(
                f"Nível de dor inválido ({self.nivel_dor}). "
                f"Deve estar entre {NIVEL_DOR_MINIMO} e {NIVEL_DOR_MAXIMO}."
            )

    def __repr__(self) -> str:
        return (f"Paciente(id={self.paciente_id}, nome={self.nome!r}, "
                f"dor={self.nivel_dor})")


# =============================================================================
# MAX-HEAP DE PACIENTES
# =============================================================================

class FilaTriagem:
    """Fila de prioridade implementada como um Max-Heap de pacientes.

    A prioridade é determinada por uma chave composta:
        (nivel_dor desc, ordem_chegada asc)
    O paciente com maior dor é atendido primeiro; em caso de empate,
    quem chegou antes tem precedência.

    Mantém um dicionário ``_indices`` que mapeia ``paciente_id`` para
    a posição atual do paciente no heap. Isso permite que a operação
    ``ajustar_prioridade`` seja realizada em O(log n).
    """

    def __init__(self) -> None:
        """Inicializa a fila vazia."""
        self._heap: list[Paciente] = []
        self._indices: dict[int, int] = {}

    # -------------------------------------------------------------------------
    # Operações de consulta
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._heap)

    def esta_vazia(self) -> bool:
        """Retorna True se não houver pacientes aguardando atendimento."""
        return len(self._heap) == 0

    def proximo(self) -> Optional[Paciente]:
        """Retorna (sem remover) o paciente com maior prioridade.

        Complexidade: O(1).

        Returns:
            O próximo paciente a ser atendido, ou None se a fila estiver vazia.
        """
        return self._heap[0] if self._heap else None

    # -------------------------------------------------------------------------
    # Operações de modificação
    # -------------------------------------------------------------------------

    def inserir(self, paciente: Paciente) -> None:
        """Insere um paciente na fila.

        Complexidade: O(log n).

        Args:
            paciente: Paciente a ser inserido.
        """
        self._heap.append(paciente)
        indice = len(self._heap) - 1
        self._indices[paciente.paciente_id] = indice
        self._sift_up(indice)

    def atender(self) -> Paciente:
        """Remove e retorna o paciente de maior prioridade (raiz do heap).

        Complexidade: O(log n).

        Returns:
            O paciente atendido.

        Raises:
            IndexError: Se a fila estiver vazia.
        """
        if not self._heap:
            raise IndexError("A fila de triagem está vazia.")

        raiz = self._heap[0]
        ultimo = self._heap.pop()
        del self._indices[raiz.paciente_id]

        if self._heap:
            self._heap[0] = ultimo
            self._indices[ultimo.paciente_id] = 0
            self._sift_down(0)

        return raiz

    def ajustar_prioridade(self, paciente_id: int, novo_nivel_dor: int) -> None:
        """Ajusta o nível de dor de um paciente já presente na fila.

        Esta operação engloba os conceitos clássicos de:
            - Increase-Key: novo_nivel_dor > nivel_dor atual  =>  sift-up
            - Decrease-Key: novo_nivel_dor < nivel_dor atual  =>  sift-down

        Complexidade:
            - Localização do paciente : O(1)  (via dicionário de índices)
            - Reequilíbrio do heap    : O(log n)
            - Total                   : O(log n)

        Sem o dicionário auxiliar, a localização seria O(n) por varredura
        linear, resultando em O(n) no total — ainda assim dominado pela
        busca, e não pelo reequilíbrio.

        Args:
            paciente_id: Identificador do paciente a ser ajustado.
            novo_nivel_dor: Novo nível de dor (1 a 10).

        Raises:
            KeyError: Se o paciente não estiver presente na fila.
            ValueError: Se ``novo_nivel_dor`` estiver fora do intervalo válido.
        """
        if not (NIVEL_DOR_MINIMO <= novo_nivel_dor <= NIVEL_DOR_MAXIMO):
            raise ValueError(
                f"Nível de dor inválido ({novo_nivel_dor}). "
                f"Deve estar entre {NIVEL_DOR_MINIMO} e {NIVEL_DOR_MAXIMO}."
            )

        if paciente_id not in self._indices:
            raise KeyError(
                f"Paciente id={paciente_id} não encontrado na fila."
            )

        indice = self._indices[paciente_id]
        nivel_anterior = self._heap[indice].nivel_dor
        self._heap[indice].nivel_dor = novo_nivel_dor

        if novo_nivel_dor > nivel_anterior:
            self._sift_up(indice)
        elif novo_nivel_dor < nivel_anterior:
            self._sift_down(indice)

    # -------------------------------------------------------------------------
    # Helpers internos do heap
    # -------------------------------------------------------------------------

    @staticmethod
    def _chave(paciente: Paciente) -> tuple[int, int]:
        """Calcula a chave de comparação (maior é mais prioritário).

        Para o Max-Heap, queremos que MAIOR dor venha primeiro e que
        MENOR ordem_chegada desempate. Como Python comparada tuplas
        elemento a elemento, retornamos ``-ordem_chegada`` para que
        a comparação por "maior" funcione corretamente.
        """
        return (paciente.nivel_dor, -paciente.ordem_chegada)

    def _mais_prioritario(self, i: int, j: int) -> int:
        """Retorna o índice do paciente com maior prioridade entre i e j."""
        if self._chave(self._heap[i]) >= self._chave(self._heap[j]):
            return i
        return j

    def _trocar(self, i: int, j: int) -> None:
        """Troca dois pacientes de posição no heap e atualiza o mapa de índices."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._indices[self._heap[i].paciente_id] = i
        self._indices[self._heap[j].paciente_id] = j

    def _sift_up(self, indice: int) -> None:
        """Sobe um nó até restaurar a propriedade do Max-Heap.

        Complexidade: O(log n).
        """
        while indice > 0:
            pai = (indice - 1) // 2
            if self._chave(self._heap[indice]) > self._chave(self._heap[pai]):
                self._trocar(indice, pai)
                indice = pai
            else:
                break

    def _sift_down(self, indice: int) -> None:
        """Desce um nó até restaurar a propriedade do Max-Heap.

        Complexidade: O(log n).
        """
        tamanho = len(self._heap)
        while True:
            esquerda = 2 * indice + 1
            direita = 2 * indice + 2
            maior = indice

            if esquerda < tamanho:
                maior = self._mais_prioritario(maior, esquerda)
            if direita < tamanho:
                maior = self._mais_prioritario(maior, direita)

            if maior == indice:
                break

            self._trocar(indice, maior)
            indice = maior


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

def demonstrar_triagem() -> None:
    """Executa um cenário de triagem completo para demonstração."""
    print("=" * 60)
    print("PRONTO-SOCORRO — SISTEMA DE TRIAGEM (Max-Heap)")
    print("=" * 60)

    pacientes_entrada = [
        ("Ana",     4),
        ("Bruno",   9),
        ("Carla",   2),
        ("Daniel",  7),
        ("Eduarda", 9),
        ("Felipe",  5),
    ]

    fila = FilaTriagem()

    print("\n[1] Chegada dos pacientes:")
    for ordem, (nome, dor) in enumerate(pacientes_entrada, start=1):
        paciente = Paciente(
            paciente_id=ordem,
            nome=nome,
            nivel_dor=dor,
            ordem_chegada=ordem,
        )
        fila.inserir(paciente)
        print(f"  -> chegou {paciente}")

    print(f"\n[2] Próximo a ser atendido: {fila.proximo()}")

    print("\n[3] Ajuste de prioridade:")
    print("    Carla (id=3) relatou piora do quadro — dor agora é 10.")
    fila.ajustar_prioridade(paciente_id=3, novo_nivel_dor=10)
    print(f"    Próximo agora: {fila.proximo()}")

    print("\n    Bruno (id=2) foi medicado e a dor caiu para 3.")
    fila.ajustar_prioridade(paciente_id=2, novo_nivel_dor=3)
    print(f"    Próximo agora: {fila.proximo()}")

    print("\n[4] Ordem de atendimento resultante:")
    posicao = 1
    while not fila.esta_vazia():
        atendido = fila.atender()
        print(f"  {posicao:>2}º -> {atendido}")
        posicao += 1


def demonstrar_complexidade() -> None:
    """Imprime um resumo da análise de complexidade das operações."""
    print("\n" + "=" * 60)
    print("ANÁLISE DE COMPLEXIDADE")
    print("=" * 60)
    linhas = [
        ("inserir(paciente)",                "O(log n)"),
        ("atender()  [extract-max]",         "O(log n)"),
        ("proximo()  [peek]",                "O(1)"),
        ("ajustar_prioridade()  c/ índice",  "O(log n)"),
        ("ajustar_prioridade()  s/ índice",  "O(n)  — domina pela busca"),
        ("construção em lote (heapify)",     "O(n)"),
    ]
    for operacao, custo in linhas:
        print(f"  {operacao:<36} -> {custo}")

    print(
        "\nImpacto do dicionário de índices:\n"
        "  Sem ele, localizar um paciente arbitrário no array do heap\n"
        "  exige varredura linear O(n). Mantendo o mapa paciente_id ->\n"
        "  índice atualizado em cada troca (sift-up/sift-down), a\n"
        "  operação de ajuste passa a ser dominada pelo reequilíbrio,\n"
        "  resultando em O(log n) — igual a Decrease/Increase-Key em\n"
        "  heaps binários clássicos."
    )


def main() -> None:
    """Ponto de entrada principal."""
    demonstrar_triagem()
    demonstrar_complexidade()


if __name__ == "__main__":
    main()
