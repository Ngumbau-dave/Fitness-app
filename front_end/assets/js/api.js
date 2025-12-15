// API Helper for FitTrack Frontend
const BASE_URL = 'https://fittrack-api-7b9k.onrender.com';  // Local backend

// Token from localStorage (for JWT - we'll use later)
function getToken() {
    return localStorage.getItem("access_token");
}

// Generic GET request
async function apiGet(endpoint) {
    const response = await fetch(BASE_URL + endpoint, {
        headers: {
            "Authorization": `Bearer ${getToken() || ''}`,  // Safe if no token
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

// Generic POST request
async function apiPost(endpoint, data) {
    const response = await fetch(BASE_URL + endpoint, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${getToken() || ''}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

/


// Example usage in other files:
// await apiGet(ACTIVITIES_ENDPOINT)
// await apiPost(ACTIVITIES_ENDPOINT, newActivityData)