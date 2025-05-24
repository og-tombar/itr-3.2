"use client";

import styles from "./ChatToggle.module.css";

interface ChatToggleProps {
  isOpen: boolean;
  toggleChat: () => void;
}

export default function ChatToggle({ isOpen, toggleChat }: ChatToggleProps) {
  return (
    <button
      className={styles.chatToggleBtn}
      onClick={toggleChat}
      aria-label={isOpen ? "Close chat" : "Open chat"}
      aria-expanded={isOpen}
    >
      {isOpen ? "✕" : "💬"}
    </button>
  );
}
