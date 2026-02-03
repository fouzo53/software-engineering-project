const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:6868/api";

async function fetcher(endpoint: string, options: RequestInit = {}) {
    const token = typeof window !== "undefined" ? localStorage.getItem("bizflow_token") : null;

    const headers = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        cache: "no-store",
        ...options,
        headers,
    });

    const data = await response.json();

    if (!response.ok) {
        const errMsg = data.message || data.error || "Something went wrong";
        throw new Error(errMsg);
    }

    return data;
}

export const authAPI = {
    login: (data: any) => fetcher("/auth/login", { method: "POST", body: JSON.stringify(data) }),
    register: (data: any) => fetcher("/auth/register", { method: "POST", body: JSON.stringify(data) }),
};

export const productsAPI = {
    getAll: () => fetcher("/products"),
    create: (data: any) => fetcher("/products", { method: "POST", body: JSON.stringify(data) }),
};

export const customersAPI = {
    getAll: () => fetcher("/customers"),
    create: (data: any) => fetcher("/customers", { method: "POST", body: JSON.stringify(data) }),
    makePayment: (customerId: number, amount: number) =>
        fetcher(`/customers/${customerId}/payment`, {
            method: "POST",
            body: JSON.stringify({ amount }),
        }),

};

export const categoriesAPI = {
    getAll: () => fetcher("/categories"),
};

export const ordersAPI = {
    getAll: (page = 1, perPage = 10) => fetcher(`/orders?page=${page}&per_page=${perPage}`),
    create: (data: any) => fetcher("/orders", { method: "POST", body: JSON.stringify(data) }),
    getPrint: (orderId: number) => fetcher(`/orders/${orderId}/print`),
};

export const aiAPI = {
    parseOrder: (text: string) =>
        fetcher("/ai/parse-order", {
            method: "POST",
            body: JSON.stringify({ text }),
        }),
    parseVoiceOrder: (audioBlob: Blob) => {
        const formData = new FormData();
        formData.append("audio", audioBlob, "voice_order.webm");

        // We can't use the 'fetcher' helper directly because of FormData and Authorization
        const token = typeof window !== "undefined" ? localStorage.getItem("bizflow_token") : null;
        return fetch(`${API_URL}/ai/parse-voice-order`, {
            method: "POST",
            headers: {
                ...(token && { Authorization: `Bearer ${token}` }),
            },
            body: formData,
        }).then(async (res) => {
            const data = await res.json();
            if (!res.ok) throw new Error(data.message || data.error || "Failed to parse voice");
            return data;
        });
    },
    confirmDraft: (draftId: number) =>
        fetcher(`/ai/confirm-draft/${draftId}`, {
            method: "POST",
        }),
};

export const reportsAPI = {
    getDailyRevenue: (startDate: string, endDate: string) =>
        fetcher(`/reports/revenue?start_date=${startDate}&end_date=${endDate}`),

    getTax: (startDate: string, endDate: string) =>
        fetcher(`/reports/tax?start_date=${startDate}&end_date=${endDate}`),

    getRevenueLedger: (startDate: string, endDate: string) =>
        fetcher(`/reports/ledger/revenue?start_date=${startDate}&end_date=${endDate}`),

    getCashBook: (startDate: string, endDate: string) =>
        fetcher(`/reports/ledger/cash?start_date=${startDate}&end_date=${endDate}`),
};

export const notificationsAPI = {
    getAll: (unreadOnly = false) => fetcher(`/notifications?unread_only=${unreadOnly}`),
    markRead: (id: number) => fetcher(`/notifications/${id}/read`, { method: "PUT" }),
    markAllRead: () => fetcher("/notifications/read-all", { method: "PUT" }),
};

export const subscriptionAPI = {
    getPlans: () => fetcher("/subscription/plans"),
    getCurrent: () => fetcher("/subscription/current"),
    upgrade: (plan: string) => fetcher("/subscription/upgrade", {
        method: "POST",
        body: JSON.stringify({ plan }),
    }),
};
