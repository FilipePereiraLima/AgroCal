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

// --- Calcula determinante de matriz 3x3 pela Regra de Sarrus ---
function det3(m) {
return (
m[0][0] * (m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
m[0][1] * (m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
m[0][2] * (m[1][0]*m[2][1] - m[1][1]*m[2][0])
);
}

// --- Substitui coluna da matriz para Regra de Cramer ---
function substituirColuna(matriz, coluna, vetor) {
return matriz.map((linha, i) =>
linha.map((val, j) => j === coluna ? vetor[i] : val)
);
}

// --- Cálculo principal ---
function calcularBlend() {
// Lê a matriz de composição (em %, divide por 100)
const M = [
[+document.getElementById('a11').value/100, +document.getElementById('a12').value/100, +document.getElementById('a13').value/100],
[+document.getElementById('a21').value/100, +document.getElementById('a22').value/100, +document.getElementById('a23').value/100],
[+document.getElementById('a31').value/100, +document.getElementById('a32').value/100, +document.getElementById('a33').value/100],
];

// Lê o vetor de demanda nutricional (kg/ha)
const b    = [+document.getElementById('b1').value, +document.getElementById('b2').value, +document.getElementById('b3').value];
const area = +document.getElementById('area-blend').value || 1;

// Exibe o sistema montado em notação legível
document.getElementById('sistema-montado').innerHTML = `
<strong>Sistema Linear Montado (M · x = b):</strong><br><br>
${fmt2(M[0][0])}·xA + ${fmt2(M[0][1])}·xB + ${fmt2(M[0][2])}·xC = ${b[0]} kg N/ha<br>
${fmt2(M[1][0])}·xA + ${fmt2(M[1][1])}·xB + ${fmt2(M[1][2])}·xC = ${b[1]} kg P/ha<br>
${fmt2(M[2][0])}·xA + ${fmt2(M[2][1])}·xB + ${fmt2(M[2][2])}·xC = ${b[2]} kg K/ha
`;

// Calcula determinante principal
const detM = det3(M);

if (Math.abs(detM) < 1e-10) {
alert('Sistema sem solução única: os fertilizantes são linearmente dependentes. Revise a composição.');
return;
}

// Aplica Regra de Cramer para cada variável
const xA = det3(substituirColuna(M, 0, b)) / detM;
const xB = det3(substituirColuna(M, 1, b)) / detM;
const xC = det3(substituirColuna(M, 2, b)) / detM;

// Avisa se algum valor for negativo (solução matematicamente válida mas fisicamente impossível)
if (xA < 0 || xB < 0 || xC < 0) {
alert('Atenção: algum fertilizante resultou em quantidade negativa. Revise a composição ou a demanda.');
}

const totalKgHa = xA + xB + xC;

// Tabela de quantidades
const nomes = ['A', 'B', 'C'];
const vals  = [xA, xB, xC];
const cores = ['#2d6a4f', '#52b788', '#a37c27'];

document.getElementById('tabela-blend').innerHTML = vals.map((v, i) => `
<tr>
    <td>Fertilizante ${nomes[i]}</td>
    <td><strong>${v.toFixed(2)} kg/ha</strong></td>
    <td>${(v * area).toFixed(1)} kg</td>
</tr>
`).join('') + `
<tr style="font-weight:700;">
    <td>Total</td>
    <td>${totalKgHa.toFixed(2)} kg/ha</td>
    <td>${(totalKgHa * area).toFixed(1)} kg</td>
</tr>
`;

// Gráfico de proporção
document.getElementById('grafico-blend').innerHTML = vals.map((v, i) => {
const pct = totalKgHa > 0 ? (v / totalKgHa * 100).toFixed(1) : 0;
return `
    <div>
    <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:3px;">
        <span>Fertilizante ${nomes[i]}</span><span>${v.toFixed(2)} kg/ha (${pct}%)</span>
    </div>
    <div style="background:var(--borda); border-radius:4px; height:18px; overflow:hidden;">
        <div style="width:${pct}%; background:${cores[i]}; height:100%; border-radius:4px; transition:width 0.6s ease;"></div>
    </div>
    </div>`;
}).join('');

// Verificação: recalcula nutrientes fornecidos pelo blend
const nutrientes = ['N (Nitrogênio)', 'P (Fósforo)', 'K (Potássio)'];
document.getElementById('tabela-verif').innerHTML = b.map((dem, i) => {
const fornecido = M[i][0]*xA + M[i][1]*xB + M[i][2]*xC;
const diff      = fornecido - dem;
const cor       = Math.abs(diff) < 0.01 ? 'var(--verde-claro)' : '#e63946';
return `
    <tr>
    <td>${nutrientes[i]}</td>
    <td>${dem.toFixed(2)}</td>
    <td>${fornecido.toFixed(2)}</td>
    <td style="color:${cor}">${diff >= 0 ? '+' : ''}${diff.toFixed(4)}</td>
    </tr>`;
}).join('');

document.getElementById('resultado-blend').classList.add('visivel');
}

// Formata número com 4 casas para exibição do sistema
function fmt2(n) { return n.toFixed(4); }