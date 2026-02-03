
"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { subscriptionAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Check, Shield, Zap, Star, ArrowLeft } from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { toast } from "sonner";

export default function SubscriptionPage() {
    const { isOwner } = useAuth();
    const [plans, setPlans] = useState<any>(null);
    const [currentPlan, setCurrentPlan] = useState<string>("basic");
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [plansRes, currentRes] = await Promise.all([
                subscriptionAPI.getPlans(),
                subscriptionAPI.getCurrent()
            ]);
            setPlans(plansRes);
            setCurrentPlan(currentRes.plan);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpgrade = async (planKey: string) => {
        if (confirm(`Bạn có chắc muốn nâng cấp lên gói ${plans[planKey].name}?`)) {
            setProcessing(true);
            try {
                await subscriptionAPI.upgrade(planKey);
                toast.success("Nâng cấp thành công!");
                setCurrentPlan(planKey);
                // Reload user context if needed, or just state
            } catch (error: any) {
                toast.error(error.message || "Lỗi nâng cấp");
            } finally {
                setProcessing(false);
            }
        }
    };

    if (!isOwner) return <div className="p-8 text-white">Chỉ chủ cửa hàng mới có quyền truy cập.</div>;

    if (loading || !plans) return <div className="p-8 text-white">Đang tải...</div>;

    const planKeys = ["free", "basic", "pro"]; // Order

    return (
        <div className="min-h-screen bg-slate-900 p-8">
            <Link href="/dashboard">
                <Button variant="ghost" className="text-white hover:bg-white/10 mb-6 pl-0">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Quay lại Dashboard
                </Button>
            </Link>

            <div className="max-w-5xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-3xl font-bold text-white mb-4">Gói dịch vụ BizFlow</h1>
                    <p className="text-slate-400">Chọn gói phù hợp với quy mô cửa hàng của bạn</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {planKeys.map((key) => {
                        const plan = plans[key];
                        const isCurrent = currentPlan === key;
                        const isBasic = key === "basic";
                        const isEnterprise = key === "enterprise";

                        return (
                            <Card
                                key={key}
                                className={`relative border-2 ${isCurrent ? "border-emerald-500 bg-white/5" : "border-white/10 bg-white/5"} ${isEnterprise ? "bg-gradient-to-b from-slate-900 to-indigo-950" : ""}`}
                            >
                                {isCurrent && (
                                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500 text-black font-bold px-3 py-1 rounded-full text-xs">
                                        Đang sử dụng
                                    </div>
                                )}
                                <CardHeader>
                                    <CardTitle className="text-white flex items-center justify-between">
                                        <span>{plan.name}</span>
                                        {key === "pro" && <Zap className="w-5 h-5 text-yellow-400" />}
                                        {key === "enterprise" && <Shield className="w-5 h-5 text-purple-400" />}
                                    </CardTitle>
                                    <div className="mt-4">
                                        <span className="text-3xl font-bold text-white">
                                            {plan.price === 0 ? "Miễn phí" : formatCurrency(plan.price)}
                                        </span>
                                        {plan.price > 0 && <span className="text-slate-400 text-sm">/tháng</span>}
                                    </div>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="space-y-2">
                                        {Object.entries(plan.limits).map(([limitKey, val]: [string, any]) => (
                                            <div key={limitKey} className="flex justify-between text-sm text-slate-300">
                                                <span className="capitalize">{limitKey.replace(/_/g, " ")}:</span>
                                                <span className="font-bold text-white">{val > 1000 ? "Không giới hạn" : val}</span>
                                            </div>
                                        ))}
                                    </div>
                                    <div className="border-t border-white/10 pt-4 space-y-2">
                                        {plan.features.map((feature: string, i: number) => (
                                            <div key={i} className="flex items-center gap-2 text-sm text-slate-300">
                                                <Check className="w-4 h-4 text-emerald-500" />
                                                {feature}
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                                <CardFooter>
                                    <Button
                                        onClick={() => handleUpgrade(key)}
                                        disabled={isCurrent || processing}
                                        className={`w-full ${isCurrent ? "bg-white/10 text-slate-400" : "bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600"}`}
                                    >
                                        {isCurrent ? "Đang sử dụng" : "Nâng cấp ngay"}
                                    </Button>
                                </CardFooter>
                            </Card>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
