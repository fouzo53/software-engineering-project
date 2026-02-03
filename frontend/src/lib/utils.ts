export function formatCurrency(amount: number): string {
    return new Intl.NumberFormat("vi-VN", {
        style: "currency",
        currency: "VND",
    }).format(amount);
}

export function cn(...inputs: any[]) {
    return inputs.filter(Boolean).join(" ");
}
