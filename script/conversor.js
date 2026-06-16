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

// ============================================================
// CONVERSOR DE BASES
// ============================================================
function converter() {
  const raw    = document.getElementById('valor-conv').value.trim().toUpperCase();
  const base   = parseInt(document.getElementById('base-origem').value);
  const tbody  = document.getElementById('tabela-conv');
  const visual = document.getElementById('bits-visual');

  if (!raw) {
    tbody.innerHTML = '<tr><td colspan="2" style="text-align:center;color:var(--texto-secundario);">Digite um valor acima</td></tr>';
    visual.innerHTML = '';
    return;
  }

  // Converte para decimal primeiro, depois para as outras bases
  const decimal = parseInt(raw, base);

  if (isNaN(decimal) || decimal < 0) {
    tbody.innerHTML = '<tr><td colspan="2" style="color:#e63946; text-align:center;">Valor inválido para a base selecionada</td></tr>';
    visual.innerHTML = '';
    return;
  }

  const binario = decimal.toString(2);
  const hexa    = decimal.toString(16).toUpperCase();

  tbody.innerHTML = `
    <tr><td>Decimal (base 10)</td><td><strong>${decimal}</strong></td></tr>
    <tr><td>Binário (base 2)</td><td><strong>${binario}</strong></td></tr>
    <tr><td>Hexadecimal (base 16)</td><td><strong>${hexa}</strong></td></tr>
    <tr><td>Octal (base 8)</td><td>${decimal.toString(8)}</td></tr>
  `;

  // Visualização dos bits individuais (8 bits mínimo, preenchendo com zeros)
  const bits = binario.padStart(Math.max(8, binario.length % 8 === 0 ? binario.length : binario.length + (8 - binario.length % 8)), '0');
  visual.innerHTML = `
    <p style="font-size:0.85rem; color:var(--texto-secundario); margin-bottom:0.5rem;">Representação em bits (${bits.length}-bit):</p>
    <div style="display:flex; flex-wrap:wrap; gap:6px;">
      ${bits.split('').map((b, i) => `
        <div style="
          width:36px; height:36px; border-radius:6px; display:flex; align-items:center;
          justify-content:center; font-weight:700; font-size:1rem;
          background:${b === '1' ? 'var(--verde-campo)' : 'var(--borda)'};
          color:${b === '1' ? '#fff' : 'var(--texto-secundario)'};
          border: 1px solid var(--borda);
        ">${b}</div>
      `).join('')}
    </div>
  `;
}

// ============================================================
// SIMULADOR DE PORTA LÓGICA
// ============================================================
function simularPorta() {
  const porta = document.getElementById('porta').value;
  const A     = parseInt(document.getElementById('entrada-a').value);
  const B     = parseInt(document.getElementById('entrada-b').value);

  // NOT usa apenas A — esconde campo B
  const grupoB = document.getElementById('grupo-b');
  grupoB.style.opacity = porta === 'NOT' ? '0.3' : '1';
  grupoB.style.pointerEvents = porta === 'NOT' ? 'none' : 'auto';

  // Calcula saída conforme a porta selecionada
  let saida;
  switch (porta) {
    case 'AND':  saida = A & B;       break;
    case 'OR':   saida = A | B;       break;
    case 'NOT':  saida = A === 1 ? 0 : 1; break;
    case 'NAND': saida = (A & B) === 1 ? 0 : 1; break;
    case 'NOR':  saida = (A | B) === 1 ? 0 : 1; break;
    case 'XOR':  saida = A ^ B;       break;
  }

  // Exibe resultado visual
  const corSaida = saida === 1 ? 'var(--verde-claro)' : '#e63946';
  const entradas = porta === 'NOT' ? `A = ${A}` : `A = ${A}  |  B = ${B}`;
  document.getElementById('porta-visual').innerHTML = `
    <div style="font-size:0.9rem; font-weight:400; color:var(--texto-secundario); margin-bottom:0.5rem;">${entradas}</div>
    <div style="font-size:1rem; margin-bottom:0.4rem;">${porta}</div>
    <div style="font-size:2rem; color:${corSaida};">Saída = ${saida}</div>
    <div style="font-size:0.85rem; color:${corSaida}; margin-top:0.3rem;">${saida === 1 ? '✅ VERDADEIRO' : '❌ FALSO'}</div>
  `;

  // Gera tabela verdade completa para a porta selecionada
  gerarTabelaVerdade(porta);
}

// Gera tabela verdade de todas as combinações possíveis
function gerarTabelaVerdade(porta) {
  const A_atual = parseInt(document.getElementById('entrada-a').value);
  const B_atual = parseInt(document.getElementById('entrada-b').value);

  const entradas = porta === 'NOT'
    ? [[0], [1]]
    : [[0,0],[0,1],[1,0],[1,1]];

  const cabecalho = porta === 'NOT'
    ? '<tr><th>A</th><th>NOT A</th></tr>'
    : `<tr><th>A</th><th>B</th><th>${porta}</th></tr>`;

  const linhas = entradas.map(([a, b]) => {
    let s;
    switch (porta) {
      case 'AND':  s = a & b;             break;
      case 'OR':   s = a | b;             break;
      case 'NOT':  s = a === 1 ? 0 : 1;  break;
      case 'NAND': s = (a & b) === 1 ? 0 : 1; break;
      case 'NOR':  s = (a | b) === 1 ? 0 : 1; break;
      case 'XOR':  s = a ^ b;             break;
    }
    // Destaca a linha atual
    const atual = (porta === 'NOT') ? (a === A_atual) : (a === A_atual && b === B_atual);
    const estilo = atual ? 'background:rgba(82,183,136,0.15); font-weight:600;' : '';
    const cols = porta === 'NOT'
      ? `<td>${a}</td><td style="color:${s===1?'var(--verde-claro)':'#e63946'}">${s}</td>`
      : `<td>${a}</td><td>${b}</td><td style="color:${s===1?'var(--verde-claro)':'#e63946'}">${s}</td>`;
    return `<tr style="${estilo}">${cols}</tr>`;
  }).join('');

  document.getElementById('tabela-verdade').innerHTML = `<thead>${cabecalho}</thead><tbody>${linhas}</tbody>`;
}

// Inicializa os módulos ao carregar a página
converter();
simularPorta();
