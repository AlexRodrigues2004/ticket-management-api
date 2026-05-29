requireAuth();

const user = getUser();
document.getElementById('user-name').textContent = `${user.first_name || user.username} (${user.role})`;
if (isAdmin()) document.getElementById('nav-users').style.display = 'block';
if (!isAttendant()) document.getElementById('btn-novo').style.display = 'none';

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('pt-BR');
}

async function loadCategories() {
    const res = await api.get('/categories/');
    const tbody = document.getElementById('categories-table');

    if (res.status !== 200 || res.data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-state"><p>Nenhuma categoria encontrada.</p></td></tr>';
        return;
    }

    tbody.innerHTML = res.data.map(c => `
        <tr>
            <td>#${c.id}</td>
            <td>${c.name}</td>
            <td>${c.description || '—'}</td>
            <td>${formatDate(c.created_at)}</td>
            <td style="display:flex;gap:6px">
                ${isAttendant() ? `<button class="btn btn-sm btn-secondary" onclick="openEditModal(${c.id})">Editar</button>` : ''}
                ${isAdmin() ? `<button class="btn btn-sm btn-danger" onclick="deleteCategory(${c.id})">Del</button>` : ''}
            </td>
        </tr>
    `).join('');
}

function openModal() {
    document.getElementById('modal-title').textContent = 'Nova Categoria';
    document.getElementById('category-id').value = '';
    document.getElementById('category-name').value = '';
    document.getElementById('category-description').value = '';
    document.getElementById('modal-alert').style.display = 'none';
    document.getElementById('modal-category').classList.add('active');
}

async function openEditModal(id) {
    const res = await api.get(`/categories/${id}/`);
    const c = res.data;
    document.getElementById('modal-title').textContent = 'Editar Categoria';
    document.getElementById('category-id').value = c.id;
    document.getElementById('category-name').value = c.name;
    document.getElementById('category-description').value = c.description || '';
    document.getElementById('modal-alert').style.display = 'none';
    document.getElementById('modal-category').classList.add('active');
}

function closeModal() {
    document.getElementById('modal-category').classList.remove('active');
}

async function saveCategory() {
    const id = document.getElementById('category-id').value;
    const name = document.getElementById('category-name').value.trim();
    const description = document.getElementById('category-description').value.trim();
    const alertEl = document.getElementById('modal-alert');

    if (!name) {
        alertEl.textContent = 'Preencha o nome da categoria.';
        alertEl.style.display = 'block';
        return;
    }

    const payload = { name, description };
    const res = id
        ? await api.put(`/categories/${id}/`, payload)
        : await api.post('/categories/', payload);

    if (res.status === 200 || res.status === 201) {
        closeModal();
        loadCategories();
    } else {
        alertEl.textContent = JSON.stringify(res.data);
        alertEl.style.display = 'block';
    }
}

async function deleteCategory(id) {
    if (!confirm('Deseja remover esta categoria?')) return;
    await api.delete(`/categories/${id}/`);
    loadCategories();
}

loadCategories();