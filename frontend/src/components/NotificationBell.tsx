"use client";

import { useEffect, useState } from "react";
import { Bell, Check } from "lucide-react";
import { notificationsAPI } from "@/lib/api";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

interface Notification {
    id: number;
    title: string;
    message: string;
    is_read: boolean;
    created_at: string;
    type: string;
}

export function NotificationBell() {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [unreadCount, setUnreadCount] = useState(0);

    const loadNotifications = async () => {
        try {
            const data = await notificationsAPI.getAll();
            setNotifications(data);
            setUnreadCount(data.filter((n: Notification) => !n.is_read).length);
        } catch (error) {
            console.error("Failed to load notifications", error);
        }
    };

    useEffect(() => {
        loadNotifications();
        // Polling every 30 seconds as a simple real-time fallback
        const interval = setInterval(loadNotifications, 30000);
        return () => clearInterval(interval);
    }, []);

    const markAsRead = async (id: number) => {
        try {
            await notificationsAPI.markRead(id);
            setNotifications(prev =>
                prev.map(n => n.id === id ? { ...n, is_read: true } : n)
            );
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch (error) {
            console.error("Failed to mark as read", error);
        }
    };

    const markAllRead = async () => {
        try {
            await notificationsAPI.markAllRead();
            setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
            setUnreadCount(0);
            toast.success("Đã đánh dấu đọc tất cả");
        } catch (error) {
            console.error("Failed to mark all as read", error);
        }
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="relative text-white hover:bg-white/10">
                    <Bell className="w-5 h-5" />
                    {unreadCount > 0 && (
                        <Badge className="absolute -top-1 -right-1 h-5 w-5 p-0 flex items-center justify-center bg-red-500 border-none text-[10px]">
                            {unreadCount}
                        </Badge>
                    )}
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80 bg-slate-900 border-white/10 text-white p-0 overflow-hidden">
                <div className="p-4 border-b border-white/10 flex items-center justify-between">
                    <h3 className="font-bold">Thông báo</h3>
                    {unreadCount > 0 && (
                        <Button variant="ghost" size="sm" onClick={markAllRead} className="text-xs text-blue-400 hover:text-blue-300 h-auto p-0">
                            Đánh dấu đã đọc hết
                        </Button>
                    )}
                </div>
                <div className="max-h-[400px] overflow-y-auto">
                    {notifications.length === 0 ? (
                        <div className="p-8 text-center text-slate-400 text-sm">
                            Chưa có thông báo nào
                        </div>
                    ) : (
                        notifications.map((n) => (
                            <DropdownMenuItem
                                key={n.id}
                                className={`flex flex-col items-start p-4 border-b border-white/5 last:border-0 cursor-pointer focus:bg-white/5 ${!n.is_read ? 'bg-blue-500/5' : ''}`}
                                onClick={() => markAsRead(n.id)}
                            >
                                <div className="flex items-center justify-between w-full mb-1">
                                    <span className={`text-sm font-bold ${!n.is_read ? 'text-blue-400' : 'text-slate-300'}`}>
                                        {n.title}
                                    </span>
                                    <span className="text-[10px] text-slate-500">
                                        {new Date(n.created_at).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                </div>
                                <p className="text-xs text-slate-400 line-clamp-2">
                                    {n.message}
                                </p>
                            </DropdownMenuItem>
                        ))
                    )}
                </div>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
