"use client";

import { useRef, useState } from "react";
import { ChatMessage } from "../chat/types";

export const greetingMessage = {
  id: "1",
  username: "System",
  message: "Welcome to the game chat!",
  timestamp: new Date(),
};

export const formatTime = (timestamp: Date) => {
  return timestamp.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};

export function useChatBox() {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([greetingMessage]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      setMessages([
        ...messages,
        {
          id: Date.now().toString(),
          username: "You",
          message: message.trim(),
          timestamp: new Date(),
        },
      ]);
      setMessage("");
    }
  };

  return {
    message,
    setMessage,
    messages,
    formatTime,
    handleSendMessage,
    messagesEndRef,
  };
}
