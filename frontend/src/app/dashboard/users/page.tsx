"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { formatCurrency } from "@/lib/utils";
import { Users, UserPlus, ArrowLeft, Shield, User, Store } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

interface UserData {
  id: number;
  username: string;
  full_name: string;
  role: string;
  created_at?: string;
}

const BASE_URL = "/api";

// API functions for users
async function getUsers(): Promise<UserData[]> {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("bizflow_token")
      : null;
  const response = await fetch(`${BASE_URL}/auth/users`, {
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
  });
  const data = await response.json();
  if (!response.ok)
    throw new Error(data.error || "Không thể tải danh sách nhân viên");
  return data.data || data.users || [];
}

async function createUser(userData: {
  username: string;
  password: string;
  full_name: string;
  role: string;
}) {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("bizflow_token")
      : null;
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify(userData),
  });
  const data = await response.json();
  if (!response.ok) {
    // Handle error - could be string or object
    let errorMsg = "Không thể tạo tài khoản";
    if (typeof data.error === "string") {
      errorMsg = data.error;
    } else if (typeof data.error === "object") {
      errorMsg = JSON.stringify(data.error);
    } else if (data.message) {
      errorMsg = data.message;
    }
    throw new Error(errorMsg);
  }
  return data;
}

export default function UsersPage() {
  const router = useRouter();
  const { isAuthenticated, isOwner } = useAuth();
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [newUser, setNewUser] = useState({
    username: "",
    password: "",
    full_name: "",
    role: "employee",
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    if (!isOwner) {
      toast.error("Bạn không có quyền truy cập trang này");
      router.push("/dashboard");
      return;
    }
    loadUsers();
  }, [isAuthenticated, isOwner, router]);

  const loadUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error: any) {
      console.error("Error loading users:", error);
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newUser.username || !newUser.password || !newUser.full_name) {
      toast.error("Vui lòng điền đầy đủ thông tin");
      return;
    }

    setCreating(true);
    try {
      await createUser(newUser);
      toast.success("Tạo tài khoản thành công!");
      setNewUser({
        username: "",
        password: "",
        full_name: "",
        role: "employee",
      });
      setShowForm(false);
      loadUsers();
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setCreating(false);
    }
  };

  if (!isAuthenticated || !isOwner) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-white/5 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button
                variant="ghost"
                size="icon"
                className="text-white hover:bg-white/10"
              >
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">
                  Quản lý nhân viên
                </h1>
                <p className="text-xs text-violet-300">
                  Tạo và quản lý tài khoản
                </p>
              </div>
            </div>
          </div>
          <Button
            onClick={() => setShowForm(!showForm)}
            className="bg-gradient-to-r from-emerald-500 to-teal-500"
          >
            <UserPlus className="w-4 h-4 mr-2" />
            Thêm nhân viên
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* User List */}
          <div className="lg:col-span-2">
            <Card className="backdrop-blur-xl bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  Danh sách tài khoản ({users.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center text-violet-300 py-8">
                    Đang tải...
                  </div>
                ) : users.length === 0 ? (
                  <div className="text-center text-violet-300 py-8">
                    Chưa có nhân viên nào
                  </div>
                ) : (
                  <div className="space-y-3">
                    {users.map((user) => (
                      <div
                        key={user.id}
                        className="p-4 rounded-lg bg-white/5 border border-white/10 flex items-center justify-between"
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center ${
                              user.role === "owner"
                                ? "bg-red-500/20"
                                : "bg-blue-500/20"
                            }`}
                          >
                            {user.role === "owner" ? (
                              <Shield className="w-5 h-5 text-red-400" />
                            ) : (
                              <User className="w-5 h-5 text-blue-400" />
                            )}
                          </div>
                          <div>
                            <p className="font-medium text-white">
                              {user.full_name || user.username}
                            </p>
                            <p className="text-sm text-violet-300">
                              @{user.username}
                            </p>
                          </div>
                        </div>
                        <Badge
                          className={
                            user.role === "owner"
                              ? "bg-red-500 hover:bg-red-600"
                              : "bg-blue-500 hover:bg-blue-600"
                          }
                        >
                          {user.role === "owner" ? "Admin" : "Nhân viên"}
                        </Badge>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Add User Form */}
          <div className={showForm ? "block" : "hidden lg:block"}>
            <Card className="backdrop-blur-xl bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <UserPlus className="w-5 h-5" />
                  Thêm nhân viên mới
                </CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreateUser} className="space-y-4">
                  <div>
                    <Label className="text-white">Họ và tên</Label>
                    <Input
                      value={newUser.full_name}
                      onChange={(e) =>
                        setNewUser({ ...newUser, full_name: e.target.value })
                      }
                      className="bg-white/10 border-white/20 text-white"
                      placeholder="Nguyễn Văn A"
                      required
                    />
                  </div>
                  <div>
                    <Label className="text-white">Tên đăng nhập</Label>
                    <Input
                      value={newUser.username}
                      onChange={(e) =>
                        setNewUser({ ...newUser, username: e.target.value })
                      }
                      className="bg-white/10 border-white/20 text-white"
                      placeholder="nhanvien1"
                      required
                    />
                  </div>
                  <div>
                    <Label className="text-white">Mật khẩu</Label>
                    <Input
                      type="password"
                      value={newUser.password}
                      onChange={(e) =>
                        setNewUser({ ...newUser, password: e.target.value })
                      }
                      className="bg-white/10 border-white/20 text-white"
                      placeholder="••••••••"
                      required
                    />
                  </div>
                  <div>
                    <Label className="text-white">Vai trò</Label>
                    <select
                      value={newUser.role}
                      onChange={(e) =>
                        setNewUser({ ...newUser, role: e.target.value })
                      }
                      className="w-full p-2 rounded-md bg-white/10 border border-white/20 text-white"
                    >
                      <option value="employee" className="bg-slate-800">
                        Nhân viên
                      </option>
                      <option value="owner" className="bg-slate-800">
                        Admin
                      </option>
                    </select>
                  </div>
                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-emerald-500 to-teal-500"
                    disabled={creating}
                  >
                    {creating ? "Đang tạo..." : "Tạo tài khoản"}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
