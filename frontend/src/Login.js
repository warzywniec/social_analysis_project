import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username, password }),
    });
    const data = await response.json();
    if (data.access_token) {
        localStorage.setItem("token", data.access_token); // ✅ zapisz token
        alert("Zalogowano!");
        navigate("/main");
      } else {
      alert("Błąd logowania");
    }
  };

  return (
    <div>
      <h2>Logowanie</h2>
      <form onSubmit={handleLogin}>
        <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Login" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Hasło" />
        <button type="submit">Zaloguj</button>
      </form>
      <Link to="/register">Nie masz konta? Zarejestruj się</Link>
    </div>
  );
}
