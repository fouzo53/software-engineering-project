"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { authAPI } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    confirmPassword: "",
    full_name: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.username || !formData.password || !formData.full_name) {
      toast.error("Vui lòng điền đầy đủ thông tin");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error("Mật khẩu xác nhận không khớp");
      return;
    }

    if (formData.password.length < 6) {
      toast.error("Mật khẩu phải có ít nhất 6 ký tự");
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.register({
        username: formData.username,
        password: formData.password,
        full_name: formData.full_name,
        role: "employee",
      });
      toast.success("Đăng ký thành công!");
      router.push("/login");
    } catch (error: any) {
      toast.error(error.message || "Đăng ký thất bại");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-950 via-indigo-950 to-purple-950 relative overflow-hidden flex items-center justify-center p-4">
      {/* Aurora Background Effect */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-violet-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
      </div>

      {/* Glass Card */}
      <div className="relative z-10 w-full max-w-md">
        <div className="backdrop-blur-xl bg-white/10 rounded-2xl p-8 border border-white/20 shadow-2xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">BizFlow</h1>
            <p className="text-violet-200">Đăng ký tài khoản</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="full_name" className="text-white">
                Họ và tên
              </Label>
              <Input
                id="full_name"
                type="text"
                value={formData.full_name}
                onChange={(e) =>
                  setFormData({ ...formData, full_name: e.target.value })
                }
                className="bg-white/10 border-white/20 text-white placeholder:text-violet-300"
                placeholder="Nhập họ và tên"
                required
              />
            </div>

            <div>
              <Label htmlFor="username" className="text-white">
                Tên đăng nhập
              </Label>
              <Input
                id="username"
                type="text"
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                className="bg-white/10 border-white/20 text-white placeholder:text-violet-300"
                placeholder="Nhập tên đăng nhập"
                required
              />
            </div>

            <div>
              <Label htmlFor="password" className="text-white">
                Mật khẩu
              </Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                className="bg-white/10 border-white/20 text-white placeholder:text-violet-300"
                placeholder="Nhập mật khẩu"
                required
              />
            </div>

            <div>
              <Label htmlFor="confirmPassword" className="text-white">
                Xác nhận mật khẩu
              </Label>
              <Input
                id="confirmPassword"
                type="password"
                value={formData.confirmPassword}
                onChange={(e) =>
                  setFormData({ ...formData, confirmPassword: e.target.value })
                }
                className="bg-white/10 border-white/20 text-white placeholder:text-violet-300"
                placeholder="Nhập lại mật khẩu"
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-violet-500 to-indigo-500 hover:from-violet-600 hover:to-indigo-600 text-white"
              disabled={loading}
            >
              {loading ? "Đang xử lý..." : "Đăng ký"}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-violet-300">
              Đã có tài khoản?{" "}
              <Link
                href="/login"
                className="text-white hover:underline font-medium"
              >
                Đăng nhập
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
