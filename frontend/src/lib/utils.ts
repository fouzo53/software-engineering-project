export function formatCurrency(amount: number): string {
    return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
    }).format(amount);
}

export function cn(...inputs: any[]) {
    return inputs.filter(Boolean).join(" ");
}

export function formatPhone(phone: string): string {
    if (!phone) return "";
    if (phone.startsWith("0")) {
        return "+84" + phone.substring(1);
    }
    return phone;
}
