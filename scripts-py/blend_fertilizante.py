"""
AgroCalc Web — Módulo 4: Blend de Fertilizante NPK
Disciplina: Matemática Aplicada
Conceito: Sistema Linear 3x3 — Regra de Cramer + NumPy (np.linalg.solve)

Autor: [Seu Nome]
Projeto Integrador — 2025
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def det3(m: np.ndarray) -> float:
    """
    Calcula o determinante de uma matriz 3x3 pela Regra de Sarrus.

    Fórmula:
      det = a11(a22*a33 - a23*a32)
          - a12(a21*a33 - a23*a31)
          + a13(a21*a32 - a22*a31)

    Args:
        m (np.ndarray): Matriz 3x3

    Returns:
        float: Valor do determinante
    """
    return (
        m[0,0] * (m[1,1]*m[2,2] - m[1,2]*m[2,1]) -
        m[0,1] * (m[1,0]*m[2,2] - m[1,2]*m[2,0]) +
        m[0,2] * (m[1,0]*m[2,1] - m[1,1]*m[2,0])
    )


def resolver_cramer(M: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Resolve o sistema linear M·x = b pela Regra de Cramer.

    Para cada variável i:
      x_i = det(M_i) / det(M)
    onde M_i é a matriz M com a coluna i substituída por b.

    Args:
        M (np.ndarray): Matriz de coeficientes 3x3
        b (np.ndarray): Vetor de termos independentes (demanda nutricional)

    Returns:
        np.ndarray: Vetor solução [xA, xB, xC] em kg/ha

    Raises:
        ValueError: Se o determinante for zero (sistema sem solução única)
    """
    det_M = det3(M)

    if abs(det_M) < 1e-10:
        raise ValueError(
            "Determinante zero: fertilizantes linearmente dependentes. "
            "Escolha fertilizantes com composições distintas."
        )

    solucao = np.zeros(3)
    for i in range(3):
        # Substitui coluna i pelo vetor b
        Mi = M.copy()
        Mi[:, i] = b
        solucao[i] = det3(Mi) / det_M

    return solucao


def verificar_solucao(M: np.ndarray, x: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Verifica a solução calculando M·x e comparando com b.

    Serve como checagem numérica — a diferença deve ser próxima de zero.

    Args:
        M (np.ndarray): Matriz de coeficientes
        x (np.ndarray): Vetor solução obtido
        b (np.ndarray): Vetor de demanda original

    Returns:
        np.ndarray: Vetor de resíduos (M·x - b), ideal próximo de [0,0,0]
    """
    return M @ x - b


def calcular_blend(composicao_pct: list, demanda_kg_ha: list, area: float = 1.0) -> dict:
    """
    Função principal: monta e resolve o sistema NPK completo.

    Converte as composições de % para decimal, monta a matriz M,
    resolve por Cramer e verifica pelo np.linalg.solve do NumPy.

    Args:
        composicao_pct (list): Lista 3x3 com % de N, P, K em cada fertilizante
                               [[N_A, P_A, K_A], [N_B, P_B, K_B], [N_C, P_C, K_C]]
        demanda_kg_ha  (list): Demanda [N, P, K] em kg/ha
        area           (float): Área em hectares para calcular total

    Returns:
        dict: Quantidades, verificação, totais por área e dados para gráfico
    """
    # Converte % para fração decimal e transpõe:
    # cada LINHA da matriz M representa um nutriente, cada COLUNA um fertilizante
    M = np.array(composicao_pct, dtype=float).T / 100
    b = np.array(demanda_kg_ha, dtype=float)

    # Resolve pelo método de Cramer (implementação manual)
    x_cramer = resolver_cramer(M, b)

    # Resolve também pelo NumPy para validação cruzada
    x_numpy = np.linalg.solve(M, b)

    # Verifica resíduos (M·x - b)
    residuos = verificar_solucao(M, x_cramer, b)

    return {
        "M": M,
        "b": b,
        "det_M": det3(M),
        "x_cramer": x_cramer,          # solução pela Regra de Cramer
        "x_numpy": x_numpy,            # solução pelo NumPy (validação)
        "residuos": residuos,           # deve ser próximo de zero
        "total_fertilizante_ha": float(np.sum(x_cramer)),
        "total_por_area": x_cramer * area,
        "area": area,
    }


# ============================================================
# GERAÇÃO DE GRÁFICO (bônus: matplotlib)
# ============================================================

def gerar_grafico(resultado: dict, nomes: list = None, salvar_em: str = "grafico_blend.png"):
    """
    Gera dois gráficos:
      1. Pizza com proporção de cada fertilizante no blend
      2. Barras agrupadas comparando demanda vs nutrientes fornecidos

    Args:
        resultado (dict): Saída de calcular_blend()
        nomes     (list): Nomes dos fertilizantes (padrão: A, B, C)
        salvar_em (str) : Caminho para salvar o PNG
    """
    if nomes is None:
        nomes = ["Fertilizante A", "Fertilizante B", "Fertilizante C"]

    x      = resultado["x_cramer"]
    M      = resultado["M"]
    b      = resultado["b"]
    cores  = ["#2d6a4f", "#52b788", "#a37c27"]
    nutri  = ["N (Nitrogênio)", "P (Fósforo)", "K (Potássio)"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("AgroCalc — Blend de Fertilizante NPK", fontsize=13, fontweight="bold")

    # Gráfico 1: pizza das proporções
    # Filtra valores positivos para evitar erro na pizza
    vals_pos  = [max(v, 0) for v in x]
    total_pos = sum(vals_pos)
    if total_pos > 0:
        ax1.pie(vals_pos, labels=nomes, colors=cores, autopct="%1.1f%%",
                startangle=90, textprops={"fontsize": 10})
    ax1.set_title("Proporção de Cada Fertilizante", fontsize=11)

    # Gráfico 2: demanda vs fornecido por nutriente
    fornecido = M @ x   # nutrientes efetivamente fornecidos pelo blend
    x_pos     = np.arange(len(nutri))
    largura   = 0.35

    ax2.bar(x_pos - largura/2, b,         largura, label="Demanda",   color="#2d6a4f")
    ax2.bar(x_pos + largura/2, fornecido, largura, label="Fornecido", color="#52b788", alpha=0.85)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(nutri, fontsize=9)
    ax2.set_ylabel("kg/ha", fontsize=10)
    ax2.set_title("Demanda vs Nutrientes Fornecidos", fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(salvar_em, dpi=150)
    plt.close(fig)
    print(f"[✓] Gráfico salvo em: {salvar_em}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  AgroCalc — Blend de Fertilizante NPK")
    print("=" * 50)

    # Composição dos fertilizantes (% de N, P, K)
    # Ureia: 45% N | Superfosfato simples: 46% P | Cloreto de potássio: 60% K
    COMPOSICAO = [
        [45,  0,  0],   # Fertilizante A (Ureia)
        [ 0, 46,  0],   # Fertilizante B (Superfosfato)
        [ 0,  0, 60],   # Fertilizante C (KCl)
    ]

    # Demanda nutricional da cultura (kg/ha)
    DEMANDA = [90, 60, 80]   # N, P, K

    AREA  = 10.0  # hectares
    NOMES = ["Ureia (A)", "Superfosfato (B)", "Cloreto K (C)"]

    try:
        res = calcular_blend(COMPOSICAO, DEMANDA, AREA)

        print(f"\nMatriz de composição M (colunas = fertilizantes, linhas = nutrientes):")
        print(np.round(res["M"], 4))
        print(f"\nDeterminante de M: {res['det_M']:.6f}")
        print(f"\nDemanda (b): N={DEMANDA[0]}, P={DEMANDA[1]}, K={DEMANDA[2]} kg/ha")

        print("\nSolução — Regra de Cramer:")
        for i, (n, v) in enumerate(zip(NOMES, res["x_cramer"])):
            print(f"  {n}: {v:.2f} kg/ha → {v * AREA:.1f} kg para {AREA:.0f} ha")

        print(f"\nTotal de fertilizante: {res['total_fertilizante_ha']:.2f} kg/ha")

        print("\nVerificação (resíduos M·x - b, ideal ≈ 0):")
        print(np.round(res["residuos"], 8))

        print("\nValidação NumPy (np.linalg.solve):")
        for n, v in zip(NOMES, res["x_numpy"]):
            print(f"  {n}: {v:.2f} kg/ha")

        # Gera gráficos PNG
        gerar_grafico(res, NOMES, salvar_em="grafico_blend.png")

    except ValueError as e:
        print(f"[ERRO] {e}")
    except np.linalg.LinAlgError as e:
        print(f"[ERRO NumPy] {e}")
