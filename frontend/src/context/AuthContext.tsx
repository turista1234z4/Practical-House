import { createContext, useState, useContext} from "react";
import type {ReactNode} from "react";

interface AuthContextType {
  user: any;
  token: string | null;
  login: (user: any, token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [token, setToken] = useState<string | null>(null);

  function login(userData: any, jwt: string) {
    setUser(userData);
    setToken(jwt);
    localStorage.setItem("token", jwt);
  }

  function logout() {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}
