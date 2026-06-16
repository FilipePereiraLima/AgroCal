"""
AgroCalc Web — Módulo 3: Mapa de Produtividade por Talhão
Disciplina: Matemática Aplicada + Introdução à Computação
Conceito: Matrizes com NumPy — operações, estatísticas e visualização

Autor: [Seu Nome]
Projeto Integrador — 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# ============================================================
# FUNÇÕES DE ANÁLISE DA MATRIZ
# ============================================================

def analisar_matriz(matriz: np.ndarray) -> dict:
    """
    Realiza análise estatística completa de uma matriz de produtividade.

    Usa operações nativas do NumPy para calcular média, máximo, mínimo,
    desvio padrão e médias por linha e coluna.

    Args:
        matriz (np.ndarray): Matriz 2D com produtividade em sacas/ha

    Returns:
        dict: Dicionário com todos os indicadores calculados
    """
    if matriz.ndim != 2:
        raise ValueError("A entrada deve ser uma matriz 2D (linhas x colunas).")
    if np.any(matriz < 0):
        raise ValueError("Produtividade não pode ser negativa.")

    # Índice (linha, coluna) do melhor e pior talhão
    idx_melhor = np.unravel_index(np.argmax(matriz), matriz.shape)
    idx_pior   = np.unravel_index(np.argmin(matriz), matriz.shape)

    return {
        "media_geral":    float(np.mean(matriz)),
        "maximo":         float(np.max(matriz)),
        "minimo":         float(np.min(matriz)),
        "desvio_padrao":  float(np.std(matriz)),
        "soma_total":     float(np.sum(matriz)),
        "medias_linha":   np.mean(matriz, axis=1).tolist(),   # média por talhão (linha)
        "medias_coluna":  np.mean(matriz, axis=0).tolist(),   # média por setor (coluna)
        "idx_melhor":     idx_melhor,
        "idx_pior":       idx_pior,
        "shape":          matriz.shape,
    }


def classificar_talhoes(matriz: np.ndarray, media: float) -> np.ndarray:
    """
    Classifica cada talhão como 'Alto', 'Médio' ou 'Baixo' em relação à média.

    Critério:
      - Alto  : valor >= media * 1.10  (10% acima da média)
      - Baixo : valor <= media * 0.90  (10% abaixo da média)
      - Médio : demais

    Args:
        matriz (np.ndarray): Matriz de produtividade
        media  (float)     : Média geral da matriz

    Returns:
        np.ndarray: Matriz de strings com a classificação de cada célula
    """
    classificacao = np.empty(matriz.shape, dtype=object)
    classificacao[matriz >= media * 1.10] = "Alto"
    classificacao[matriz <= media * 0.90] = "Baixo"
    # Células que não foram classificadas ainda recebem "Médio"
    mascara_medio = (matriz > media * 0.90) & (matriz < media * 1.10)
    classificacao[mascara_medio] = "Médio"
    return classificacao


# ============================================================
# GERAÇÃO DE GRÁFICO (bônus: matplotlib)
# ============================================================

def gerar_grafico(matriz: np.ndarray, analise: dict, salvar_em: str = "grafico_talhoes.png"):
    """
    Gera um mapa de calor (heatmap) da matriz de produtividade e um
    gráfico de barras com as médias por linha de talhão.

    Args:
        matriz    (np.ndarray): Matriz de produtividade
        analise   (dict)      : Resultado de analisar_matriz()
        salvar_em (str)       : Caminho para salvar o PNG
    """
    linhas, cols = matriz.shape
    rotulos_lin  = [f"T{i+1}" for i in range(linhas)]
    rotulos_col  = [f"S{j+1}" for j in range(cols)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("AgroCalc — Mapa de Produtividade por Talhão", fontsize=13, fontweight="bold")

    # --- Gráfico 1: Heatmap da matriz ---
    # Cria colormap personalizado: vermelho → amarelo → verde
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "agro", ["#e63946", "#a37c27", "#2d6a4f"]
    )
    im = ax1.imshow(matriz, cmap=cmap, aspect="auto")
    fig.colorbar(im, ax=ax1, label="Produtividade (sc/ha)")

    # Adiciona valor de cada célula no heatmap
    for i in range(linhas):
        for j in range(cols):
            ax1.text(j, i, f"{matriz[i,j]:.0f}",
                     ha="center", va="center", fontsize=10,
                     color="white", fontweight="bold")

    ax1.set_xticks(range(cols))
    ax1.set_xticklabels(rotulos_col)
    ax1.set_yticks(range(linhas))
    ax1.set_yticklabels(rotulos_lin)
    ax1.set_title("Mapa de Calor — Produtividade (sc/ha)", fontsize=11)

    # Destaca melhor e pior talhão com borda
    mi, mj = analise["idx_melhor"]
    pi, pj = analise["idx_pior"]
    ax1.add_patch(plt.Rectangle((mj-.5, mi-.5), 1, 1, fill=False, edgecolor="white", lw=3))
    ax1.add_patch(plt.Rectangle((pj-.5, pi-.5), 1, 1, fill=False, edgecolor="red",   lw=3))

    # --- Gráfico 2: Médias por linha (talhão) ---
    medias = analise["medias_linha"]
    cores  = ["#2d6a4f" if m >= analise["media_geral"] else "#e63946" for m in medias]
    ax2.barh(rotulos_lin, medias, color=cores)
    ax2.axvline(analise["media_geral"], color="#a37c27", linestyle="--",
                linewidth=1.5, label=f"Média geral: {analise['media_geral']:.1f}")
    ax2.set_xlabel("Média de Produtividade (sc/ha)", fontsize=10)
    ax2.set_title("Média por Linha de Talhão", fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(salvar_em, dpi=150)
    plt.close(fig)
    print(f"[✓] Gráfico salvo em: {salvar_em}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  AgroCalc — Mapa de Talhões (NumPy)")
    print("=" * 50)

    # Matriz de exemplo: 3 talhões x 4 setores (sacas/ha)
    dados = np.array([
        [58, 62, 55, 70],
        [45, 68, 72, 60],
        [80, 53, 48, 65],
    ], dtype=float)

    try:
        analise = analisar_matriz(dados)
        classif = classificar_talhoes(dados, analise["media_geral"])

        print(f"\nMatriz de produtividade ({analise['shape'][0]}x{analise['shape'][1]}):")
        print(dados)

        print(f"\nMédia geral:    {analise['media_geral']:.2f} sc/ha")
        print(f"Máximo:         {analise['maximo']:.0f} sc/ha — "
              f"Talhão T{analise['idx_melhor'][0]+1}-S{analise['idx_melhor'][1]+1}")
        print(f"Mínimo:         {analise['minimo']:.0f} sc/ha — "
              f"Talhão T{analise['idx_pior'][0]+1}-S{analise['idx_pior'][1]+1}")
        print(f"Desvio padrão:  {analise['desvio_padrao']:.2f} sc/ha")
        print(f"Produção total: {analise['soma_total']:.0f} sacas (1 ha por célula)")

        print("\nMédias por linha (talhão):")
        for i, m in enumerate(analise["medias_linha"]):
            print(f"  T{i+1}: {m:.2f} sc/ha")

        print("\nClassificação por talhão:")
        print(classif)

        # Gera heatmap + gráfico de barras
        gerar_grafico(dados, analise, salvar_em="grafico_talhoes.png")

    except ValueError as e:
        print(f"[ERRO] {e}")
