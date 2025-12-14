async function loginUser(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    if (data.access) {
        localStorage.setItem("token", data.access);
        window.location.href = "dashboard.html";  // redirect
    } else {
        alert("Invalid login. Try again.");
    }
}

// Logout
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
    const API_BASE = 'http://127.0.0.1:8000/api/activities/';
}
