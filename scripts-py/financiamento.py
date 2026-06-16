"""
AgroCalc Web — Módulo 2: Financiamento Agrícola
Disciplina: Matemática Aplicada
Conceito: Juros Compostos + Tabela Price (Sistema Francês de Amortização)

Autor: [Seu Nome]
Projeto Integrador — 2025
"""

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def taxa_anual_para_mensal(taxa_anual: float) -> float:
    """
    Converte taxa de juros anual para taxa mensal efetiva.

    Fórmula: i_mensal = (1 + i_anual)^(1/12) - 1

    Args:
        taxa_anual (float): Taxa anual em percentual (ex: 7.5 para 7,5%)

    Returns:
        float: Taxa mensal efetiva (ex: 0.00604 para ~0,604% a.m.)
    """
    return (1 + taxa_anual / 100) ** (1 / 12) - 1


def calcular_parcela_price(principal: float, taxa_mensal: float, n: int) -> float:
    """
    Calcula o valor da parcela fixa pela Tabela Price.

    Fórmula: PMT = P * i / (1 - (1 + i)^(-n))

    Args:
        principal    (float): Valor financiado (R$)
        taxa_mensal  (float): Taxa mensal efetiva (decimal, ex: 0.006)
        n            (int)  : Número de parcelas

    Returns:
        float: Valor da parcela mensal (R$)
    """
    if taxa_mensal <= 0 or n <= 0:
        raise ValueError("Taxa e prazo devem ser maiores que zero.")

    return principal * taxa_mensal / (1 - (1 + taxa_mensal) ** (-n))


def gerar_tabela_amortizacao(principal: float, taxa_mensal: float,
                              n: int, carencia: int = 0) -> list:
    """
    Gera a tabela de amortização completa (Price), parcela a parcela.

    Durante a carência, apenas juros são cobrados (sem amortização do principal).

    Args:
        principal    (float): Valor financiado (R$)
        taxa_mensal  (float): Taxa mensal efetiva (decimal)
        n            (int)  : Número de parcelas normais
        carencia     (int)  : Meses de carência (padrão: 0)

    Returns:
        list: Lista de dicts com {mes, parcela, juros, amortizacao, saldo}
    """
    pmt   = calcular_parcela_price(principal, taxa_mensal, n)
    saldo = principal
    tabela = []

    # Período de carência: paga só juros, saldo não diminui
    for m in range(1, carencia + 1):
        juros = saldo * taxa_mensal
        tabela.append({
            "mes": f"C{m}",
            "parcela": juros,
            "juros": juros,
            "amortizacao": 0.0,
            "saldo": saldo,
        })

    # Parcelas normais com amortização do principal
    for m in range(1, n + 1):
        juros = saldo * taxa_mensal
        amort = pmt - juros
        saldo -= amort
        if saldo < 0.01:
            saldo = 0.0  # elimina resíduo por arredondamento

        tabela.append({
            "mes": m,
            "parcela": pmt,
            "juros": juros,
            "amortizacao": amort,
            "saldo": saldo,
        })

    return tabela


def resumo_financiamento(principal: float, taxa_anual: float,
                          n: int, carencia: int = 0) -> dict:
    """
    Retorna um resumo completo do financiamento.

    Args:
        principal   (float): Valor financiado (R$)
        taxa_anual  (float): Taxa anual em percentual
        n           (int)  : Número de parcelas
        carencia    (int)  : Meses de carência

    Returns:
        dict: Resumo com parcela, total pago, total de juros e tabela
    """
    i     = taxa_anual_para_mensal(taxa_anual)
    pmt   = calcular_parcela_price(principal, i, n)
    total = pmt * n
    juros = total - principal
    tab   = gerar_tabela_amortizacao(principal, i, n, carencia)

    return {
        "taxa_mensal": i,
        "parcela": pmt,
        "total_pago": total,
        "total_juros": juros,
        "cet_percentual": (juros / principal) * 100,
        "tabela": tab,
    }


# ============================================================
# GERAÇÃO DE GRÁFICO (bônus: matplotlib)
# ============================================================

def gerar_grafico(tabela: list, principal: float, salvar_em: str = "grafico_financiamento.png"):
    """
    Gera dois gráficos empilhados:
      1. Evolução do saldo devedor ao longo do tempo
      2. Composição de cada parcela (juros vs amortização)

    Args:
        tabela     (list): Tabela de amortização gerada por gerar_tabela_amortizacao()
        principal  (float): Valor original financiado
        salvar_em  (str)  : Caminho para salvar o PNG
    """
    # Filtra só as parcelas normais (ignora carência)
    parcelas = [p for p in tabela if isinstance(p["mes"], int)]
    meses    = [p["mes"] for p in parcelas]
    saldos   = [p["saldo"] for p in parcelas]
    juros_v  = [p["juros"] for p in parcelas]
    amort_v  = [p["amortizacao"] for p in parcelas]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8))
    fig.suptitle("AgroCalc — Financiamento Agrícola (Tabela Price)", fontsize=13, fontweight="bold")

    # Gráfico 1: saldo devedor
    ax1.plot(meses, saldos, color="#2d6a4f", linewidth=2.5)
    ax1.fill_between(meses, saldos, alpha=0.15, color="#2d6a4f")
    ax1.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax1.set_xlabel("Mês", fontsize=10)
    ax1.set_ylabel("Saldo Devedor (R$)", fontsize=10)
    ax1.set_title("Evolução do Saldo Devedor", fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: composição das parcelas (barras empilhadas)
    ax2.bar(meses, amort_v, label="Amortização", color="#52b788")
    ax2.bar(meses, juros_v, bottom=amort_v, label="Juros", color="#e63946", alpha=0.85)
    ax2.set_xlabel("Mês", fontsize=10)
    ax2.set_ylabel("R$", fontsize=10)
    ax2.set_title("Composição das Parcelas (Amortização + Juros)", fontsize=11)
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
    print("  AgroCalc — Financiamento Agrícola")
    print("=" * 50)

    # Dados de exemplo (financiamento rural típico)
    PRINCIPAL  = 50_000.0  # R$
    TAXA_ANUAL = 7.5       # % ao ano
    PRAZO      = 36        # meses
    CARENCIA   = 3         # meses de carência

    try:
        res = resumo_financiamento(PRINCIPAL, TAXA_ANUAL, PRAZO, CARENCIA)

        print(f"\nValor financiado:    R$ {PRINCIPAL:,.2f}")
        print(f"Taxa anual:          {TAXA_ANUAL}% a.a.")
        print(f"Taxa mensal efetiva: {res['taxa_mensal']*100:.4f}% a.m.")
        print(f"Prazo:               {PRAZO} meses (+ {CARENCIA} de carência)")
        print(f"Parcela (Price):     R$ {res['parcela']:,.2f}")
        print(f"Total pago:          R$ {res['total_pago']:,.2f}")
        print(f"Total de juros:      R$ {res['total_juros']:,.2f}")
        print(f"CET sobre principal: {res['cet_percentual']:.2f}%")

        # Exibe as 5 primeiras linhas da tabela
        print("\nPrimeiras parcelas:")
        print(f"{'Mês':<6} {'Parcela':>12} {'Juros':>12} {'Amort.':>12} {'Saldo':>14}")
        print("-" * 60)
        for p in res["tabela"][:5]:
            print(f"{str(p['mes']):<6} R${p['parcela']:>10,.2f}  R${p['juros']:>10,.2f}"
                  f"  R${p['amortizacao']:>10,.2f}  R${p['saldo']:>12,.2f}")

        # Gera gráfico PNG
        gerar_grafico(res["tabela"], PRINCIPAL, salvar_em="grafico_financiamento.png")

    except ValueError as e:
        print(f"[ERRO] {e}")
