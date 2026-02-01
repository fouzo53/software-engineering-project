"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { productsAPI, customersAPI, ordersAPI } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import {
  ShoppingCart,
  Plus,
  Minus,
  Trash2,
  ArrowLeft,
  CreditCard,
} from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

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

interface CartItem {
  product_id: number;
  name: string;
  price: number;
  quantity: number;
  unit: string;
}

export default function POSPage() {
  const router = useRouter();
  const { isAuthenticated, isOwner } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState<number | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<"CASH" | "DEBT">("CASH");
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

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

  const addToCart = (product: Product) => {
    const existingItem = cart.find((item) => item.product_id === product.id);

    if (existingItem) {
      if (existingItem.quantity >= product.stock) {
        toast.error("Không đủ hàng trong kho");
        return;
      }
      setCart(
        cart.map((item) =>
          item.product_id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item,
        ),
      );
    } else {
      setCart([
        ...cart,
        {
          product_id: product.id,
          name: product.name,
          price: product.selling_price,
          quantity: 1,
          unit: product.unit,
        },
      ]);
    }
    toast.success(`Đã thêm ${product.name}`);
  };

  const updateQuantity = (productId: number, delta: number) => {
    const product = products.find((p) => p.id === productId);
    setCart(
      cart
        .map((item) => {
          if (item.product_id === productId) {
            const newQty = item.quantity + delta;
            if (newQty <= 0) return item;
            if (product && newQty > product.stock) {
              toast.error("Không đủ hàng trong kho");
              return item;
            }
            return { ...item, quantity: newQty };
          }
          return item;
        })
        .filter((item) => item.quantity > 0),
    );
  };

  const removeFromCart = (productId: number) => {
    setCart(cart.filter((item) => item.product_id !== productId));
  };

  const totalAmount = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  const handleCheckout = async () => {
    if (cart.length === 0) {
      toast.error("Giỏ hàng trống");
      return;
    }

    if (!selectedCustomer) {
      toast.error("Vui lòng chọn khách hàng");
      return;
    }

    setProcessing(true);
    try {
      await ordersAPI.create({
        customer_id: selectedCustomer,
        items: cart.map((item) => ({
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.price,
        })),
        payment_method: paymentMethod,
        total_amount: totalAmount,
      });

      toast.success("Tạo đơn hàng thành công!");
      setCart([]);
      setSelectedCustomer(null);
      loadData();
    } catch (error: any) {
      toast.error(error.message || "Không thể tạo đơn hàng");
    } finally {
      setProcessing(false);
    }
  };

  if (!isAuthenticated) {
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
            <h1 className="text-xl font-bold text-white">Bán hàng</h1>
            <Badge
              className={
                isOwner
                  ? "bg-red-500 hover:bg-red-600"
                  : "bg-blue-500 hover:bg-blue-600"
              }
            >
              {isOwner ? "Admin" : "Nhân viên"}
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Products Grid */}
          <div className="lg:col-span-2">
            <Card className="backdrop-blur-xl bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle className="text-white">Danh sách sản phẩm</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center text-violet-300 py-8">
                    Đang tải...
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[600px] overflow-y-auto">
                    {products.map((product) => (
                      <div
                        key={product.id}
                        onClick={() => addToCart(product)}
                        className="p-4 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 cursor-pointer transition-all"
                      >
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-medium text-white">
                            {product.name}
                          </h3>
                          <Badge
                            variant={
                              product.stock < 20 ? "destructive" : "default"
                            }
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
          </div>

          {/* Cart */}
          <div className="lg:col-span-1">
            <Card className="backdrop-blur-xl bg-white/10 border-white/20 sticky top-24">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <ShoppingCart className="w-5 h-5" />
                  Giỏ hàng ({cart.length})
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Customer Select */}
                <div>
                  <label className="text-sm text-violet-300 mb-2 block">
                    Khách hàng
                  </label>
                  <select
                    value={selectedCustomer || ""}
                    onChange={(e) =>
                      setSelectedCustomer(Number(e.target.value) || null)
                    }
                    className="w-full p-2 rounded-lg bg-white/10 border border-white/20 text-white"
                  >
                    <option value="">Chọn khách hàng</option>
                    {customers.map((c) => (
                      <option key={c.id} value={c.id} className="text-black">
                        {c.name} - {c.phone}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Cart Items */}
                <div className="space-y-3 max-h-[300px] overflow-y-auto">
                  {cart.length === 0 ? (
                    <p className="text-center text-violet-300 py-4">
                      Giỏ hàng trống
                    </p>
                  ) : (
                    cart.map((item) => (
                      <div
                        key={item.product_id}
                        className="p-3 rounded-lg bg-white/5 border border-white/10"
                      >
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="text-white text-sm font-medium">
                            {item.name}
                          </h4>
                          <button
                            onClick={() => removeFromCart(item.product_id)}
                            className="text-red-400 hover:text-red-300"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                        <div className="flex justify-between items-center">
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() =>
                                updateQuantity(item.product_id, -1)
                              }
                              className="w-7 h-7 rounded bg-white/10 flex items-center justify-center text-white hover:bg-white/20"
                            >
                              <Minus className="w-3 h-3" />
                            </button>
                            <span className="text-white w-8 text-center">
                              {item.quantity}
                            </span>
                            <button
                              onClick={() => updateQuantity(item.product_id, 1)}
                              className="w-7 h-7 rounded bg-white/10 flex items-center justify-center text-white hover:bg-white/20"
                            >
                              <Plus className="w-3 h-3" />
                            </button>
                          </div>
                          <p className="text-emerald-400 font-medium">
                            {formatCurrency(item.price * item.quantity)}
                          </p>
                        </div>
                      </div>
                    ))
                  )}
                </div>

                {/* Payment Method */}
                <div className="flex gap-2">
                  <button
                    onClick={() => setPaymentMethod("CASH")}
                    className={`flex-1 py-2 rounded-lg border transition-all ${
                      paymentMethod === "CASH"
                        ? "bg-emerald-500/20 border-emerald-500 text-emerald-400"
                        : "bg-white/5 border-white/20 text-white"
                    }`}
                  >
                    Tiền mặt
                  </button>
                  <button
                    onClick={() => setPaymentMethod("DEBT")}
                    className={`flex-1 py-2 rounded-lg border transition-all ${
                      paymentMethod === "DEBT"
                        ? "bg-amber-500/20 border-amber-500 text-amber-400"
                        : "bg-white/5 border-white/20 text-white"
                    }`}
                  >
                    Ghi nợ
                  </button>
                </div>

                {/* Total & Checkout */}
                <div className="pt-4 border-t border-white/10">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-lg text-white">Tổng cộng:</span>
                    <span className="text-2xl font-bold text-emerald-400">
                      {formatCurrency(totalAmount)}
                    </span>
                  </div>
                  <Button
                    onClick={handleCheckout}
                    disabled={
                      cart.length === 0 || !selectedCustomer || processing
                    }
                    className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600"
                  >
                    <CreditCard className="w-4 h-4 mr-2" />
                    {processing ? "Đang xử lý..." : "Thanh toán"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
