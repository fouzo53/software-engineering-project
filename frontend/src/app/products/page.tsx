"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { productsAPI } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { Package, Plus, Search, ArrowLeft, Edit, Trash2 } from "lucide-react";
import Link from "next/link";
import Image from "next/image";
import { toast } from "sonner";

interface Product {
  id: number;
  name: string;
  price: number;
  selling_price: number;
  cost_price: number;
  stock: number;
  unit: string;
  category_id: number;
  image_url?: string;
}

interface Category {
  id: number;
  name: string;
}

export default function ProductsPage() {
  const router = useRouter();
  const { isAuthenticated, isOwner, user } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    cost_price: "",
    stock: "",
    category_id: "",
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    loadProducts();
  }, [isAuthenticated, router]);

  const loadProducts = async () => {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        productsAPI.getAll(),
        fetch("/api/categories").then((r) => r.json()),
      ]);
      setProducts(productsRes.data || []);
      setCategories(categoriesRes.data || categoriesRes.value || []);
    } catch (error) {
      console.error("Error loading products:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProduct.category_id) {
      toast.error("Vui lòng chọn danh mục!");
      return;
    }
    try {
      await productsAPI.create({
        name: newProduct.name,
        price: Number(newProduct.price),
        cost_price: Number(newProduct.cost_price),
        stock: Number(newProduct.stock),
        category_id: Number(newProduct.category_id),
      });
      toast.success("Thêm sản phẩm thành công!");
      setShowAddForm(false);
      setNewProduct({
        name: "",
        price: "",
        cost_price: "",
        stock: "",
        category_id: "",
      });
      loadProducts();
    } catch (error: any) {
      toast.error(error.message || "Không thể thêm sản phẩm");
    }
  };

  const filteredProducts = products.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

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
            <h1 className="text-xl font-bold text-white">Quản lý sản phẩm</h1>
            <Badge className={isOwner ? "bg-red-500" : "bg-blue-500"}>
              {isOwner ? "Admin" : "Nhân viên"}
            </Badge>
          </div>
          {isOwner && (
            <Button
              onClick={() => setShowAddForm(true)}
              className="bg-gradient-to-r from-emerald-500 to-teal-500"
            >
              <Plus className="w-4 h-4 mr-2" />
              Thêm sản phẩm
            </Button>
          )}
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Search */}
        <div className="mb-6">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-violet-300" />
            <Input
              placeholder="Tìm kiếm sản phẩm..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-violet-300"
            />
          </div>
        </div>

        {/* Add Product Form */}
        {showAddForm && isOwner && (
          <Card className="backdrop-blur-xl bg-white/10 border-white/20 mb-6">
            <CardHeader>
              <CardTitle className="text-white">Thêm sản phẩm mới</CardTitle>
            </CardHeader>
            <CardContent>
              <form
                onSubmit={handleAddProduct}
                className="grid grid-cols-1 md:grid-cols-2 gap-4"
              >
                <Input
                  placeholder="Tên sản phẩm"
                  value={newProduct.name}
                  onChange={(e) =>
                    setNewProduct({ ...newProduct, name: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                  required
                />
                <Input
                  type="number"
                  placeholder="Giá bán"
                  value={newProduct.price}
                  onChange={(e) =>
                    setNewProduct({ ...newProduct, price: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                  required
                />
                <Input
                  type="number"
                  placeholder="Giá nhập"
                  value={newProduct.cost_price}
                  onChange={(e) =>
                    setNewProduct({ ...newProduct, cost_price: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                />
                <Input
                  type="number"
                  placeholder="Số lượng tồn"
                  value={newProduct.stock}
                  onChange={(e) =>
                    setNewProduct({ ...newProduct, stock: e.target.value })
                  }
                  className="bg-white/10 border-white/20 text-white"
                />
                <select
                  value={newProduct.category_id}
                  onChange={(e) =>
                    setNewProduct({
                      ...newProduct,
                      category_id: e.target.value,
                    })
                  }
                  className="w-full p-2 rounded-md bg-white/10 border border-white/20 text-white"
                  required
                >
                  <option value="" className="bg-slate-800">
                    -- Chọn danh mục --
                  </option>
                  {categories.map((cat) => (
                    <option
                      key={cat.id}
                      value={cat.id}
                      className="bg-slate-800"
                    >
                      {cat.name}
                    </option>
                  ))}
                </select>
                <div className="md:col-span-2 flex gap-2">
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

        {/* Products Grid */}
        <Card className="backdrop-blur-xl bg-white/10 border-white/20">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Package className="w-5 h-5" />
              Danh sách sản phẩm ({filteredProducts.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center text-violet-300 py-8">
                Đang tải...
              </div>
            ) : filteredProducts.length === 0 ? (
              <div className="text-center text-violet-300 py-8">
                {searchTerm
                  ? "Không tìm thấy sản phẩm"
                  : "Chưa có sản phẩm nào"}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-white/10">
                      <th className="text-left py-3 px-4 text-violet-300 font-medium">
                        Hình ảnh
                      </th>
                      <th className="text-left py-3 px-4 text-violet-300 font-medium">
                        Tên sản phẩm
                      </th>
                      <th className="text-right py-3 px-4 text-violet-300 font-medium">
                        Giá bán
                      </th>
                      <th className="text-right py-3 px-4 text-violet-300 font-medium">
                        Giá nhập
                      </th>
                      <th className="text-right py-3 px-4 text-violet-300 font-medium">
                        Tồn kho
                      </th>
                      <th className="text-right py-3 px-4 text-violet-300 font-medium">
                        Lợi nhuận
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredProducts.map((product) => (
                      <tr
                        key={product.id}
                        className="border-b border-white/5 hover:bg-white/5"
                      >
                        <td className="py-3 px-4">
                          <div className="relative h-12 w-12 rounded border overflow-hidden">
                            <Image
                              src={
                                product.image_url || "https://placehold.co/50"
                              }
                              alt={product.name}
                              fill
                              className="object-cover"
                            />
                          </div>
                        </td>
                        <td className="py-3 px-4 text-white">{product.name}</td>
                        <td className="py-3 px-4 text-right text-emerald-400 font-medium">
                          {formatCurrency(
                            product.price || product.selling_price,
                          )}
                        </td>
                        <td className="py-3 px-4 text-right text-violet-300">
                          {formatCurrency(product.cost_price || 0)}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <Badge
                            variant={
                              product.stock < 20 ? "destructive" : "default"
                            }
                          >
                            {product.stock} {product.unit || "cái"}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-right text-amber-400">
                          {formatCurrency(
                            (product.price || product.selling_price) -
                              (product.cost_price || 0),
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
