import { useEffect, useRef, useState } from "react";
import { ChatMessage } from "./types";

const greetingMessage = {
  id: "1",
  username: "System",
  message: "Welcome to the game chat!",
  timestamp: new Date(),
};

const formatTime = (timestamp: Date) => {
  return timestamp.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};

export function useChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([greetingMessage]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        username: "You", // TODO: Replace with actual username
        message: message.trim(),
        timestamp: new Date(),
      };
      setMessages([...messages, newMessage]);
      setMessage("");
    }
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return {
    messages,
    setMessages,
    scrollToBottom,
    messagesEndRef,
    isOpen,
    toggleChat,
    handleSendMessage,
    message,
    setMessage,
    formatTime,
  };
}
