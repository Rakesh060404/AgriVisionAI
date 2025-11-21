import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Bot, User, Send, Copy, Check, Mic, MicOff } from "lucide-react";
import { API_ENDPOINTS } from "@/config/api";

interface Message {
  id: number;
  text: string;
  isBot: boolean;
  timestamp: Date;
}

export const Chatbot = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello! I'm your AgriVision AI assistant. How can I help you today?",
      isBot: true,
      timestamp: new Date()
    }
  ]);

  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const generateBotResponse = async (userMessage: string) => {
    try {
      const res = await fetch(API_ENDPOINTS.CHAT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      if (!res.ok) throw new Error(`HTTP error: ${res.status}`);

      const data = await res.json();
      return data.reply;  // IMPORTANT FIX
    } catch (err) {
      console.error("Chatbot error:", err);
      return "Sorry, I’m having trouble connecting right now.";
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMsg: Message = {
      id: messages.length + 1,
      text: inputText,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);
    const userText = inputText;
    setInputText("");
    setIsTyping(true);

    const botReply = await generateBotResponse(userText);

    const botMsg: Message = {
      id: messages.length + 2,
      text: botReply,
      isBot: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, botMsg]);
    setIsTyping(false);
  };

  return (
    <div className="space-y-6">
      <Card className="max-w-4xl mx-auto h-[600px] flex flex-col">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot /> AgriVision Chatbot
          </CardTitle>
        </CardHeader>

        <CardContent className="flex-1 flex flex-col p-0 overflow-hidden">
          <ScrollArea className="flex-1 p-6">
            {messages.map(msg => (
              <div key={msg.id} className={`flex mb-4 ${msg.isBot ? "justify-start" : "justify-end"}`}>
                <div className={`p-3 rounded-lg max-w-[70%] ${msg.isBot ? "bg-muted" : "bg-primary text-white"}`}>
                  {msg.text}
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex text-muted">AgriVision is typing...</div>
            )}
          </ScrollArea>

          <div className="p-4 border-t flex items-center gap-2">
            <Input
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              placeholder="Ask something about crops..."
            />
            <Button onClick={handleSendMessage}>
              <Send />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
