"use client";

import { useState, useRef } from "react";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Mic, Square, Loader2, Bot, Send } from "lucide-react";
import { aiAPI } from "@/lib/api";
import { toast } from "sonner";
import { DraftOrderReview } from "./DraftOrderReview";

export function AiOrderDialog({ onSuccess }: { onSuccess?: () => void }) {
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [open, setOpen] = useState(false);
    const [liveTranscript, setLiveTranscript] = useState("");
    const [isReviewing, setIsReviewing] = useState(false);
    const recognitionRef = useRef<any>(null);

    const startRecording = async () => {
        setLiveTranscript("");
        setIsReviewing(false);
        try {
            // Setup Real-time Recognition (Browser API)
            const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.lang = 'vi-VN';
                recognition.continuous = true;
                recognition.interimResults = true;

                recognition.onresult = (event: any) => {
                    let transcript = "";
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        transcript += event.results[i][0].transcript;
                    }
                    setLiveTranscript(transcript);
                };

                recognition.onend = () => {
                    setIsRecording(false);
                };

                recognition.start();
                recognitionRef.current = recognition;
                setIsRecording(true);
            } else {
                toast.error("Trình duyệt không hỗ trợ Web Speech API");
            }
        } catch (err) {
            console.error("Error accessing microphone:", err);
            toast.error("Không thể truy cập micro!");
        }
    };

    const stopRecording = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
        // Sau khi dừng, chuyển sang chế độ review nếu có transcript
        setIsRecording(false);
        if (liveTranscript.trim()) {
            setIsReviewing(true);
        }
    };

    const handleVoiceSubmit = async (text: string) => {
        setIsProcessing(true);
        try {
            const data = await aiAPI.parseOrder(text);
            setResult(data);
        } catch (error: any) {
            toast.error(error.message || "Lỗi xử lý giọng nói");
        } finally {
            setIsProcessing(false);
        }
    };

    const reset = () => {
        setResult(null);
        setIsRecording(false);
        setIsProcessing(false);
        setLiveTranscript("");
        setIsReviewing(false);
    };

    return (
        <Dialog open={open} onOpenChange={(val) => {
            // Nếu người dùng đóng dialog trong khi còn đang ghi âm hoặc đang review,
            // thì hủy bỏ mọi phiên nhận diện âm thanh, xóa đoạn transcript và không gửi lệnh.
            if (!val) {
                if (recognitionRef.current) {
                    try {
                        // Ngắt các handler để tránh onend/onresult kích hoạt sau khi đóng
                        recognitionRef.current.onresult = null;
                        recognitionRef.current.onend = null;
                        if (typeof recognitionRef.current.abort === 'function') {
                            recognitionRef.current.abort();
                        } else if (typeof recognitionRef.current.stop === 'function') {
                            recognitionRef.current.stop();
                        }
                    } catch (e) {
                        console.warn('Failed to stop recognition:', e);
                    } finally {
                        recognitionRef.current = null;
                    }
                }

                // Xóa mọi trạng thái (bao gồm liveTranscript và chế độ review)
                reset();
                setOpen(false);
                return;
            }

            setOpen(val);
        }}>
            <DialogTrigger asChild>
                <Button className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600">
                    <Bot className="w-4 h-4 mr-2" />
                    Trợ lý AI
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px] bg-slate-900 border-white/10 text-white">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2 text-2xl">
                        <Bot className="w-6 h-6 text-pink-500" />
                        Trợ lý Bán hàng AI
                    </DialogTitle>
                </DialogHeader>

                <div className="py-6">
                    {!result ? (
                        <div className="flex flex-col items-center justify-center space-y-6">
                            <div className={`p-8 rounded-full transition-all duration-300 ${isRecording ? "bg-red-500/20 scale-110 animate-pulse" : "bg-white/5"
                                }`}>
                                {isRecording ? (
                                    <Square
                                        className="w-12 h-12 text-red-500 cursor-pointer"
                                        onClick={stopRecording}
                                    />
                                ) : (
                                    <Mic
                                        className="w-12 h-12 text-white cursor-pointer hover:text-pink-500 transition-colors"
                                        onClick={startRecording}
                                    />
                                )}
                            </div>

                            <div className="text-center w-full px-6">
                                <p className="text-lg font-medium mb-3">
                                    {isRecording
                                        ? "Đang lắng nghe..."
                                        : isReviewing
                                            ? "Kiểm tra lại câu lệnh trước khi gửi"
                                            : "Nhấn vào micro để nói"}
                                </p>

                                {(isRecording || isReviewing) && liveTranscript && (
                                    <div className="bg-white/5 border border-pink-500/20 p-4 rounded-xl mb-4 animate-in fade-in slide-in-from-bottom-2">
                                        <p className="text-pink-400 text-sm italic">
                                            "{liveTranscript}"
                                        </p>
                                    </div>
                                )}

                                {isReviewing && liveTranscript && (
                                    <div className="flex items-center justify-center gap-3 mt-2">
                                        <Button
                                            size="sm"
                                            className="bg-emerald-500 hover:bg-emerald-600"
                                            onClick={() => {
                                                handleVoiceSubmit(liveTranscript);
                                                setIsReviewing(false);
                                            }}
                                            disabled={isProcessing}
                                        >
                                            Gửi lệnh này
                                        </Button>
                                        <Button
                                            size="sm"
                                            variant="outline"
                                            className="border-white/20 text-slate-200"
                                            onClick={() => {
                                                setLiveTranscript("");
                                                setIsReviewing(false);
                                            }}
                                            disabled={isProcessing}
                                        >
                                            Ghi lại
                                        </Button>
                                    </div>
                                )}

                                <p className="text-sm text-slate-400 mt-2">
                                    Ví dụ: "Bán cho anh Nam 5 xi măng nợ nhé"
                                </p>
                            </div>

                            {isProcessing && (
                                <div className="flex items-center gap-3 text-pink-400 bg-pink-500/10 px-4 py-2 rounded-full">
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Đang phân tích lệnh...
                                </div>
                            )}
                        </div>
                    ) : (
                        <DraftOrderReview
                            data={result}
                            onCancel={reset}
                            onConfirm={() => {
                                setOpen(false);
                                reset();
                                if (onSuccess) onSuccess();
                            }}
                        />
                    )}
                </div>
            </DialogContent>
        </Dialog>
    );
}
