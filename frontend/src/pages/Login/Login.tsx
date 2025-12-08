import { useState } from "react";
import { login as authLogin } from "../../API/auth";
import { useAuth } from "../../context/AuthContext";
import "./Login.css";

export default function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const data = await authLogin(email, password);
      login(data.user, data.token);
      window.location.href = "/dashboard";
    } catch (error) {
      alert("Credenciais inválidas");
    }
  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <h2>Entrar</h2>
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}
