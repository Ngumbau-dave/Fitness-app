// API Base (for activities and other endpoints)
const API_BASE = 'http://127.0.0.1:8000/api/activities/';

// Login function
async function loginUser(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Please enter username and password");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/token/', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Invalid credentials');
        }

        const data = await response.json();

        // Save both tokens (access for API calls, refresh for renewal)
        localStorage.setItem("access_token", data.access);
        localStorage.setItem("refresh_token", data.refresh);

        alert("Login successful!");
        window.location.href = "dashboard.html";
    } catch (error) {
        alert("Login failed: " + error.message);
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