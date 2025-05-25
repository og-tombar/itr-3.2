"use client";

import styles from "./Chat.module.css";
import ChatToggle from "../chat-toggle/ChatToggle";
import { useChatToggle } from "../chat-toggle/useChatToggle";
import ChatBox from "../chat-box";

export default function Chat() {
  const { isOpen, onToggleChat } = useChatToggle();

  return (
    <aside className={styles.chatContainer} aria-label="Game chat">
      <ChatToggle isOpen={isOpen} toggleChat={onToggleChat} />
      <div hidden={!isOpen}>
        <ChatBox />
      </div>
    </aside>
  );
}
