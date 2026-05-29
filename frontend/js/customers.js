requireAuth();

const user = getUser();
document.getElementById('user-name').textContent = `${user.first_name || user.username} (${user.role})`;
if (isAdmin()) document.getElementById('nav-users').style.display = 'block';
if (!isAttendant()) document.getElementById('btn-novo').style.display = 'none';

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('pt-BR');
}

async function loadCustomers() {
    const res = await api.get('/customers/');
    const tbody = document.getElementById('customers-table');

    if (res.status !== 200 || res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><p>Nenhum cliente encontrado.</p></td></tr>';
        return;
    }

    tbody.innerHTML = res.data.map(c => `
        <tr>
            <td>#${c.id}</td>
            <td>${c.name}</td>
            <td>${c.email}</td>
            <td>${c.phone}</td>
            <td><span class="badge ${c.is_active ? 'badge-resolvido' : 'badge-cancelado'}">${c.is_active ? 'Ativo' : 'Inativo'}</span></td>
            <td>${formatDate(c.created_at)}</td>
            <td style="display:flex;gap:6px">
                ${isAttendant() ? `<button class="btn btn-sm btn-secondary" onclick="openEditModal(${c.id})">Editar</button>` : ''}
                ${isAdmin() ? `<button class="btn btn-sm btn-danger" onclick="deleteCustomer(${c.id})">Del</button>` : ''}
            </td>
        </tr>
    `).join('');
}

function openModal() {
    document.getElementById('modal-title').textContent = 'Novo Cliente';
    document.getElementById('customer-id').value = '';
    document.getElementById('customer-name').value = '';
    document.getElementById('customer-email').value = '';
    document.getElementById('customer-phone').value = '';
    document.getElementById('active-group').style.display = 'none';
    document.getElementById('modal-alert').style.display = 'none';
    document.getElementById('modal-customer').classList.add('active');
}

async function openEditModal(id) {
    const res = await api.get(`/customers/${id}/`);
    const c = res.data;
    document.getElementById('modal-title').textContent = 'Editar Cliente';
    document.getElementById('customer-id').value = c.id;
    document.getElementById('customer-name').value = c.name;
    document.getElementById('customer-email').value = c.email;
    document.getElementById('customer-phone').value = c.phone;
    document.getElementById('customer-active').value = c.is_active ? 'true' : 'false';
    document.getElementById('active-group').style.display = 'block';
    document.getElementById('modal-alert').style.display = 'none';
    document.getElementById('modal-customer').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-customer').classList.remove('active');
}

async function saveCustomer() {
    const id = document.getElementById('customer-id').value;
    const name = document.getElementById('customer-name').value.trim();
    const email = document.getElementById('customer-email').value.trim();
    const phone = document.getElementById('customer-phone').value.trim();
    const is_active = document.getElementById('customer-active').value === 'true';
    const alertEl = document.getElementById('modal-alert');

    if (!name || !email || !phone) {
        alertEl.textContent = 'Preencha todos os campos.';
        alertEl.style.display = 'block';
        return;
    }

    const payload = { name, email, phone, is_active };
    const res = id
        ? await api.put(`/customers/${id}/`, payload)
        : await api.post('/customers/', payload);

    if (res.status === 200 || res.status === 201) {
        closeModal();
        loadCustomers();
    } else {
        alertEl.textContent = JSON.stringify(res.data);
        alertEl.style.display = 'block';
    }
}

async function deleteCustomer(id) {
    if (!confirm('Deseja remover este cliente?')) return;
    await api.delete(`/customers/${id}/`);
    loadCustomers();
}

loadCustomers();