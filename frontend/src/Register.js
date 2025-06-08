import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:8000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (data.access_token) {
      alert("Zarejestrowano!");
      navigate("/"); // po rejestracji wracamy do logowania
    } else {
      alert("Błąd rejestracji");
    }
  };

  return (
    <div>
      <h2>Rejestracja</h2>
      <form onSubmit={handleRegister}>
        <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Login" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Hasło" />
        <button type="submit">Zarejestruj</button>
      </form>
      <Link to="/">Masz konto? Zaloguj się</Link>
    </div>
  );
}
