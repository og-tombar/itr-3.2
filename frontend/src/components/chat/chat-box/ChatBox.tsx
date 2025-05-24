"use client";

import { useChatBox } from "./useChatBox";
import styles from "./ChatBox.module.css";

export default function ChatBox() {
  const {
    message,
    setMessage,
    messages,
    formatTime,
    handleSendMessage,
    messagesEndRef,
  } = useChatBox();

  return (
    <div className={styles.chatBox} role="dialog" aria-labelledby="chat-title">
      <header className={styles.chatHeader}>
        <h3 id="chat-title" className={styles.chatTitle}>
          Game Chat
        </h3>
      </header>

      <div
        className={styles.chatMessages}
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
      >
        {messages.map((msg) => (
          <div key={msg.id} className={styles.chatMessage} role="listitem">
            <div className={styles.messageHeader}>
              <span className={styles.messageUsername}>{msg.username}</span>
              <time
                className={styles.messageTime}
                dateTime={msg.timestamp.toISOString()}
              >
                {formatTime(msg.timestamp)}
              </time>
            </div>
            <div className={styles.messageContent}>{msg.message}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form className={styles.chatInputForm} onSubmit={handleSendMessage}>
        <label htmlFor="chat-input" className={styles.srOnly}>
          Type your message
        </label>
        <input
          id="chat-input"
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
          className={styles.chatInput}
          maxLength={200}
          autoComplete="off"
        />
        <button
          type="submit"
          className={styles.chatSendBtn}
          disabled={!message.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
}
