async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const BACKEND_URL = "https://wpolaris-1.onrender.com";

  const res = await fetch(`${BACKEND_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (res.ok) {
    alert("Login exitoso. Token: " + data.access_token);
    localStorage.setItem("token", data.access_token);
  } else {
    alert("Error: " + data.detail);
  }
}

async function getVault() {
  const token = localStorage.getItem("token");

  const res = await fetch("https://wpolaris-1.onrender.com/vault", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (res.ok) {
    console.log(data);
    alert("Vault: " + JSON.stringify(data));
  } else {
    alert("Error al acceder al vault: " + data.detail);
  }
}