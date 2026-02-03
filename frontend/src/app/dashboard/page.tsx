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
  UserPlus,
  Crown,
  Eye,
  FileText,
  BookOpen,
} from "lucide-react";
import Link from "next/link";
import { NotificationBell } from "@/components/NotificationBell";
import { AiOrderDialog } from "@/components/ai/AiOrderDialog";

interface Product {
  id: number;
  name: string;
  price: number;
  selling_price?: number;
  stock: number;
  unit: string;
}

interface Customer {
  id: number;
  name: string;
  phone: string;
  debt_amount: number;
}

interface Order {
  id: number;
  customer_name: string;
  created_by: string;
  total_amount: number;
  payment_method: string;
  created_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, isAuthenticated, isOwner, isAdmin } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
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
      const { productsAPI, customersAPI, ordersAPI } = await import("@/lib/api");
      const [productsRes, customersRes, ordersRes] = await Promise.all([
        productsAPI.getAll(),
        customersAPI.getAll(),
        ordersAPI.getAll(1, 5),
      ]);
      setProducts(productsRes.data || []);
      setCustomers(customersRes.data || []);
      setOrders(ordersRes.orders || []);
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
                {isOwner && (
                  <Link href="/dashboard/subscription">
                    <Badge variant="outline" className="border-emerald-500 text-emerald-400 hover:bg-emerald-500/10 cursor-pointer">
                      Gói {user?.subscription?.toUpperCase() || "BASIC"}
                    </Badge>
                  </Link>
                )}
              </div>
              <p className="text-xs text-violet-300">
                Xin chào, {user?.full_name || user?.username}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <NotificationBell />
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
            {isOwner && (
              <Link href="/dashboard/reports">
                <Button
                  variant="outline"
                  className="border-yellow-500/50 text-yellow-400 hover:bg-yellow-500/10"
                >
                  <BookOpen className="w-4 h-4 mr-2" />
                  Sổ sách
                </Button>
              </Link>
            )}
            <AiOrderDialog onSuccess={loadData} />
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
        </div >
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
                    Bán hàng & Xem sản phẩm
                  </div>
                  <p className="text-xs text-violet-300 mt-1">
                    Quyền hạn của bạn
                  </p>
                </>
              )}
            </CardContent>
          </Card>
        </div >

        {/* Recent Orders */}
        <Card className="backdrop-blur-xl bg-white/10 border-white/20 mb-8">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-400" />
              Đơn hàng gần đây
            </CardTitle>
            <Button variant="ghost" className="text-violet-300 hover:text-white text-xs">
              Xem tất cả
            </Button>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center text-violet-300 py-8">Đang tải...</div>
            ) : orders.length === 0 ? (
              <div className="text-center text-violet-300 py-8">Chưa có đơn hàng nào</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-violet-300 text-sm">
                      <th className="py-3 px-4 font-medium">Mã đơn</th>
                      <th className="py-3 px-4 font-medium">Khách hàng</th>
                      <th className="py-3 px-4 font-medium">Người tạo</th>
                      <th className="py-3 px-4 font-medium text-right">Tổng tiền</th>
                      <th className="py-3 px-4 font-medium">Ngày tạo</th>
                      <th className="py-3 px-4 font-medium"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {orders.map((order) => (
                      <tr key={order.id} className="text-white hover:bg-white/5 transition-colors">
                        <td className="py-3 px-4 font-mono text-xs">#{order.id}</td>
                        <td className="py-3 px-4">
                          <p className="font-medium text-sm">{order.customer_name}</p>
                          <Badge variant="outline" className="text-[10px] py-0 border-white/20 text-violet-300">
                            {order.payment_method === 'DEBT' ? 'Ghi nợ' : 'Tiền mặt'}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-sm text-violet-300">{order.created_by}</td>
                        <td className="py-3 px-4 text-right font-bold text-emerald-400">
                          {formatCurrency(order.total_amount)}
                        </td>
                        <td className="py-3 px-4 text-xs text-violet-300">
                          {new Date(order.created_at).toLocaleString('vi-VN')}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <Button
                            variant="ghost"
                            size="icon"
                            className="text-violet-300 hover:text-white"
                            onClick={async () => {
                              const { ordersAPI } = await import("@/lib/api");
                              const printRes = await ordersAPI.getPrint(order.id);
                              if (printRes.success) {
                                const printWindow = window.open('', '_blank');
                                if (printWindow) {
                                  printWindow.document.write(printRes.html);
                                  printWindow.document.close();
                                  printWindow.print();
                                }
                              }
                            }}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>



        {/* Customers with Debt - Only for Owner */}
        {
          isOwner && (
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
          )
        }
      </main >
    </div >
  );
}
