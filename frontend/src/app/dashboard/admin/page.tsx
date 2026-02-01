"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import {
  Shield,
  Users,
  Store,
  User,
  UserPlus,
  ArrowLeft,
  Power,
  PowerOff,
  Search,
  Crown,
} from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

interface UserData {
  id: number;
  username: string;
  full_name: string;
  role: string;
  status: string;
}

const BASE_URL = "/api";

// API functions
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
    throw new Error(data.error || "Không thể tải danh sách tài khoản");
  return data.data || data.users || [];
}

async function toggleUserStatus(userId: number) {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("bizflow_token")
      : null;
  const response = await fetch(
    `${BASE_URL}/auth/users/${userId}/toggle-status`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    },
  );
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Không thể cập nhật trạng thái");
  }
  return data;
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
    let errorMsg = "Không thể tạo tài khoản";
    if (typeof data.error === "string") {
      errorMsg = data.error;
    } else if (typeof data.error === "object") {
      errorMsg = JSON.stringify(data.error);
    }
    throw new Error(errorMsg);
  }
  return data;
}

export default function AdminPage() {
  const router = useRouter();
  const { isAuthenticated, isAdmin, user } = useAuth();
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterRole, setFilterRole] = useState<string>("all");
  const [showForm, setShowForm] = useState(false);
  const [creating, setCreating] = useState(false);
  const [newUser, setNewUser] = useState({
    username: "",
    password: "",
    full_name: "",
    role: "owner",
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    if (!isAdmin) {
      toast.error("Chỉ Admin Platform mới có quyền truy cập!");
      router.push("/dashboard");
      return;
    }
    loadUsers();
  }, [isAuthenticated, isAdmin, router]);

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

  const handleToggleStatus = async (userId: number, currentStatus: string) => {
    try {
      const result = await toggleUserStatus(userId);
      toast.success(result.message);
      loadUsers();
    } catch (error: any) {
      toast.error(error.message);
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
        role: "owner",
      });
      setShowForm(false);
      loadUsers();
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setCreating(false);
    }
  };

  // Filter users
  const filteredUsers = users.filter((u) => {
    const matchSearch =
      u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u.full_name || "").toLowerCase().includes(searchTerm.toLowerCase());
    const matchRole = filterRole === "all" || u.role === filterRole;
    // Don't show admin accounts in the list (can't disable yourself)
    return matchSearch && matchRole && u.role !== "admin";
  });

  // Stats
  const activeOwners = users.filter(
    (u) => u.role === "owner" && u.status === "active",
  ).length;
  const inactiveOwners = users.filter(
    (u) => u.role === "owner" && u.status === "inactive",
  ).length;
  const totalEmployees = users.filter((u) => u.role === "employee").length;

  if (!isAuthenticated || !isAdmin) {
    return null;
  }

  const getRoleIcon = (role: string) => {
    switch (role) {
      case "admin":
        return <Crown className="w-5 h-5 text-yellow-400" />;
      case "owner":
        return <Store className="w-5 h-5 text-purple-400" />;
      default:
        return <User className="w-5 h-5 text-blue-400" />;
    }
  };

  const getRoleBadge = (role: string) => {
    switch (role) {
      case "admin":
        return (
          <Badge className="bg-yellow-500 hover:bg-yellow-600">
            Admin Platform
          </Badge>
        );
      case "owner":
        return (
          <Badge className="bg-purple-500 hover:bg-purple-600">
            Chủ cửa hàng
          </Badge>
        );
      default:
        return (
          <Badge className="bg-blue-500 hover:bg-blue-600">Nhân viên</Badge>
        );
    }
  };

  const getStatusBadge = (status: string) => {
    if (status === "active") {
      return (
        <Badge className="bg-emerald-500 hover:bg-emerald-600">Hoạt động</Badge>
      );
    }
    return <Badge className="bg-red-500 hover:bg-red-600">Vô hiệu</Badge>;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
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
                <Crown className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Admin Platform</h1>
                <p className="text-xs text-yellow-300">
                  Quản lý toàn bộ hệ thống
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge className="bg-yellow-500/20 text-yellow-300 border border-yellow-500/30">
              <Crown className="w-3 h-3 mr-1" />
              {user?.full_name || user?.username}
            </Badge>
            <Button
              onClick={() => setShowForm(!showForm)}
              className="bg-gradient-to-r from-emerald-500 to-teal-500"
            >
              <UserPlus className="w-4 h-4 mr-2" />
              Thêm Owner
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                  <Store className="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <p className="text-sm text-violet-300">Owners hoạt động</p>
                  <p className="text-2xl font-bold text-white">
                    {activeOwners}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
                  <PowerOff className="w-6 h-6 text-red-400" />
                </div>
                <div>
                  <p className="text-sm text-violet-300">Owners vô hiệu</p>
                  <p className="text-2xl font-bold text-white">
                    {inactiveOwners}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                  <Users className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-sm text-violet-300">Tổng nhân viên</p>
                  <p className="text-2xl font-bold text-white">
                    {totalEmployees}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-emerald-500/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-emerald-400" />
                </div>
                <div>
                  <p className="text-sm text-violet-300">Tổng tài khoản</p>
                  <p className="text-2xl font-bold text-white">
                    {users.length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* User List */}
          <div className="lg:col-span-2">
            <Card className="backdrop-blur-xl bg-white/10 border-white/20">
              <CardHeader>
                <div className="flex flex-col sm:flex-row justify-between gap-4">
                  <CardTitle className="text-white flex items-center gap-2">
                    <Users className="w-5 h-5" />
                    Quản lý tài khoản
                  </CardTitle>
                  <div className="flex gap-2">
                    <div className="relative">
                      <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-violet-300" />
                      <Input
                        placeholder="Tìm kiếm..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-9 bg-white/10 border-white/20 text-white w-48"
                      />
                    </div>
                    <select
                      value={filterRole}
                      onChange={(e) => setFilterRole(e.target.value)}
                      className="px-3 py-2 rounded-md bg-white/10 border border-white/20 text-white text-sm"
                    >
                      <option value="all" className="bg-slate-800">
                        Tất cả
                      </option>
                      <option value="owner" className="bg-slate-800">
                        Chủ cửa hàng
                      </option>
                      <option value="employee" className="bg-slate-800">
                        Nhân viên
                      </option>
                    </select>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center text-violet-300 py-8">
                    Đang tải...
                  </div>
                ) : filteredUsers.length === 0 ? (
                  <div className="text-center text-violet-300 py-8">
                    Không tìm thấy tài khoản nào
                  </div>
                ) : (
                  <div className="space-y-3">
                    {filteredUsers.map((u) => (
                      <div
                        key={u.id}
                        className={`p-4 rounded-lg border flex items-center justify-between ${
                          u.status === "inactive"
                            ? "bg-red-500/10 border-red-500/30"
                            : "bg-white/5 border-white/10"
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center ${
                              u.status === "inactive"
                                ? "bg-gray-500/20"
                                : u.role === "owner"
                                  ? "bg-purple-500/20"
                                  : "bg-blue-500/20"
                            }`}
                          >
                            {getRoleIcon(u.role)}
                          </div>
                          <div>
                            <p
                              className={`font-medium ${
                                u.status === "inactive"
                                  ? "text-gray-400 line-through"
                                  : "text-white"
                              }`}
                            >
                              {u.full_name || u.username}
                            </p>
                            <p className="text-sm text-violet-300">
                              @{u.username}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {getRoleBadge(u.role)}
                          {getStatusBadge(u.status)}
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleToggleStatus(u.id, u.status)}
                            className={
                              u.status === "active"
                                ? "text-red-400 hover:text-red-300 hover:bg-red-500/20"
                                : "text-emerald-400 hover:text-emerald-300 hover:bg-emerald-500/20"
                            }
                            title={
                              u.status === "active"
                                ? "Vô hiệu hóa"
                                : "Kích hoạt"
                            }
                          >
                            {u.status === "active" ? (
                              <PowerOff className="w-4 h-4" />
                            ) : (
                              <Power className="w-4 h-4" />
                            )}
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Add Owner Form */}
          <div className={showForm ? "block" : "hidden lg:block"}>
            <Card className="backdrop-blur-xl bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <UserPlus className="w-5 h-5" />
                  Thêm chủ cửa hàng mới
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
                      placeholder="cuahang1"
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
                      <option value="owner" className="bg-slate-800">
                        Chủ cửa hàng
                      </option>
                      <option value="employee" className="bg-slate-800">
                        Nhân viên
                      </option>
                    </select>
                  </div>
                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-yellow-500 to-orange-500"
                    disabled={creating}
                  >
                    {creating ? "Đang tạo..." : "Tạo tài khoản"}
                  </Button>
                </form>

                <div className="mt-6 p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
                  <h4 className="text-yellow-300 font-medium mb-2 flex items-center gap-2">
                    <Shield className="w-4 h-4" />
                    Quyền Admin Platform
                  </h4>
                  <ul className="text-sm text-yellow-200/80 space-y-1">
                    <li>• Xem tất cả tài khoản trên hệ thống</li>
                    <li>• Tạo tài khoản Owner/Employee mới</li>
                    <li>• Vô hiệu hóa khi không thanh toán phí</li>
                    <li>• Kích hoạt lại tài khoản</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
