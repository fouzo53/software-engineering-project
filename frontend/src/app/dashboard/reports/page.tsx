"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { reportsAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { formatCurrency } from "@/lib/utils";
import { BookOpen, Calendar, Printer, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function ReportsPage() {
    const { isOwner } = useAuth();
    const [loading, setLoading] = useState(false);
    const [startDate, setStartDate] = useState(
        new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0]
    );
    const [endDate, setEndDate] = useState(
        new Date().toISOString().split('T')[0]
    );

    const [revenueLedger, setRevenueLedger] = useState<any>(null);
    const [cashBook, setCashBook] = useState<any>(null);

    const loadReports = async () => {
        setLoading(true);
        try {
            const [revenueRes, cashRes] = await Promise.all([
                reportsAPI.getRevenueLedger(startDate, endDate),
                reportsAPI.getCashBook(startDate, endDate)
            ]);
            setRevenueLedger(revenueRes);
            setCashBook(cashRes);
        } catch (error) {
            console.error("Error loading reports:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isOwner) {
            loadReports();
        }
    }, [isOwner, startDate, endDate]);

    if (!isOwner) {
        return <div className="p-8 text-center text-white">Bạn không có quyền xem báo cáo này.</div>;
    }

    const printReport = () => {
        window.print();
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <Link href="/dashboard">
                        <Button variant="ghost" className="text-white hover:bg-white/10 mb-2 pl-0">
                            <ArrowLeft className="w-4 h-4 mr-2" />
                            Quay lại Dashboard
                        </Button>
                    </Link>
                    <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                        <BookOpen className="w-8 h-8 text-yellow-400" />
                        Sổ sách Kế toán (Thông tư 88)
                    </h1>
                    <p className="text-slate-400 text-sm">
                        Chuẩn hóa theo quy định của Bộ Tài Chính cho hộ kinh doanh
                    </p>
                </div>

                <div className="flex items-center gap-2 bg-white/5 p-2 rounded-lg border border-white/10">
                    <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-slate-400" />
                        <Input
                            type="date"
                            className="bg-transparent border-0 text-white w-32 p-0 focus-visible:ring-0"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                        />
                        <span className="text-slate-400">-</span>
                        <Input
                            type="date"
                            className="bg-transparent border-0 text-white w-32 p-0 focus-visible:ring-0"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                        />
                    </div>
                </div>
            </div>

            <Tabs defaultValue="s1" className="w-full">
                <TabsList className="bg-white/5 border border-white/10 w-full justify-start">
                    <TabsTrigger value="s1" className="data-[state=active]:bg-yellow-500 data-[state=active]:text-black">
                        Mẫu S1-HKD: Doanh thu
                    </TabsTrigger>
                    <TabsTrigger value="s4" className="data-[state=active]:bg-emerald-500 data-[state=active]:text-white">
                        Mẫu S4-HKD: Quỹ tiền mặt
                    </TabsTrigger>
                </TabsList>

                {/* --- S1-HKD: Sổ chi tiết doanh thu --- */}
                <TabsContent value="s1">
                    <Card className="bg-white border-none shadow-lg text-black overflow-hidden relative">
                        <div className="absolute top-4 right-4 print:hidden">
                            <Button variant="outline" size="sm" onClick={printReport} className="flex gap-2">
                                <Printer className="w-4 h-4" /> In sổ
                            </Button>
                        </div>
                        <CardHeader className="text-center border-b border-gray-200 bg-yellow-50 pb-6 print:pb-2">
                            <p className="text-sm font-bold text-right absolute top-4 right-4 hidden print:block">Mẫu số S1-HKD</p>

                            <h2 className="text-xl font-bold uppercase text-gray-900">Sổ chi tiết doanh thu bán hàng hóa, dịch vụ</h2>
                            <p className="text-sm text-gray-600">
                                (Ban hành kèm theo Thông tư số 88/2021/TT-BTC ngày 11/10/2021 của Bộ Tài chính)
                            </p>
                            <p className="text-sm italic mt-2">
                                Từ ngày {new Date(startDate).toLocaleDateString('vi-VN')} đến ngày {new Date(endDate).toLocaleDateString('vi-VN')}
                            </p>
                        </CardHeader>
                        <CardContent className="p-0 overflow-x-auto">
                            <table className="w-full border-collapse text-sm">
                                <thead>
                                    <tr className="bg-gray-100 text-gray-700">
                                        <th rowSpan={2} className="border border-gray-300 p-2 w-10">Ngày CT</th>
                                        <th rowSpan={2} className="border border-gray-300 p-2 w-20">Số CT</th>
                                        <th colSpan={2} className="border border-gray-300 p-2">Thông tin khách hàng</th>
                                        <th colSpan={3} className="border border-gray-300 p-2">Doanh thu bán hàng hóa, dịch vụ</th>
                                        <th rowSpan={2} className="border border-gray-300 p-2">Giảm giá/Trả lại</th>
                                    </tr>
                                    <tr className="bg-gray-50 text-gray-600 text-xs">
                                        <th className="border border-gray-300 p-2">Họ tên</th>
                                        <th className="border border-gray-300 p-2">Địa chỉ</th>
                                        <th className="border border-gray-300 p-2">Tổng doanh thu</th>
                                        <th className="border border-gray-300 p-2">Hàng hóa</th>
                                        <th className="border border-gray-300 p-2">Dịch vụ</th>
                                    </tr>
                                    {/* Column Numbers */}
                                    <tr className="text-center text-gray-400 italic text-[10px]">
                                        <td className="border border-gray-300">A</td>
                                        <td className="border border-gray-300">B</td>
                                        <td className="border border-gray-300">C</td>
                                        <td className="border border-gray-300">D</td>
                                        <td className="border border-gray-300">1</td>
                                        <td className="border border-gray-300">2</td>
                                        <td className="border border-gray-300">3</td>
                                        <td className="border border-gray-300">4</td>
                                    </tr>
                                </thead>
                                <tbody>
                                    {loading ? (
                                        <tr><td colSpan={8} className="p-8 text-center text-gray-500">Đang tải dữ liệu...</td></tr>
                                    ) : revenueLedger?.rows?.map((row: any, i: number) => (
                                        <tr key={i} className="hover:bg-yellow-50/50">
                                            <td className="border border-gray-300 p-2 text-center">{row.date}</td>
                                            <td className="border border-gray-300 p-2 text-center">{row.voucher_no}</td>
                                            <td className="border border-gray-300 p-2">{row.customer_name}</td>
                                            <td className="border border-gray-300 p-2 text-xs truncate max-w-[150px]">{row.customer_address}</td>
                                            <td className="border border-gray-300 p-2 text-right font-medium">
                                                {formatCurrency(row.total_revenue)}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right">{formatCurrency(row.product_revenue)}</td>
                                            <td className="border border-gray-300 p-2 text-right">{formatCurrency(row.service_revenue)}</td>
                                            <td className="border border-gray-300 p-2 text-right">0</td>
                                        </tr>
                                    ))}

                                    {/* Total Row */}
                                    {!loading && (
                                        <tr className="bg-yellow-100 font-bold">
                                            <td colSpan={4} className="border border-gray-300 p-2 text-center uppercase">Tổng cộng phát sinh</td>
                                            <td className="border border-gray-300 p-2 text-right text-red-600">
                                                {formatCurrency(revenueLedger?.total_revenue || 0)}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right">
                                                {formatCurrency(revenueLedger?.total_revenue || 0)}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right">0</td>
                                            <td className="border border-gray-300 p-2 text-right">0</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* --- S4-HKD: Sổ quỹ tiền mặt --- */}
                <TabsContent value="s4">
                    <Card className="bg-white border-none shadow-lg text-black overflow-hidden relative">
                        <div className="absolute top-4 right-4 print:hidden">
                            <Button variant="outline" size="sm" onClick={printReport} className="flex gap-2">
                                <Printer className="w-4 h-4" /> In sổ
                            </Button>
                        </div>
                        <CardHeader className="text-center border-b border-gray-200 bg-emerald-50 pb-6 print:pb-2">
                            <p className="text-sm font-bold text-right absolute top-4 right-4 hidden print:block">Mẫu số S4-HKD</p>

                            <h2 className="text-xl font-bold uppercase text-gray-900">Sổ quỹ tiền mặt</h2>
                            <p className="text-sm text-gray-600">
                                (Ban hành kèm theo Thông tư số 88/2021/TT-BTC ngày 11/10/2021 của Bộ Tài chính)
                            </p>
                        </CardHeader>
                        <CardContent className="p-0 overflow-x-auto">
                            <table className="w-full border-collapse text-sm">
                                <thead>
                                    <tr className="bg-gray-100 text-gray-700">
                                        <th rowSpan={2} className="border border-gray-300 p-2 w-24">Ngày tháng ghi sổ</th>
                                        <th rowSpan={2} className="border border-gray-300 p-2 w-24">Ngày tháng CT</th>
                                        <th rowSpan={2} className="border border-gray-300 p-2">Số phiếu CT</th>
                                        <th rowSpan={2} className="border border-gray-300 p-2">Diễn giải</th>
                                        <th colSpan={3} className="border border-gray-300 p-2">Số tiền</th>
                                        <th rowSpan={2} className="border border-gray-300 p-2">Ghi chú</th>
                                    </tr>
                                    <tr className="bg-gray-50 text-gray-600 text-xs">
                                        <th className="border border-gray-300 p-2 text-emerald-700">Thu</th>
                                        <th className="border border-gray-300 p-2 text-red-700">Chi</th>
                                        <th className="border border-gray-300 p-2">Tồn quỹ</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr className="bg-gray-50 font-bold italic">
                                        <td colSpan={4} className="border border-gray-300 p-2 text-center">Số dư đầu kỳ</td>
                                        <td className="border border-gray-300 p-2"></td>
                                        <td className="border border-gray-300 p-2"></td>
                                        <td className="border border-gray-300 p-2 text-right text-emerald-600">
                                            {formatCurrency(cashBook?.opening_balance || 0)}
                                        </td>
                                        <td className="border border-gray-300 p-2"></td>
                                    </tr>

                                    {loading ? (
                                        <tr><td colSpan={8} className="p-8 text-center text-gray-500">Đang tải dữ liệu...</td></tr>
                                    ) : cashBook?.rows?.map((row: any, i: number) => (
                                        <tr key={i} className="hover:bg-emerald-50/50">
                                            <td className="border border-gray-300 p-2 text-center">{row.date}</td>
                                            <td className="border border-gray-300 p-2 text-center">{row.date}</td>
                                            <td className="border border-gray-300 p-2 text-center font-mono text-xs">{row.voucher_no}</td>
                                            <td className="border border-gray-300 p-2">{row.description}</td>
                                            <td className="border border-gray-300 p-2 text-right font-medium">
                                                {row.receipt_amount > 0 ? formatCurrency(row.receipt_amount) : '-'}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right">
                                                {row.payment_amount > 0 ? formatCurrency(row.payment_amount) : '-'}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right font-bold text-gray-800">
                                                {formatCurrency(row.balance)}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right"></td>
                                        </tr>
                                    ))}

                                    {!loading && (
                                        <tr className="bg-gray-100 font-bold">
                                            <td colSpan={4} className="border border-gray-300 p-2 text-center uppercase">Cộng số phát sinh</td>
                                            <td className="border border-gray-300 p-2 text-right text-emerald-600">
                                                {formatCurrency(cashBook?.total_receipt || 0)}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right text-red-600">
                                                {formatCurrency(cashBook?.total_payment || 0)}
                                            </td>
                                            <td className="border border-gray-300 p-2 text-right bg-gray-200">

                                            </td>
                                            <td className="border border-gray-300 p-2 text-right"></td>
                                        </tr>
                                    )}

                                    <tr className="bg-emerald-100 font-bold text-lg border-t-2 border-emerald-500">
                                        <td colSpan={4} className="border border-gray-300 p-2 text-center uppercase">Số dư cuối kỳ</td>
                                        <td className="border border-gray-300 p-2"></td>
                                        <td className="border border-gray-300 p-2"></td>
                                        <td className="border border-gray-300 p-2 text-right text-emerald-800">
                                            {formatCurrency(cashBook?.closing_balance || 0)}
                                        </td>
                                        <td className="border border-gray-300 p-2"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>

            <style jsx global>{`
                @media print {
                    @page { size: landscape; margin: 10mm; }
                    body { background: white; color: black; }
                    .print\\:hidden { display: none !important; }
                    .print\\:block { display: block !important; }
                    .print\\:pb-2 { padding-bottom: 0.5rem !important; }
                    /* Hide Sidebar and Header */
                    nav, header, aside { display: none !important; }
                }
            `}</style>
        </div>
    );
}
