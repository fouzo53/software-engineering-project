"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/utils";
import { Check, X, AlertTriangle, User, Package, CreditCard } from "lucide-react";
import { aiAPI } from "@/lib/api";
import { toast } from "sonner";

interface Props {
    data: any;
    onCancel: () => void;
    onConfirm: () => void;
}

export function DraftOrderReview({ data, onCancel, onConfirm }: Props) {
    const [isConfirming, setIsConfirming] = useState(false);

    // Adapter for different API response formats
    const draft_id = data.draft_id;
    const transcript = data.transcript;
    const confidence = data.confidence || 0.99; // Default high confidence if not provided
    const issues = data.issues || [];
    const warnings = data.warnings || [];

    // Construct draft_order object from flat data if needed
    const draft_order = data.draft_order || {
        customer: data.customer,
        items: data.items || [],
        payment: { type: data.payment_method?.toLowerCase() || 'cash' },
        total_amount: data.total_amount || 0
    };

    const handleConfirm = async () => {
        setIsConfirming(true);
        try {
            await aiAPI.confirmDraft(draft_id);
            toast.success("Đã xác nhận đơn hàng thành công!");
            onConfirm();
        } catch (error: any) {
            toast.error(error.message || "Lỗi khi xác nhận đơn hàng");
        } finally {
            setIsConfirming(false);
        }
    };

    return (
        <div className="space-y-6">
            {/* Transcript Info */}
            <div className="bg-white/5 p-3 rounded-lg border border-white/10">
                <p className="text-xs text-slate-400 uppercase font-bold mb-1">Câu lệnh bóc tách:</p>
                <p className="italic text-slate-200">"{transcript?.original_text}"</p>
            </div>

            {/* Confidence Score */}
            <div className="flex items-center justify-between px-1">
                <div className="flex items-center gap-2">
                    <p className="text-sm text-slate-400">Độ tin cậy:</p>
                    <Badge className={confidence > 0.8 ? "bg-emerald-500" : confidence > 0.5 ? "bg-amber-500" : "bg-red-500"}>
                        {Math.round(confidence * 100)}%
                    </Badge>
                </div>
                {data.status === "needs_review" && (
                    <div className="flex items-center gap-1 text-amber-400 text-xs">
                        <AlertTriangle className="w-3 h-3" />
                        Cần kiểm tra lại
                    </div>
                )}
            </div>

            {/* Issues & Warnings */}
            {(issues?.length > 0 || warnings?.length > 0) && (
                <div className="space-y-2">
                    {issues.map((issue: string, i: number) => (
                        <div key={i} className="flex items-start gap-2 text-red-400 text-sm bg-red-500/10 p-2 rounded">
                            <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                            {issue}
                        </div>
                    ))}
                    {warnings.map((warning: string, i: number) => (
                        <div key={i} className="flex items-start gap-2 text-amber-400 text-sm bg-amber-500/10 p-2 rounded">
                            <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                            {warning}
                        </div>
                    ))}
                </div>
            )}

            {/* Order Details */}
            <div className="space-y-4">
                {/* Customer */}
                <div className="flex items-center gap-3 p-3 bg-white/5 rounded-lg border border-white/10">
                    <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center">
                        <User className="w-5 h-5 text-blue-400" />
                    </div>
                    <div className="flex-1">
                        <p className="text-xs text-slate-400 font-medium">Khách hàng</p>
                        <p className="text-white font-bold">
                            {draft_order.customer?.name || "Khách vãng lai"}
                        </p>
                    </div>
                    {draft_order.customer?.match_type === "none" && (
                        <Badge variant="outline" className="text-amber-400 border-amber-400/50">Mới</Badge>
                    )}
                </div>

                {/* Items */}
                <div className="space-y-2">
                    <p className="text-xs text-slate-400 font-bold uppercase px-1">Sản phẩm</p>
                    {draft_order.items.map((item: any, i: number) => (
                        <div key={i} className="flex items-center gap-3 p-3 bg-white/5 rounded-lg border border-white/10">
                            <div className="w-10 h-10 rounded bg-emerald-500/20 flex items-center justify-center">
                                <Package className="w-5 h-5 text-emerald-400" />
                            </div>
                            <div className="flex-1">
                                <p className="text-white font-medium">{item.product.name}</p>
                                <p className="text-xs text-slate-400">
                                    {item.quantity} {item.unit}
                                </p>
                            </div>
                            {item.product.match_type === "none" && (
                                <Badge variant="destructive" className="text-[10px]">Lỗi khớp</Badge>
                            )}
                        </div>
                    ))}
                </div>

                {/* Total & Payment */}
                <div className="flex items-center justify-between p-4 bg-slate-800 rounded-lg border border-white/10">
                    <div className="flex items-center gap-2">
                        <CreditCard className="w-5 h-5 text-slate-400" />
                        <span className="text-slate-300 capitalize">{draft_order.payment.type === 'debt' ? 'Ghi nợ' : 'Tiền mặt'}</span>
                    </div>
                    <div className="text-right">
                        <p className="text-xs text-slate-400">Tổng tiền dừa tính</p>
                        <p className="text-xl font-bold text-emerald-400">{formatCurrency(draft_order.total_amount)}</p>
                    </div>
                </div>
            </div>

            <div className="flex gap-3 pt-2">
                <Button
                    variant="outline"
                    className="flex-1 border-white/10 text-white hover:bg-white/5"
                    onClick={onCancel}
                >
                    <X className="w-4 h-4 mr-2" />
                    Hủy bỏ
                </Button>
                <Button
                    className="flex-1 bg-emerald-500 hover:bg-emerald-600"
                    onClick={handleConfirm}
                    disabled={isConfirming}
                >
                    {isConfirming ? (
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                        <Check className="w-4 h-4 mr-2" />
                    )}
                    Xác nhận
                </Button>
            </div>
        </div>
    );
}

// Add a tiny fix for missing Loader2 import in AiOrderDialog logic
import { Loader2 } from "lucide-react";
