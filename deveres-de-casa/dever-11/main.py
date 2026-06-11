"""Módulo para detecção de ciclos em grafos utilizando Union-Find.

Este módulo implementa a estrutura de dados Disjoint Set (Conjuntos Disjuntos)
com a técnica Union-Find para verificar a existência de ciclos em um grafo
não direcionado, seguindo as diretrizes PEP 8 e PEP 257.
"""

from typing import List, Set

# ==========================================
# Constantes em SCREAMING_SNAKE_CASE
# ==========================================
# Simulando o "Grafo do Exemplo Principal" de uma aula típica.
# Arestas: (1, 2), (2, 3), (3, 4) e (4, 1). 
# A última aresta (4, 1) fechará o ciclo.
ARESTAS_EXEMPLO_AULA = [(1, 2), (2, 3), (3, 4), (4, 1)]


class UnionFind:
    """Estrutura de dados Union-Find para gerenciar conjuntos disjuntos.

    Permite agrupar elementos em conjuntos e verificar rapidamente se
    dois elementos pertencem ao mesmo conjunto.
    """

    def __init__(self, vertices: Set[int]):
        """Inicializa a estrutura considerando cada vértice como seu próprio pai.

        Args:
            vertices (Set[int]): Conjunto de identificadores dos vértices.
        """
        # Inicialmente, o representante (pai) de cada vértice é ele mesmo.
        self.pai = {v: v for v in vertices}
        # O rank ajuda a manter a árvore de conjuntos balanceada durante a união.
        self.rank = {v: 0 for v in vertices}

    def encontrar(self, vertice: int) -> int:
        """Encontra o representante (raiz) do conjunto a qual o vértice pertence.

        Utiliza a técnica de compressão de caminho (path compression) para
        otimizar as buscas futuras.

        Args:
            vertice (int): O vértice a ser buscado.

        Returns:
            int: O identificador do representante do conjunto.
        """
        if self.pai[vertice] != vertice:
            # Recursivamente encontra a raiz e achata a árvore (compressão)
            self.pai[vertice] = self.encontrar(self.pai[vertice])
        return self.pai[vertice]

    def unir(self, origem: int, destino: int) -> None:
        """Une os conjuntos de dois vértices diferentes.

        Utiliza a união por rank (union by rank) para anexar a árvore
        menor à raiz da árvore maior.

        Args:
            origem (int): Primeiro vértice.
            destino (int): Segundo vértice.
        """
        raiz_origem = self.encontrar(origem)
        raiz_destino = self.encontrar(destino)

        # Só une se estiverem em conjuntos diferentes
        if raiz_origem != raiz_destino:
            if self.rank[raiz_origem] > self.rank[raiz_destino]:
                self.pai[raiz_destino] = raiz_origem
            elif self.rank[raiz_origem] < self.rank[raiz_destino]:
                self.pai[raiz_origem] = raiz_destino
            else:
                self.pai[raiz_destino] = raiz_origem
                self.rank[raiz_origem] += 1

    def tem_ciclo(self, origem: int, destino: int) -> bool:
        """Verifica se a ligação entre origem e destino forma um ciclo.

        (Implementação do objetivo 1: Adaptação de 'temCiclo' para PEP 8).
        Objetivo 2 e Dica: Usa Union-Find para ver se têm o mesmo representante.

        Args:
            origem (int): Vértice de origem.
            destino (int): Vértice de destino.

        Returns:
            bool: True se formar um ciclo, False caso contrário.
        """
        representante_origem = self.encontrar(origem)
        representante_destino = self.encontrar(destino)

        # Se os representantes forem iguais, formam um ciclo.
        return representante_origem == representante_destino


def testar_deteccao_ciclo() -> None:
    """Executa o teste do algoritmo com o Grafo do 'Exemplo Principal'."""
    # Extraindo os vértices únicos do nosso grafo de exemplo
    vertices = set()
    for u, v in ARESTAS_EXEMPLO_AULA:
        vertices.add(u)
        vertices.add(v)
    
    # Instanciando a classe em PascalCase
    detector_union_find = UnionFind(vertices)

    print("Iniciando a análise do grafo passo a passo...\n")
    
    ciclo_detectado = False

    for origem, destino in ARESTAS_EXEMPLO_AULA:
        print(f"Analisando aresta ({origem}, {destino})...")
        
        # Objetivo 1 e 2 em ação
        if detector_union_find.tem_ciclo(origem, destino):
            print(
                f"🚨 CICLO DETECTADO! Os vértices {origem} e {destino} já "
                f"possuem o mesmo representante."
            )
            ciclo_detectado = True
            break
        
        # Se não há ciclo, unimos os conjuntos
        detector_union_find.unir(origem, destino)
        print(f"✅ Aresta ({origem}, {destino}) adicionada com sucesso. Conjuntos unidos.")

    if not ciclo_detectado:
        print("\nO grafo não possui ciclos.")


if __name__ == "__main__":
    testar_deteccao_ciclo()