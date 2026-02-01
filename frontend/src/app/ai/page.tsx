"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { ArrowLeft, Send, Bot, User } from "lucide-react";
import Link from "next/link";

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function AIAssistantPage() {
  const router = useRouter();
  const { isAuthenticated, isOwner } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: "assistant",
      content:
        "Xin chào! Tôi là trợ lý AI của BizFlow. Tôi có thể giúp bạn:\n\n• Phân tích đơn hàng từ tin nhắn\n• Tra cứu thông tin sản phẩm\n• Tìm kiếm khách hàng\n• Hỗ trợ nghiệp vụ bán hàng\n\nBạn cần hỗ trợ gì?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    // Simulate AI response (in production, call real AI API)
    setTimeout(() => {
      const aiResponse: Message = {
        id: messages.length + 2,
        role: "assistant",
        content: getAIResponse(input),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiResponse]);
      setLoading(false);
    }, 1000);
  };

  const getAIResponse = (query: string): string => {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes("xi măng") || lowerQuery.includes("ximang")) {
      return "📦 **Xi măng Hà Tiên**\n\n• Giá bán: 95,000 VND/bao\n• Tồn kho: 250 bao\n• Đơn vị: Bao 50kg\n\nBạn muốn tạo đơn hàng với sản phẩm này không?";
    }

    if (lowerQuery.includes("đơn hàng") || lowerQuery.includes("order")) {
      return '📝 Để tạo đơn hàng nhanh, bạn có thể nói:\n\n• "Anh Ba mua 10 bao xi măng"\n• "Chị Tư lấy 5 thùng sơn ghi nợ"\n\nTôi sẽ tự động phân tích và tạo đơn hàng cho bạn.';
    }

    if (lowerQuery.includes("khách") || lowerQuery.includes("nợ")) {
      return "👥 **Danh sách khách hàng có nợ:**\n\n• Trần Thị Bích: 500,000 VND\n• Lê Hoàng Linh: 1,200,000 VND\n• Vũ Thị Hương: 750,000 VND\n\nBạn muốn thu nợ khách hàng nào?";
    }

    if (lowerQuery.includes("báo cáo") || lowerQuery.includes("doanh thu")) {
      return "📊 **Báo cáo hôm nay:**\n\n• Doanh thu: 5,250,000 VND\n• Số đơn hàng: 12\n• Sản phẩm bán chạy: Xi măng Hà Tiên\n\nBạn muốn xem chi tiết không?";
    }

    return (
      'Tôi hiểu bạn đang hỏi về: "' +
      query +
      '"\n\nTôi có thể giúp bạn với:\n• Tra cứu sản phẩm và giá\n• Tạo đơn hàng nhanh\n• Quản lý công nợ khách hàng\n• Xem báo cáo doanh thu\n\nHãy cho tôi biết cụ thể hơn nhé!'
    );
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-white/5 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
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
            <div className="w-10 h-10 bg-gradient-to-r from-pink-500 to-rose-500 rounded-lg flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Trợ lý AI</h1>
              <p className="text-xs text-violet-300">
                Hỗ trợ bán hàng thông minh
              </p>
            </div>
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

      <main className="container mx-auto px-4 py-6 max-w-3xl">
        <Card className="backdrop-blur-xl bg-white/10 border-white/20 h-[calc(100vh-180px)] flex flex-col">
          {/* Messages */}
          <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.role === "user" ? "flex-row-reverse" : ""}`}
              >
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    message.role === "user"
                      ? "bg-violet-500"
                      : "bg-gradient-to-r from-pink-500 to-rose-500"
                  }`}
                >
                  {message.role === "user" ? (
                    <User className="w-4 h-4 text-white" />
                  ) : (
                    <Bot className="w-4 h-4 text-white" />
                  )}
                </div>
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    message.role === "user"
                      ? "bg-violet-500/20 border border-violet-500/30"
                      : "bg-white/10 border border-white/10"
                  }`}
                >
                  <p className="text-white whitespace-pre-wrap">
                    {message.content}
                  </p>
                  <p className="text-xs text-violet-400 mt-1">
                    {message.timestamp.toLocaleTimeString("vi-VN")}
                  </p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-pink-500 to-rose-500 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div className="bg-white/10 border border-white/10 p-3 rounded-lg">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
          </CardContent>

          {/* Input */}
          <div className="p-4 border-t border-white/10">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Nhập tin nhắn..."
                className="bg-white/10 border-white/20 text-white placeholder:text-violet-300"
                disabled={loading}
              />
              <Button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>
      </main>
    </div>
  );
}
