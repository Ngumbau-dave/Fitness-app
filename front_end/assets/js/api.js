// API Helper for FitTrack Frontend
const BASE_URL = 'https://fittrack-api-7b9k.onrender.com';  // Local backend

// Token from localStorage (for JWT - we'll use later)
function getToken() {
    return localStorage.getItem("access_token");
}

// Generic GET request
// Generic GET request
async function apiGet(endpoint) {
    const token = localStorage.getItem('access_token');
    const headers = {
        "Content-Type": "application/json"
    };
    if (token && token.trim() !== '' && token !== 'null' && token !== 'undefined') {
        headers["Authorization"] = `Bearer ${token.trim()}`;
    }
    const response = await fetch(BASE_URL + endpoint, { headers });
    if (!response.ok) {
        const errorText = await response.text();
        console.error('API GET error:', response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

async function apiPost(endpoint, data) {
    const token = localStorage.getItem('access_token');
    const headers = {
        "Content-Type": "application/json"
    };
    if (token && token.trim() !== '' && token !== 'null' && token !== 'undefined') {
        headers["Authorization"] = `Bearer ${token.trim()}`;
    }
    const response = await fetch(BASE_URL + endpoint, {
        method: "POST",
        headers,
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const errorText = await response.text();
        console.error('API POST error:', response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

// Do the same for apiGet if needed

async function loginUser(event) {
    event.preventDefault();  // Stop form reload

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('error');

    if (!username || !password) {
        errorEl.textContent = 'Please enter username and password';
        return;
    }

    errorEl.textContent = '';  // Clear previous errors

    try {
        // Adjust endpoint if yours is different (common: /api/token/, /api/login/, /api/token/obtain/)
        const data = await apiPost('/api/token/', { username, password });

        // SimpleJWT returns {refresh, access}
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);  // Optional

        // Success! Redirect to dashboard or home
        window.location.href = 'dashboard.html';  // Change to your protected page
    } catch (err) {
        console.error('Login error:', err);

        // Better error handling
        if (err.message.includes('401')) {
            errorEl.textContent = 'Invalid username or password';
        } else if (err.message.includes('404')) {
            errorEl.textContent = 'Login endpoint not found—check backend URL';
        } else {
            errorEl.textContent = 'Login failed: ' + err.message;
        }
    }
}



// Example usage in other files:
// await apiGet(ACTIVITIES_ENDPOINT)
// await apiPost(ACTIVITIES_ENDPOINT, newActivityData)