"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { customersAPI } from "@/lib/api";
import { formatCurrency, formatPhone } from "@/lib/utils";
import { Users, Plus, Search, ArrowLeft, CreditCard } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

interface Customer {
  id: number;
  name: string;
  phone: string;
  address: string;
  debt_amount: number;
}

export default function CustomersPage() {
  const router = useRouter();
  const { isAuthenticated, isOwner } = useAuth();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [showPaymentForm, setShowPaymentForm] = useState<number | null>(null);
  const [paymentAmount, setPaymentAmount] = useState("");
  const [newCustomer, setNewCustomer] = useState({
    name: "",
    phone: "",
    address: "",
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    loadCustomers();
  }, [isAuthenticated, router]);

  const loadCustomers = async () => {
    try {
      const res = await customersAPI.getAll();
      setCustomers(res.data || []);
    } catch (error) {
      console.error("Error loading customers:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCustomer = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await customersAPI.create(newCustomer);
      toast.success("Thêm khách hàng thành công!");
      setShowAddForm(false);
      setNewCustomer({ name: "", phone: "", address: "" });
      loadCustomers();
    } catch (error: any) {
      toast.error(error.message || "Không thể thêm khách hàng");
    }
  };

  const handlePayment = async (customerId: number) => {
    if (!paymentAmount || Number(paymentAmount) <= 0) {
      toast.error("Vui lòng nhập số tiền hợp lệ");
      return;
    }
    try {
      await customersAPI.makePayment(customerId, Number(paymentAmount));
      toast.success("Thu nợ thành công!");
      setShowPaymentForm(null);
      setPaymentAmount("");
      loadCustomers();
    } catch (error: any) {
      toast.error(error.message || "Không thể thu nợ");
    }
  };

  const filteredCustomers = customers.filter(
    (c) =>
      c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.phone.includes(searchTerm),
  );

  const totalDebt = customers.reduce((sum, c) => sum + (c.debt_amount || 0), 0);

  if (!isAuthenticated) return null;

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
            <h1 className="text-xl font-bold text-white">Quản lý khách hàng</h1>
          </div>
          <Button
            onClick={() => setShowAddForm(true)}
            className="bg-gradient-to-r from-emerald-500 to-teal-500"
          >
            <Plus className="w-4 h-4 mr-2" />
            Thêm khách hàng
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Card className="backdrop-blur-xl bg-white/10 border-white/20">
            <CardContent className="p-4 flex items-center gap-4">
              <Users className="w-10 h-10 text-violet-400" />
              <div>
                <p className="text-violet-300 text-sm">Tổng khách hàng</p>
                <p className="text-2xl font-bold text-white">
                  {customers.length}
                </p>
              </div>
            </CardContent>
          </Card>
          {isOwner && (
            <Card className="backdrop-blur-xl bg-white/10 border-white/20">
              <CardContent className="p-4 flex items-center gap-4">
                <CreditCard className="w-10 h-10 text-amber-400" />
                <div>
                  <p className="text-violet-300 text-sm">Tổng công nợ</p>
                  <p className="text-2xl font-bold text-amber-400">
                    {formatCurrency(totalDebt)}
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-violet-300" />
            <Input
              placeholder="Tìm kiếm khách hàng..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-violet-300"
            />
          </div>
        </div>

        {/* Add Customer Form */}
        {showAddForm && (
          <Card className="backdrop-blur-xl bg-white/10 border-white/20 mb-6">
            <CardHeader>
              <CardTitle className="text-white">Thêm khách hàng mới</CardTitle>
            </CardHeader>
            <CardContent>
              <form
                onSubmit={handleAddCustomer}
                className="grid grid-cols-1 md:grid-cols-3 gap-4"
              >
                <Input
                  placeholder="Tên khách hàng"
                  value={newCustomer.name}
                  onChange={(e) =>
                    setNewCustomer({ ...newCustomer, name: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                  required
                />
                <Input
                  placeholder="Số điện thoại"
                  value={newCustomer.phone}
                  onChange={(e) =>
                    setNewCustomer({ ...newCustomer, phone: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                  required
                />
                <Input
                  placeholder="Địa chỉ"
                  value={newCustomer.address}
                  onChange={(e) =>
                    setNewCustomer({ ...newCustomer, address: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                />
                <div className="md:col-span-3 flex gap-2">
                  <Button
                    type="submit"
                    className="bg-emerald-500 hover:bg-emerald-600"
                  >
                    Lưu
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowAddForm(false)}
                    className="border-white/20 text-white hover:bg-white/10"
                  >
                    Hủy
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Customers List */}
        <Card className="backdrop-blur-xl bg-white/10 border-white/20">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Users className="w-5 h-5" />
              Danh sách khách hàng ({filteredCustomers.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center text-violet-300 py-8">
                Đang tải...
              </div>
            ) : filteredCustomers.length === 0 ? (
              <div className="text-center text-violet-300 py-8">
                {searchTerm
                  ? "Không tìm thấy khách hàng"
                  : "Chưa có khách hàng nào"}
              </div>
            ) : (
              <div className="space-y-4">
                {filteredCustomers.map((customer) => (
                  <div
                    key={customer.id}
                    className="p-4 rounded-lg bg-white/5 border border-white/10"
                  >
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div>
                        <h3 className="font-medium text-white text-lg">
                          {customer.name}
                        </h3>
                        <p className="text-violet-300">{formatPhone(customer.phone)}</p>
                        <p className="text-violet-400 text-sm">
                          {customer.address}
                        </p>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <p className="text-sm text-violet-300">Công nợ</p>
                          <p
                            className={`text-xl font-bold ${customer.debt_amount > 0
                              ? "text-amber-400"
                              : "text-emerald-400"
                              }`}
                          >
                            {formatCurrency(customer.debt_amount || 0)}
                          </p>
                        </div>
                        {customer.debt_amount > 0 && (
                          <>
                            {showPaymentForm === customer.id ? (
                              <div className="flex gap-2">
                                <Input
                                  type="number"
                                  placeholder="Số tiền"
                                  value={paymentAmount}
                                  onChange={(e) =>
                                    setPaymentAmount(e.target.value)
                                  }
                                  className="w-32 bg-white/10 border-white/20 text-white"
                                />
                                <Button
                                  size="sm"
                                  onClick={() => handlePayment(customer.id)}
                                  className="bg-emerald-500"
                                >
                                  Xác nhận
                                </Button>
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => {
                                    setShowPaymentForm(null);
                                    setPaymentAmount("");
                                  }}
                                  className="border-white/20 text-white"
                                >
                                  Hủy
                                </Button>
                              </div>
                            ) : (
                              <Button
                                size="sm"
                                onClick={() => setShowPaymentForm(customer.id)}
                                className="bg-gradient-to-r from-amber-500 to-orange-500"
                              >
                                <CreditCard className="w-4 h-4 mr-2" />
                                Thu nợ
                              </Button>
                            )}
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
