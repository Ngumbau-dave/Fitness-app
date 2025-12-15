// API Base (for activities and other endpoints)
const API_BASE = 'https://fittrack-api-7b9k.onrender.com';

// Login function
async function loginUser(event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('error');

    if (!username || !password) {
        errorEl.textContent = 'Please fill in both fields';
        return;
    }

    errorEl.textContent = '';

    try {
        const data = await apiPost('/api/token/', { username, password });

        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);  // Optional but good to have

        // Redirect to your main app page
        window.location.href = 'dashboard.html';  // Or 'index.html', etc.
    } catch (err) {
        console.error(err);
        if (err.message.includes('401')) {
            errorEl.textContent = 'Invalid username or password';
        } else {
            errorEl.textContent = 'Login failed – try again later';
        }
    }
}
// Logout
function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.location.href = "index.html";
}

// Helper to get token for API calls
function getToken() {
    return localStorage.getItem("access_token");
}

// Optional: Add token to all API requests (use in api.js)
async function apiFetch(endpoint, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };

    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(API_BASE + endpoint, {
        ...options,
        headers
    });

    if (response.status === 401) {
        // Token expired — optional: refresh or logout
        logout();
    }

    return response;
}