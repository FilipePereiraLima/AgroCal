// Verifica se o usuário já tinha preferência salva no localStorage
if (localStorage.getItem('dark') === 'true') {
    document.body.classList.add('dark');
    document.getElementById('btn-dark').textContent = '☀️ Light';
}

// Alterna entre dark e light mode
function alternarDark() {
    const ativo = document.body.classList.toggle('dark');
    const btn = document.getElementById('btn-dark');
    btn.textContent = ativo ? '☀️ Light' : '🌙 Dark';
    // Salva preferência para persistir entre páginas
    localStorage.setItem('dark', ativo);
}
