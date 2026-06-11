"""Módulo para classificação de perfil de investidor utilizando KNN.

Este módulo implementa o algoritmo K-Nearest Neighbors (K-Vizinhos Mais Próximos)
para classificar um novo cliente com base na Distância Euclidiana de suas
características em relação a um banco de dados de treino existente.
"""

import math
from typing import List, Dict, Any
from collections import Counter

# ==========================================
# Constantes em SCREAMING_SNAKE_CASE
# ==========================================
K_VIZINHOS = 3

# Banco de dados de treino contendo as características dos clientes
CLIENTES_TREINO = [
    {"nome": "Ana", "salario": 40, "pontuacao": 20, "perfil": "Conservador"},
    {"nome": "Bruno", "salario": 50, "pontuacao": 35, "perfil": "Conservador"},
    {"nome": "Carlos", "salario": 90, "pontuacao": 80, "perfil": "Agressivo"},
    {"nome": "Diana", "salario": 80, "pontuacao": 65, "perfil": "Agressivo"},
]

# Dados do novo cliente a ser classificado
NOVO_CLIENTE_ARTHUR = {"nome": "Arthur", "salario": 60, "pontuacao": 45}


class KNearestNeighborsClassifier:
    """Classificador baseado no algoritmo K-Nearest Neighbors (KNN).

    Calcula a distância euclidiana entre um ponto alvo e os pontos de
    treinamento para determinar a classe majoritária entre os 'k' vizinhos
    mais próximos.
    """

    def __init__(self, dados_treino: List[Dict[str, Any]], k: int):
        """Inicializa o classificador com os dados de treino e o valor de k.

        Args:
            dados_treino (List[Dict[str, Any]]): O banco de dados de clientes.
            k (int): O número de vizinhos mais próximos a considerar.
        """
        self.dados_treino = dados_treino
        self.k = k

    def _calcular_distancia_euclidiana(
        self, x1: float, y1: float, x2: float, y2: float
    ) -> float:
        """Calcula a distância euclidiana geométrica entre dois pontos no plano 2D.

        Método protegido designado pelo underscore inicial (_).

        Args:
            x1 (float): Coordenada X do primeiro ponto (ex: salário).
            y1 (float): Coordenada Y do primeiro ponto (ex: pontuação).
            x2 (float): Coordenada X do segundo ponto.
            y2 (float): Coordenada Y do segundo ponto.

        Returns:
            float: A distância reta (euclidiana) entre os dois pontos.
        """
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def classificar(self, cliente_alvo: Dict[str, Any]) -> str:
        """Classifica o perfil de investimento do cliente alvo.

        Args:
            cliente_alvo (Dict[str, Any]): Dicionário contendo os dados do cliente.

        Returns:
            str: O perfil de investimento classificado (ex: 'Conservador').
        """
        distancias_calculadas = []

        # 1. Calcular a distância do alvo para todos os clientes de treino
        for cliente in self.dados_treino:
            distancia = self._calcular_distancia_euclidiana(
                cliente_alvo["salario"],
                cliente_alvo["pontuacao"],
                cliente["salario"],
                cliente["pontuacao"],
            )
            distancias_calculadas.append({
                "nome": cliente["nome"],
                "distancia": distancia,
                "perfil": cliente["perfil"]
            })

        # 2. Ordenar as distâncias da menor para a maior
        distancias_ordenadas = sorted(
            distancias_calculadas, key=lambda d: d["distancia"]
        )

        # 3. Selecionar os 'k' vizinhos mais próximos
        vizinhos_proximos = distancias_ordenadas[:self.k]
        
        print(f"--- Os {self.k} vizinhos mais próximos de {cliente_alvo['nome']} ---")
        for vizinho in vizinhos_proximos:
            print(
                f"- {vizinho['nome']}: Distância {vizinho['distancia']:.2f} "
                f"({vizinho['perfil']})"
            )

        # 4. Determinar a classe majoritária (votação)
        perfis_vizinhos = [vizinho["perfil"] for vizinho in vizinhos_proximos]
        contagem_votos = Counter(perfis_vizinhos)
        perfil_vencedor = contagem_votos.most_common(1)[0][0]

        return perfil_vencedor


def resolver_desafio_arthur() -> None:
    """Executa a rotina principal para resolver o problema do cliente Arthur."""
    classificador_knn = KNearestNeighborsClassifier(CLIENTES_TREINO, K_VIZINHOS)
    
    print("Iniciando a classificação do cliente Arthur...\n")
    resultado = classificador_knn.classificar(NOVO_CLIENTE_ARTHUR)
    
    print(f"\n✅ RESULTADO: O perfil de investidor do Arthur é **{resultado}**.")


if __name__ == "__main__":
    resolver_desafio_arthur()