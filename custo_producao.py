"""
AgroCalc Web — Módulo 1: Custo de Produção
Disciplina: Matemática Aplicada
Conceito: Função Afim — C(x) = ax + b

Autor: [Seu Nome]
Projeto Integrador — 2025
"""

import matplotlib.pyplot as plt
import numpy as np
import os


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def calcular_custo(insumos: float, mao_obra: float, fixos: float, area: float) -> dict:
    """
    Calcula o custo de produção usando função afim.

    Fórmula: C(x) = (insumos + mao_obra) * x + fixos
    onde x = área em hectares.

    Args:
        insumos   (float): Custo de insumos por hectare (R$/ha)
        mao_obra  (float): Custo de mão de obra por hectare (R$/ha)
        fixos     (float): Custos fixos totais (R$), independem da área
        area      (float): Área plantada em hectares

    Returns:
        dict: Dicionário com custo_total, custo_ha, coef_angular, coef_linear
    """
    if area <= 0:
        raise ValueError("A área deve ser maior que zero.")

    # Coeficiente angular (a): custo variável por hectare
    a = insumos + mao_obra

    # Coeficiente linear (b): custos fixos
    b = fixos

    # Função afim: C(x) = ax + b
    custo_total = a * area + b

    # Custo médio por hectare
    custo_ha = custo_total / area

    return {
        "coef_angular": a,
        "coef_linear": b,
        "custo_total": custo_total,
        "custo_ha": custo_ha,
    }


def calcular_ponto_equilibrio(insumos: float, mao_obra: float, fixos: float,
                               preco_saca: float, produtividade: float) -> float:
    """
    Calcula o ponto de equilíbrio em hectares — área mínima para cobrir custos.

    Equação: receita(x) = custo(x)
    preco_saca * produtividade * x = (insumos + mao_obra) * x + fixos
    Isolando x: x = fixos / (preco_saca * produtividade - (insumos + mao_obra))

    Args:
        insumos       (float): Custo de insumos (R$/ha)
        mao_obra      (float): Custo de mão de obra (R$/ha)
        fixos         (float): Custos fixos totais (R$)
        preco_saca    (float): Preço de venda por saca (R$)
        produtividade (float): Produtividade esperada (sacas/ha)

    Returns:
        float: Área de equilíbrio em hectares
    """
    receita_ha = preco_saca * produtividade
    custo_variavel_ha = insumos + mao_obra
    margem = receita_ha - custo_variavel_ha

    if margem <= 0:
        raise ValueError("Receita por hectare não cobre o custo variável. Inviável.")

    return fixos / margem


# ============================================================
# GERAÇÃO DE GRÁFICO (bônus: matplotlib)
# ============================================================

def gerar_grafico(insumos: float, mao_obra: float, fixos: float,
                  area_max: float, preco_saca: float = 0, produtividade: float = 0,
                  salvar_em: str = "grafico_custo.png"):
    """
    Gera gráfico da função custo e (opcional) da função receita,
    mostrando o ponto de equilíbrio.

    Args:
        insumos       (float): Custo de insumos (R$/ha)
        mao_obra      (float): Custo de mão de obra (R$/ha)
        fixos         (float): Custos fixos totais (R$)
        area_max      (float): Área máxima para o eixo X do gráfico
        preco_saca    (float): Preço de venda por saca — opcional
        produtividade (float): Produtividade esperada — opcional
        salvar_em     (str)  : Caminho para salvar o PNG
    """
    # Gera array de áreas de 0 até area_max
    x = np.linspace(0, area_max, 300)

    a = insumos + mao_obra
    custo = a * x + fixos  # C(x) = ax + b

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, custo, color="#2d6a4f", linewidth=2.5, label="Custo Total C(x)")

    # Se tiver dados de receita, plota e marca ponto de equilíbrio
    if preco_saca > 0 and produtividade > 0:
        receita = preco_saca * produtividade * x
        ax.plot(x, receita, color="#a37c27", linewidth=2.5, linestyle="--", label="Receita R(x)")

        # Ponto de equilíbrio
        try:
            pe = calcular_ponto_equilibrio(insumos, mao_obra, fixos, preco_saca, produtividade)
            custo_pe = a * pe + fixos
            ax.axvline(pe, color="#e63946", linestyle=":", alpha=0.7)
            ax.scatter([pe], [custo_pe], color="#e63946", zorder=5, s=80)
            ax.annotate(f"  Equilíbrio\n  {pe:.1f} ha",
                        xy=(pe, custo_pe), fontsize=9, color="#e63946")
        except ValueError:
            pass

    ax.set_xlabel("Área plantada (ha)", fontsize=11)
    ax.set_ylabel("Valor (R$)", fontsize=11)
    ax.set_title("AgroCalc — Custo de Produção (Função Afim)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(salvar_em, dpi=150)
    plt.close(fig)
    print(f"[✓] Gráfico salvo em: {salvar_em}")


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  AgroCalc — Custo de Produção")
    print("=" * 50)

    # Dados de exemplo (soja, 10 ha)
    INSUMOS    = 1200.0   # R$/ha
    MAO_OBRA   = 400.0    # R$/ha
    FIXOS      = 3000.0   # R$
    AREA       = 10.0     # ha
    PRECO_SACA = 85.0     # R$/saca
    PRODUTIV   = 60.0     # sacas/ha

    try:
        resultado = calcular_custo(INSUMOS, MAO_OBRA, FIXOS, AREA)

        print(f"\nFunção Afim: C(x) = {resultado['coef_angular']}x + {resultado['coef_linear']}")
        print(f"Área plantada:       {AREA} ha")
        print(f"Custo Total:         R$ {resultado['custo_total']:,.2f}")
        print(f"Custo por Hectare:   R$ {resultado['custo_ha']:,.2f}/ha")

        pe = calcular_ponto_equilibrio(INSUMOS, MAO_OBRA, FIXOS, PRECO_SACA, PRODUTIV)
        print(f"Ponto de Equilíbrio: {pe:.2f} ha")

        # Gera gráfico e salva PNG
        gerar_grafico(INSUMOS, MAO_OBRA, FIXOS, area_max=20,
                      preco_saca=PRECO_SACA, produtividade=PRODUTIV,
                      salvar_em="grafico_custo.png")

    except ValueError as e:
        print(f"[ERRO] {e}")
