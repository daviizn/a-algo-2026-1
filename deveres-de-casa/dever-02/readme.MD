# Dever 02

## Algoritmo
O algoritmo calcula o fatorial de um número utilizando recursão.

A função segue a definição matemática:

n! = n × (n − 1)!

com o caso base:

0! = 1

## Resultados experimentais

Foram realizados testes medindo o tempo de execução para diferentes valores de entrada n:

| n    | Tempo de execução (segundos) |
|-----|-------------------------------|
| 10  | 0.0000030994 |
| 100 | 0.0000133514 |
| 500 | 0.0001003742 |
| 1000| 0.0002758503 |

Observa-se que o tempo de execução aumenta conforme o valor de n cresce.

## Análise de complexidade

A complexidade assintótica do algoritmo é:

O(n)

Isso ocorre porque a função recursiva é chamada n vezes até atingir o caso base.  
Cada chamada realiza apenas uma operação constante (multiplicação e chamada recursiva).

Portanto, o número total de operações cresce proporcionalmente ao tamanho da entrada n.

Os resultados experimentais confirmam esse comportamento: à medida que n aumenta, o tempo de execução também cresce de forma aproximadamente linear.