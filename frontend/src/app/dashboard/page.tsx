"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { productsAPI, customersAPI } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import {
  Package,
  Users,
  ShoppingCart,
  LogOut,
  Store,
  Bot,
  UserPlus,
  Crown,
} from "lucide-react";
import Link from "next/link";

interface Product {
  id: number;
  name: string;
  selling_price: number;
  stock: number;
  unit: string;
}

interface Customer {
  id: number;
  name: string;
  phone: string;
  debt_amount: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, isAuthenticated, isOwner, isAdmin } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    loadData();
  }, [isAuthenticated, router]);

  const loadData = async () => {
    try {
      const [productsRes, customersRes] = await Promise.all([
        productsAPI.getAll(),
        customersAPI.getAll(),
      ]);
      setProducts(productsRes.data || []);
      setCustomers(customersRes.data || []);
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  const totalDebt = customers.reduce((sum, c) => sum + (c.debt_amount || 0), 0);
  const lowStockProducts = products.filter((p) => p.stock < 20);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-white/5">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-violet-500 to-indigo-500 rounded-lg flex items-center justify-center">
              <Store className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-white">BizFlow</h1>
                <Badge
                  className={
                    isAdmin
                      ? "bg-yellow-500"
                      : isOwner
                        ? "bg-purple-500"
                        : "bg-blue-500"
                  }
                >
                  {isAdmin
                    ? "Admin Platform"
                    : isOwner
                      ? "Chủ cửa hàng"
                      : "Nhân viên"}
                </Badge>
              </div>
              <p className="text-xs text-violet-300">
                Xin chào, {user?.full_name || user?.username}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/pos">
              <Button
                variant="outline"
                className="border-white/20 text-white hover:bg-white/10"
              >
                <ShoppingCart className="w-4 h-4 mr-2" />
                Bán hàng
              </Button>
            </Link>
            <Link href="/products">
              <Button
                variant="outline"
                className="border-white/20 text-white hover:bg-white/10"
              >
                <Package className="w-4 h-4 mr-2" />
                Sản phẩm
              </Button>
            </Link>
            <Link href="/customers">
              <Button
                variant="outline"
                className="border-white/20 text-white hover:bg-white/10"
              >
                <Users className="w-4 h-4 mr-2" />
                Khách hàng
              </Button>
            </Link>
            <Link href="/ai">
              <Button className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600">
                <Bot className="w-4 h-4 mr-2" />
                Trợ lý AI
              </Button>
            </Link>
            {isOwner && (
              <Link href="/dashboard/users">
                <Button
                  variant="outline"
                  className="border-purple-500/50 text-purple-400 hover:bg-purple-500/10"
                >
                  <UserPlus className="w-4 h-4 mr-2" />
                  Nhân viên
                </Button>
              </Link>
            )}
            {isAdmin && (
              <Link href="/dashboard/admin">
                <Button
                  variant="outline"
                  className="border-yellow-500/50 text-yellow-400 hover:bg-yellow-500/10"
                >
                  <Crown className="w-4 h-4 mr-2" />
                  Admin
                </Button>
              </Link>
            )}
            <Button
              variant="ghost"
              onClick={handleLogout}
              className="text-red-400 hover:text-red-300 hover:bg-red-500/10"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Đăng xuất
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-violet-200">
                Tổng sản phẩm
              </CardTitle>
              <Package className="w-5 h-5 text-violet-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">
                {loading ? "..." : products.length}
              </div>
              <p className="text-xs text-violet-300 mt-1">
                {lowStockProducts.length} sản phẩm sắp hết hàng
              </p>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-violet-200">
                Khách hàng
              </CardTitle>
              <Users className="w-5 h-5 text-emerald-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-white">
                {loading ? "..." : customers.length}
              </div>
              <p className="text-xs text-violet-300 mt-1">Đang hoạt động</p>
            </CardContent>
          </Card>

          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-violet-200">
                {isOwner ? "Tổng công nợ" : "Chức năng"}
              </CardTitle>
              <ShoppingCart className="w-5 h-5 text-amber-400" />
            </CardHeader>
            <CardContent>
              {isOwner ? (
                <>
                  <div className="text-3xl font-bold text-amber-400">
                    {loading ? "..." : formatCurrency(totalDebt)}
                  </div>
                  <p className="text-xs text-violet-300 mt-1">Cần thu hồi</p>
                </>
              ) : (
                <>
                  <div className="text-xl font-bold text-emerald-400">
                    Bán hàng & Xem SP
                  </div>
                  <p className="text-xs text-violet-300 mt-1">
                    Quyền hạn của bạn
                  </p>
                </>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Products List */}
        <Card className="backdrop-blur-xl bg-white/10 border-white/20 mb-8">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Package className="w-5 h-5" />
              Danh sách sản phẩm
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center text-violet-300 py-8">
                Đang tải...
              </div>
            ) : products.length === 0 ? (
              <div className="text-center text-violet-300 py-8">
                Chưa có sản phẩm nào
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {products.map((product) => (
                  <div
                    key={product.id}
                    className="p-4 rounded-lg bg-white/5 border border-white/10"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium text-white">{product.name}</h3>
                      <Badge
                        variant={product.stock < 20 ? "destructive" : "default"}
                      >
                        {product.stock} {product.unit}
                      </Badge>
                    </div>
                    <p className="text-emerald-400 font-bold">
                      {formatCurrency(product.selling_price)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Customers with Debt - Only for Owner */}
        {isOwner && (
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Users className="w-5 h-5" />
                Khách hàng có công nợ
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center text-violet-300 py-8">
                  Đang tải...
                </div>
              ) : (
                <div className="space-y-3">
                  {customers
                    .filter((c) => c.debt_amount > 0)
                    .map((customer) => (
                      <div
                        key={customer.id}
                        className="flex justify-between items-center p-3 rounded-lg bg-white/5 border border-white/10"
                      >
                        <div>
                          <h3 className="font-medium text-white">
                            {customer.name}
                          </h3>
                          <p className="text-sm text-violet-300">
                            {customer.phone}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-amber-400 font-bold">
                            {formatCurrency(customer.debt_amount)}
                          </p>
                        </div>
                      </div>
                    ))}
                  {customers.filter((c) => c.debt_amount > 0).length === 0 && (
                    <div className="text-center text-violet-300 py-4">
                      Không có khách hàng nợ
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
}
