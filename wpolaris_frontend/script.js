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

document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;

  try {
    const response = await fetch("https://wpolaris-1.onrender.com/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      alert("Registro exitoso");
    } else {
      alert("Error: " + data.detail);
    }
  } catch (error) {
    console.error("Error de red:", error);
    alert("No se pudo conectar con el servidor");
  }
});