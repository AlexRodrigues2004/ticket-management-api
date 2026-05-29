requireAuth();

const user = getUser();
document.getElementById('user-name').textContent = `${user.first_name || user.username} (${user.role})`;
if (isAdmin()) document.getElementById('nav-users').style.display = 'block';

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
}

function badgeStatus(status) {
    const labels = {
        aberto: 'Aberto', em_atendimento: 'Em Atendimento',
        aguardando_cliente: 'Aguardando', resolvido: 'Resolvido', cancelado: 'Cancelado'
    };
    return `<span class="badge badge-${status}">${labels[status] || status}</span>`;
}

function badgePriority(priority) {
    const labels = { baixa: 'Baixa', media: 'Média', alta: 'Alta', critica: 'Crítica' };
    return `<span class="badge badge-${priority}">${labels[priority] || priority}</span>`;
}

async function loadDashboard() {
    const res = await api.get('/tickets/');
    if (res.status !== 200) return;

    const tickets = res.data;
    document.getElementById('total-tickets').textContent = tickets.length;
    document.getElementById('abertos').textContent = tickets.filter(t => t.status === 'aberto').length;
    document.getElementById('em-atendimento').textContent = tickets.filter(t => t.status === 'em_atendimento').length;
    document.getElementById('resolvidos').textContent = tickets.filter(t => t.status === 'resolvido').length;
    document.getElementById('criticos').textContent = tickets.filter(t => t.priority === 'critica').length;

    const tbody = document.getElementById('tickets-table');
    const latest = tickets.slice(0, 10);

    if (latest.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><p>Nenhum chamado encontrado.</p></td></tr>';
        return;
    }

    tbody.innerHTML = latest.map(t => `
        <tr>
            <td>#${t.id}</td>
            <td>${t.title}</td>
            <td>${t.customer_detail?.name || '—'}</td>
            <td>${badgeStatus(t.status)}</td>
            <td>${badgePriority(t.priority)}</td>
            <td>${formatDate(t.opened_at)}</td>
            <td><a href="ticket-detail.html?id=${t.id}" class="btn btn-sm btn-secondary">Ver</a></td>
        </tr>
    `).join('');
}

loadDashboard();