requireAuth();

const user = getUser();
document.getElementById('user-name').textContent = `${user.first_name || user.username} (${user.role})`;
if (isAdmin()) document.getElementById('nav-users').style.display = 'block';

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric'
    });
}

function badgeStatus(status) {
    const labels = {
        aberto: 'Aberto', em_atendimento: 'Em Atendimento',
        aguardando_cliente: 'Aguardando', resolvido: 'Resolvido', cancelado: 'Cancelado'
    };
    return `<span class="badge badge-${status}">${labels[status] || status}</span>`;
}

function badgePriority(p) {
    const labels = { baixa: 'Baixa', media: 'Média', alta: 'Alta', critica: 'Crítica' };
    return `<span class="badge badge-${p}">${labels[p] || p}</span>`;
}

async function loadTickets() {
    const status = document.getElementById('filter-status').value;
    const priority = document.getElementById('filter-priority').value;
    const search = document.getElementById('filter-search').value;

    let query = '/tickets/?';
    if (status) query += `status=${status}&`;
    if (priority) query += `priority=${priority}&`;
    if (search) query += `search=${encodeURIComponent(search)}&`;

    const res = await api.get(query);
    const tbody = document.getElementById('tickets-table');

    if (res.status !== 200 || res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="empty-state"><p>Nenhum chamado encontrado.</p></td></tr>';
        return;
    }

    tbody.innerHTML = res.data.map(t => `
        <tr>
            <td>#${t.id}</td>
            <td>${t.title}</td>
            <td>${t.customer_detail?.name || '—'}</td>
            <td>${t.category_detail?.name || '—'}</td>
            <td>${badgeStatus(t.status)}</td>
            <td>${badgePriority(t.priority)}</td>
            <td>${formatDate(t.opened_at)}</td>
            <td style="display:flex;gap:6px">
                <a href="ticket-detail.html?id=${t.id}" class="btn btn-sm btn-secondary">Ver</a>
                ${isAttendant() ? `<button class="btn btn-sm btn-primary" onclick="openStatusModal(${t.id}, '${t.status}', '${t.priority}')">Status</button>` : ''}
                ${isAdmin() ? `<button class="btn btn-sm btn-danger" onclick="deleteTicket(${t.id})">Del</button>` : ''}
            </td>
        </tr>
    `).join('');
}

async function loadSelects() {
    const [customers, categories] = await Promise.all([
        api.get('/customers/'),
        api.get('/categories/')
    ]);

    const custSelect = document.getElementById('ticket-customer');
    const catSelect = document.getElementById('ticket-category');

    custSelect.innerHTML = customers.data.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    catSelect.innerHTML = categories.data.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

function openModal() {
    loadSelects();
    document.getElementById('modal-ticket').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-ticket').classList.remove('active');
    document.getElementById('modal-alert').style.display = 'none';
}

function openStatusModal(id, status, priority) {
    document.getElementById('status-ticket-id').value = id;
    document.getElementById('status-value').value = status;
    document.getElementById('priority-value').value = priority;
    document.getElementById('modal-status').classList.add('active');
}

function closeStatusModal() {
    document.getElementById('modal-status').classList.remove('active');
}

async function createTicket() {
    const title = document.getElementById('ticket-title').value.trim();
    const description = document.getElementById('ticket-description').value.trim();
    const customer = document.getElementById('ticket-customer').value;
    const category = document.getElementById('ticket-category').value;
    const priority = document.getElementById('ticket-priority').value;
    const alertEl = document.getElementById('modal-alert');

    if (!title || !description) {
        alertEl.textContent = 'Preencha título e descrição.';
        alertEl.style.display = 'block';
        return;
    }

    const res = await api.post('/tickets/', { title, description, customer, category, priority });

    if (res.status === 201) {
        closeModal();
        loadTickets();
    } else {
        alertEl.textContent = JSON.stringify(res.data);
        alertEl.style.display = 'block';
    }
}

async function updateStatus() {
    const id = document.getElementById('status-ticket-id').value;
    const status = document.getElementById('status-value').value;
    const priority = document.getElementById('priority-value').value;

    const res = await api.patch(`/tickets/${id}/status/`, { status, priority });
    if (res.status === 200) {
        closeStatusModal();
        loadTickets();
    }
}

async function deleteTicket(id) {
    if (!confirm('Deseja remover este chamado?')) return;
    await api.delete(`/tickets/${id}/`);
    loadTickets();
}

function clearFilters() {
    document.getElementById('filter-status').value = '';
    document.getElementById('filter-priority').value = '';
    document.getElementById('filter-search').value = '';
    loadTickets();
}

loadTickets();