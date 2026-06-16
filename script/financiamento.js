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

function calcularFinanciamento() {
    const P         = parseFloat(document.getElementById('principal').value) || 0;
    const taxaAnual = parseFloat(document.getElementById('taxa').value)      || 0;
    const n         = parseInt(document.getElementById('prazo').value)       || 0;
    const carencia  = parseInt(document.getElementById('carencia').value)    || 0;

    if (P <= 0 || taxaAnual <= 0 || n <= 0) {
    alert('Preencha valor, taxa e prazo corretamente.');
    return;
    }

    // Converte taxa anual para mensal efetiva
    const i = Math.pow(1 + taxaAnual / 100, 1 / 12) - 1;

    // Fórmula Price para parcela fixa
    const PMT = P * i / (1 - Math.pow(1 + i, -n));

    const totalPago  = PMT * n;
    const totalJuros = totalPago - P;

    // Resumo
    document.getElementById('tabela-fin').innerHTML = `
    <tr><td>Valor Financiado</td><td>R$ ${fmt(P)}</td></tr>
    <tr><td>Taxa Mensal Efetiva</td><td>${(i * 100).toFixed(4)}% a.m.</td></tr>
    <tr><td>Prazo</td><td>${n} meses${carencia > 0 ? ` (+ ${carencia} de carência)` : ''}</td></tr>
    <tr><td>Parcela Mensal (Price)</td><td><strong>R$ ${fmt(PMT)}</strong></td></tr>
    <tr><td>Total Pago</td><td>R$ ${fmt(totalPago)}</td></tr>
    <tr><td>Total de Juros</td><td style="color:#e63946">R$ ${fmt(totalJuros)}</td></tr>
    <tr><td>Custo Efetivo Total</td><td>${((totalJuros / P) * 100).toFixed(2)}% sobre o principal</td></tr>
    `;

    // Gráfico principal vs juros
    const barras = [
    { label: 'Principal',    valor: P,          cor: '#2d6a4f' },
    { label: 'Juros Totais', valor: totalJuros, cor: '#e63946' },
    ];
    document.getElementById('grafico-fin').innerHTML = barras.map(b => {
    const pct = (b.valor / totalPago * 100).toFixed(1);
    return `
        <div>
        <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:3px;">
            <span>${b.label}</span><span>R$ ${fmt(b.valor)} (${pct}%)</span>
        </div>
        <div style="background:var(--borda); border-radius:4px; height:18px; overflow:hidden;">
            <div style="width:${pct}%; background:${b.cor}; height:100%; border-radius:4px; transition:width 0.6s ease;"></div>
        </div>
        </div>`;
    }).join('');

    // Tabela de amortização
    let saldo = P;
    let linhas = '';

    // Período de carência: só juros, sem amortizar
    for (let m = 1; m <= carencia; m++) {
    const juros = saldo * i;
    linhas += `<tr>
        <td>C${m}</td><td>R$ ${fmt(juros)}</td>
        <td>R$ ${fmt(juros)}</td><td>R$ 0,00</td><td>R$ ${fmt(saldo)}</td>
    </tr>`;
    }

    // Parcelas normais com amortização
    for (let m = 1; m <= n; m++) {
    const juros = saldo * i;
    const amort = PMT - juros;
    saldo -= amort;
    if (saldo < 0.01) saldo = 0;
    linhas += `<tr>
        <td>${m}</td><td>R$ ${fmt(PMT)}</td>
        <td>R$ ${fmt(juros)}</td><td>R$ ${fmt(amort)}</td><td>R$ ${fmt(saldo)}</td>
    </tr>`;
    }

    document.getElementById('tabela-amort').innerHTML = linhas;
    document.getElementById('resultado-fin').classList.add('visivel');
}

// Formata número em padrão pt-BR
function fmt(n) {
    return Number(n).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}