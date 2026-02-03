"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface User {
  id: number;
  username: string;
  full_name?: string;
  role: string;
  subscription: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean; // Platform admin - quyền cao nhất
  isOwner: boolean; // Chủ cửa hàng
  isEmployee: boolean; // Nhân viên
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const savedUser = localStorage.getItem("bizflow_user");
    const savedToken = localStorage.getItem("bizflow_token");

    if (savedUser && savedToken) {
      setUser(JSON.parse(savedUser));
      setToken(savedToken);
    }
  }, []);

  const login = (user: User, token: string) => {
    setUser(user);
    setToken(token);
    localStorage.setItem("bizflow_user", JSON.stringify(user));
    localStorage.setItem("bizflow_token", token);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("bizflow_user");
    localStorage.removeItem("bizflow_token");
  };

  if (!mounted) {
    return null;
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isAuthenticated: !!user && !!token,
        isAdmin: user?.role === "admin", // Platform admin
        isOwner: user?.role === "owner", // Chủ cửa hàng
        isEmployee: user?.role === "employee", // Nhân viên
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
