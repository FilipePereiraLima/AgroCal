// --- Dark mode persistente ---
if (localStorage.getItem('dark') === 'true') {
  document.body.classList.add('dark');
  document.getElementById('btn-dark').textContent = '☀️ Light';
}
function alternarDark() {
  const ativo = document.body.classList.toggle('dark');
  document.getElementById('btn-dark').textContent = ativo ? '☀️ Light' : '🌙 Dark';
  localStorage.setItem('dark', ativo);
}

// --- Função principal de cálculo ---
function calcularCusto() {
  // Leitura dos valores do formulário
  const insumos      = parseFloat(document.getElementById('insumos').value)      || 0;
  const maoObra      = parseFloat(document.getElementById('mao-obra').value)     || 0;
  const fixos        = parseFloat(document.getElementById('fixos').value)        || 0;
  const area         = parseFloat(document.getElementById('area').value)         || 0;
  const precoSaca    = parseFloat(document.getElementById('preco-saca').value)   || 0;
  const produtivid   = parseFloat(document.getElementById('produtividade').value)|| 0;

  // Validação básica
  if (area <= 0) {
    alert('Informe uma área válida (maior que 0).');
    return;
  }

  // ---- Cálculos pela função afim: C(x) = (insumos + maoObra) * x + fixos ----
  const custoVariavelHa = insumos + maoObra;          // coeficiente angular (a)
  const custoTotal      = custoVariavelHa * area + fixos; // C(x) = ax + b
  const custoHa         = custoTotal / area;           // custo médio por hectare

  // Cálculos opcionais (ponto de equilíbrio e receita esperada)
  let linhasExtras = '';
  if (precoSaca > 0 && produtivid > 0) {
    const receitaTotal    = precoSaca * produtivid * area;
    const lucroEstimado   = receitaTotal - custoTotal;
    const pontEqSacas     = custoTotal / precoSaca;   // sacas necessárias p/ cobrir custo
    linhasExtras = `
      <tr><td>Receita Esperada</td><td>R$ ${fmt(receitaTotal)}</td></tr>
      <tr><td>Lucro Estimado</td><td style="color:${lucroEstimado >= 0 ? 'var(--verde-claro)' : '#e63946'}">R$ ${fmt(lucroEstimado)}</td></tr>
      <tr><td>Ponto de Equilíbrio</td><td>${fmt(pontEqSacas)} sacas</td></tr>
    `;
  }

  // Monta tabela de resultados
  document.getElementById('tabela-resultado').innerHTML = `
    <tr><td>Custo Variável (R$/ha)</td><td>R$ ${fmt(custoVariavelHa)}</td></tr>
    <tr><td>Custos Fixos</td><td>R$ ${fmt(fixos)}</td></tr>
    <tr><td>Custo Total — C(${area} ha)</td><td><strong>R$ ${fmt(custoTotal)}</strong></td></tr>
    <tr><td>Custo Médio por Hectare</td><td><strong>R$ ${fmt(custoHa)}/ha</strong></td></tr>
    ${linhasExtras}
  `;

  // Renderiza gráfico de barras em CSS
  renderizarGrafico(insumos * area, maoObra * area, fixos, custoTotal);

  // Exibe a caixa de resultado
  document.getElementById('resultado-custo').classList.add('visivel');
}

// --- Renderiza barras proporcionais aos valores ---
function renderizarGrafico(totalInsumos, totalMaoObra, totalFixos, total) {
  const container = document.getElementById('grafico-barras');
  const itens = [
    { label: 'Insumos',      valor: totalInsumos,  cor: '#2d6a4f' },
    { label: 'Mão de Obra',  valor: totalMaoObra,  cor: '#52b788' },
    { label: 'Custos Fixos', valor: totalFixos,    cor: '#a37c27' },
  ];

  container.innerHTML = itens.map(item => {
    const pct = total > 0 ? (item.valor / total * 100).toFixed(1) : 0;
    return `
      <div>
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:3px;">
          <span>${item.label}</span>
          <span>R$ ${fmt(item.valor)} (${pct}%)</span>
        </div>
        <div style="background:var(--borda); border-radius:4px; height:18px; overflow:hidden;">
          <div style="width:${pct}%; background:${item.cor}; height:100%; border-radius:4px;
                      transition: width 0.6s ease;"></div>
        </div>
      </div>
    `;
  }).join('');
}

// --- Formata número como moeda brasileira ---
function fmt(n) {
  return Number(n).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
