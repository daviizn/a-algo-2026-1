"""Implementação do Simulated Annealing para o problema das 12-Rainhas.

Este módulo executa o Simulated Annealing e o compara com um Algoritmo
Genético, gerando um gráfico de convergência das duas abordagens.
"""

import math
import random
import matplotlib.pyplot as plt

# Importações dos módulos fornecidos
from nqueens import fitness, gerar_individuo_aleatorio
from operadores import mutacao_swap, selecao_torneio, crossover_ox


def executar_simulated_annealing(
    n: int = 12,
    temp_inicial: float = 100.0,
    taxa_resfriamento: float = 0.95,
    iteracoes_por_temp: int = 50,
) -> tuple[list[int], list[int]]:
    """Executa o algoritmo Simulated Annealing.

    Args:
        n: Número de rainhas e tamanho do tabuleiro.
        temp_inicial: Temperatura inicial do sistema.
        taxa_resfriamento: Fator de decaimento da temperatura (0 a 1).
        iteracoes_por_temp: Quantidade de vizinhos avaliados por temperatura.

    Returns:
        Uma tupla contendo a melhor solução encontrada e o histórico de
        fitness ao longo das iterações (para plotagem).
    """
    atual = gerar_individuo_aleatorio(n)
    fit_atual = fitness(atual)
    
    melhor = atual[:]
    fit_melhor = fit_atual
    
    temperatura = temp_inicial
    historico_fitness = [fit_melhor]
    
    # Critério de parada: temperatura muito baixa ou encontrou a solução (0 conflitos)
    while temperatura > 0.01 and fit_melhor > 0:
        for _ in range(iteracoes_por_temp):
            vizinho = mutacao_swap(atual, taxa=1.0)
            fit_vizinho = fitness(vizinho)
            
            delta_e = fit_vizinho - fit_atual
            
            # Aceitação: se melhorou ou se a probabilidade térmica permitir
            if delta_e < 0 or random.random() < math.exp(-delta_e / temperatura):
                atual = vizinho[:]
                fit_atual = fit_vizinho
                
                if fit_atual < fit_melhor:
                    melhor = atual[:]
                    fit_melhor = fit_atual
                    
        historico_fitness.append(fit_melhor)
        temperatura *= taxa_resfriamento
        
    return melhor, historico_fitness


def executar_algoritmo_genetico(n: int = 12, max_geracoes: int = 200) -> list[int]:
    """Executa um Algoritmo Genético básico para fins de comparação.

    Args:
        n: Número de rainhas.
        max_geracoes: Número máximo de gerações do AG.

    Returns:
        O histórico do melhor fitness de cada geração.
    """
    tam_populacao = 50
    populacao = [gerar_individuo_aleatorio(n) for _ in range(tam_populacao)]
    
    melhor_global = min(populacao, key=fitness)
    fit_melhor_global = fitness(melhor_global)
    historico_fitness = [fit_melhor_global]
    
    for _ in range(max_geracoes):
        if fit_melhor_global == 0:
            break
            
        nova_populacao = []
        while len(nova_populacao) < tam_populacao:
            pai_a = selecao_torneio(populacao, fitness)
            pai_b = selecao_torneio(populacao, fitness)
            filho = crossover_ox(pai_a, pai_b)
            filho = mutacao_swap(filho, taxa=0.3)
            nova_populacao.append(filho)
            
        populacao = nova_populacao
        melhor_geracao = min(populacao, key=fitness)
        fit_geracao = fitness(melhor_geracao)
        
        if fit_geracao < fit_melhor_global:
            melhor_global = melhor_geracao[:]
            fit_melhor_global = fit_geracao
            
        historico_fitness.append(fit_melhor_global)
        
    return historico_fitness


def plotar_convergencia() -> None:
    """Gera e exibe o gráfico de convergência comparando SA e AG."""
    _, hist_sa = executar_simulated_annealing(n=12)
    hist_ag = executar_algoritmo_genetico(n=12)
    
    plt.figure(figsize=(10, 6))
    plt.plot(hist_sa, label='Simulated Annealing', color='blue', linewidth=2)
    plt.plot(hist_ag, label='Algoritmo Genético', color='orange', linewidth=2)
    
    plt.title("Convergência: Simulated Annealing vs Algoritmo Genético (12-Rainhas)")
    plt.xlabel("Iterações / Gerações")
    plt.ylabel("Fitness (Conflitos Diagonais - Menor é melhor)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Salva o gráfico localmente antes de mostrar
    plt.savefig("convergencia_sa_ag.png", dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    plotar_convergencia()