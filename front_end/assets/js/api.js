const BASE_URL = "http://127.0.0.1:8000/api";

function getToken() {
    return localStorage.getItem("access");
}

async function apiGet(endpoint) {
    return fetch(BASE_URL + endpoint, {
        headers: {
            "Authorization": "Bearer " + getToken(),
            "Content-Type": "application/json"
        }
    }).then(r => r.json());
}

async function apiPost(endpoint, data) {
    return fetch(BASE_URL + endpoint, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + getToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(r => r.json());
}
