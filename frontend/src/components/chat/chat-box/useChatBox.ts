"use client";

import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import socket from "@/shared/socket";
import { ClientEvent, ServerEvent } from "@/shared/events";
import { Message } from "./types";

export const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};

export default function useChatBox() {
  const msgBoxRef = useRef<HTMLDivElement>(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      console.log("Sending message:", message);
      socket.emit(ClientEvent.MESSAGE, {
        id: Date.now().toString(),
        sender_id: socket.id,
        username: "You",
        message: message.trim(),
        timestamp: new Date().toISOString(),
      });
      setMessage("");
    }
  };

  const handleReceiveMessage = useCallback((message: Message) => {
    console.log("Received message:", message);
    setMessages((prevMessages) => [...prevMessages, message]);
  }, []);

  useEffect(() => {
    socket.on(ServerEvent.MESSAGE, handleReceiveMessage);
    return () => {
      socket.off(ServerEvent.MESSAGE, handleReceiveMessage);
    };
  }, [handleReceiveMessage]);

  const scrollToBottom = useCallback(() => {
    msgBoxRef.current?.scrollTo({
      top: msgBoxRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, []);

  useLayoutEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  return {
    message,
    setMessage,
    messages,
    handleSendMessage,
    msgBoxRef,
  };
}
