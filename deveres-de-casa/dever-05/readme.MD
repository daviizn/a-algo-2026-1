# 📓 Dever de Casa — Análise de Complexidade

**Aluno:** ____________Davi Serra Bezerra____________  
**Data:** __02__/__04__/___2026___  
**Disciplina:** Análise de Algoritmos  

---

## 1. Merge Sort

### Algoritmo

```
MergeSort(A, p, r):
    se p < r:
        q = ⌊(p + r) / 2⌋
        MergeSort(A, p, q)      ← T(n/2)
        MergeSort(A, q+1, r)    ← T(n/2)
        Merge(A, p, q, r)       ← Θ(n)
```

### Recorrência

```
T(n) = 2·T(n/2) + n
```

### Aplicação do Teorema Mestre

```
T(n) = a·T(n/b) + f(n)

Identificar:
  a = 2   (número de subproblemas)
  b = 2   (fator de redução)
  f(n) = n  →  f(n) = Θ(n¹)

Calcular o expoente crítico:
  log_b(a) = log₂(2) = 1

Comparar f(n) com n^(log_b a):
  f(n) = n¹  e  n^(log_b a) = n¹
  ∴ f(n) = Θ(n^(log_b a))  →  CASO 2
```

### Resultado

```
┌─────────────────────────────────────────┐
│  T(n) = Θ(n · log n)                   │
└─────────────────────────────────────────┘
```

---

## 2. Multiplicação de Matrizes (Método Clássico)

### Algoritmo

```
MatMul(A, B, n):
    para i = 1 até n:              ← n iterações
        para j = 1 até n:          ← n iterações
            C[i][j] = 0
            para k = 1 até n:      ← n iterações
                C[i][j] += A[i][k] * B[k][j]   ← O(1)
    retornar C
```

### Contagem de Operações

```
T(n) = Σᵢ₌₁ⁿ Σⱼ₌₁ⁿ Σₖ₌₁ⁿ O(1)
     = n · n · n · O(1)
     = n³ · O(1)
```

### Resultado

```
┌─────────────────────────────────────────┐
│  T(n) = Θ(n³)                          │
└─────────────────────────────────────────┘
```

---

## 3. Recorrências — Teorema Mestre

> **Enunciado do Teorema Mestre:**  
> Dada T(n) = a·T(n/b) + f(n), com a ≥ 1 e b > 1:
> - **Caso 1:** se f(n) = O(n^(log_b a − ε)) para ε > 0  →  T(n) = Θ(n^(log_b a))
> - **Caso 2:** se f(n) = Θ(n^(log_b a))                 →  T(n) = Θ(n^(log_b a) · log n)
> - **Caso 3:** se f(n) = Ω(n^(log_b a + ε)) para ε > 0  →  T(n) = Θ(f(n))

---

### 3.1 — T(n) = 2T(n/4) + √n

```
Identificar:
  a = 2,  b = 4,  f(n) = √n = n^(1/2)

Calcular expoente crítico:
  log_b(a) = log₄(2) = log(2)/log(4) = log(2) / (2·log(2)) = 1/2

Comparar:
  f(n)          = n^(1/2)
  n^(log_b a)   = n^(1/2)
  ∴ f(n) = Θ(n^(1/2))  →  CASO 2
```

```
┌─────────────────────────────────────────┐
│  T(n) = Θ(√n · log n)                  │
└─────────────────────────────────────────┘
```

---

### 3.2 — T(n) = 2T(n/4) + n

```
Identificar:
  a = 2,  b = 4,  f(n) = n = n¹

Calcular expoente crítico:
  log_b(a) = log₄(2) = 1/2

Comparar:
  f(n)          = n¹
  n^(log_b a)   = n^(1/2)
  f(n) = n¹ = Ω(n^(1/2 + ε))  para ε = 1/2 > 0

Verificar condição de regularidade:
  a·f(n/b) ≤ c·f(n)  para c < 1
  2·f(n/4) = 2·(n/4) = n/2 ≤ (1/2)·n  ✓  (c = 1/2 < 1)

∴ CASO 3
```

```
┌─────────────────────────────────────────┐
│  T(n) = Θ(n)                           │
└─────────────────────────────────────────┘
```

---

### 3.3 — T(n) = 16T(n/4) + n²

```
Identificar:
  a = 16,  b = 4,  f(n) = n²

Calcular expoente crítico:
  log_b(a) = log₄(16) = log(16)/log(4) = 4·log(2) / (2·log(2)) = 2

Comparar:
  f(n)          = n²
  n^(log_b a)   = n²
  ∴ f(n) = Θ(n²)  →  CASO 2
```

```
┌─────────────────────────────────────────┐
│  T(n) = Θ(n² · log n)                  │
└─────────────────────────────────────────┘
```

---

## Resumo Geral

| # | Problema                      | Recorrência               | Caso TM | Complexidade        |
|---|-------------------------------|---------------------------|---------|---------------------|
| 1 | Merge Sort                    | T(n) = 2T(n/2) + n        | Caso 2  | **Θ(n log n)**      |
| 2 | Multiplicação de Matrizes     | —                         | —       | **Θ(n³)**           |
| 3a | Recorrência 1                | T(n) = 2T(n/4) + √n       | Caso 2  | **Θ(√n · log n)**   |
| 3b | Recorrência 2                | T(n) = 2T(n/4) + n        | Caso 3  | **Θ(n)**            |
| 3c | Recorrência 3                | T(n) = 16T(n/4) + n²      | Caso 2  | **Θ(n² log n)**     |

---

*Código de implementação disponível em `dever-05/main.py`*