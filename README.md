# 🌱 AgroCalc Web

> Sistema integrado de cálculos para o agronegócio — Projeto Integrador 2025

**Acesse online:** [https://[seu-usuario].github.io/agrocal](https://[seu-usuario].github.io/agrocal)

---

## 📋 Sobre o Projeto

O **AgroCalc Web** é um sistema web desenvolvido como Projeto Integrador das disciplinas de **HTML/CSS**, **Introdução à Computação** e **Matemática Aplicada**. Reúne seis módulos de cálculo voltados ao agronegócio em uma interface responsiva com dark mode.

---

## 🧩 Módulos

| Módulo | Conceito |
|---|---|
| 🌾 Calculadora de Custo | Função Afim `C(x) = ax + b` |
| 💰 Financiamento Agrícola | Juros compostos / Tabela Price |
| 🔢 Conversor de Bases | Decimal ↔ Binário ↔ Hexadecimal |
| ⚡ Porta Lógica | AND, OR, NOT, NAND, NOR, XOR |
| 🗺️ Mapa de Talhões | Matriz de produtividade (NumPy) |
| 🧪 Blend NPK | Sistema linear — Regra de Cramer |

---

## 🚀 Como executar localmente

```bash
# Clone o repositório
git clone https://github.com/[seu-usuario]/agrocal.git
cd agrocal

# Abra no navegador (sem servidor necessário)
open index.html        # macOS
start index.html       # Windows
xdg-open index.html    # Linux
```

---

## 🐍 Scripts Python

Instale as dependências e rode qualquer script:

```bash
pip install numpy matplotlib

python custo_producao.py
python financiamento.py
python matriz_talhoes.py
python blend_fertilizante.py
```

Cada script gera um gráfico `.png` na pasta atual.

---

## 📁 Estrutura de Arquivos

```
agrocal/
├── index.html              # Painel principal
├── custo.html              # Calculadora de custo
├── financiamento.html      # Simulador de financiamento
├── conversor.html          # Conversor de bases + porta lógica
├── talhoes.html            # Mapa de talhões
├── blend.html              # Blend NPK
├── style.css               # Folha de estilos (dark mode, responsivo)
├── custo_producao.py       # Função afim + matplotlib
├── financiamento.py        # Juros compostos + matplotlib
├── matriz_talhoes.py       # Matrizes NumPy + heatmap
├── blend_fertilizante.py   # Sistema linear (Cramer) + matplotlib
├── relatorio.pdf           # Relatório do projeto
└── apresentacao.pptx       # Slides de apresentação
```

---

## ✨ Funcionalidades Extras (Bônus)

- 🌙 **Dark Mode** com persistência via `localStorage`
- 📊 **Gráficos matplotlib** gerados pelos 4 scripts Python
- 🌐 **Deploy no GitHub Pages**

---

## 🏫 Informações Acadêmicas

- **Aluno:** [Seu Nome Completo]
- **Curso:** [Seu Curso] | **Período:** [Seu Período]
- **Professores:** Silvério Luiz de Sousa · Matheus Couto · Patrícia Freitas
- **Ano:** 2025
