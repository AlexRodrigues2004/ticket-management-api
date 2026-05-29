function isAuthenticated() {
    return !!localStorage.getItem('access_token');
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
    }
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function isAdmin() {
    const user = getUser();
    return user && user.role === 'admin';
}

function isAttendant() {
    const user = getUser();
    return user && (user.role === 'atendente' || user.role === 'admin');
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

async function login(username, password) {
    const response = await fetch(`${API_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        const meRes = await api.get('/auth/me/');
        localStorage.setItem('user', JSON.stringify(meRes.data));

        return { success: true };
    }
    return { success: false };
}