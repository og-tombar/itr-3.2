"use client";

import React from "react";
import { useChat } from "./useChat";
import "./Chat.css";

export default function Chat() {
  const {
    messages,
    messagesEndRef,
    isOpen,
    toggleChat,
    message,
    setMessage,
    handleSendMessage,
    formatTime,
  } = useChat();

  return (
    <aside
      className={`chat-container ${isOpen ? "chat-open" : "chat-closed"}`}
      aria-label="Game chat"
    >
      {/* Chat Toggle Button */}
      <button
        className="chat-toggle-btn"
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
        aria-expanded={isOpen}
      >
        {isOpen ? "✕" : "💬"}
      </button>

      {/* Chat Box */}
      {isOpen && (
        <div className="chat-box" role="dialog" aria-labelledby="chat-title">
          <header className="chat-header">
            <h3 id="chat-title" className="chat-title">
              Game Chat
            </h3>
          </header>

          <div
            className="chat-messages"
            role="log"
            aria-live="polite"
            aria-label="Chat messages"
          >
            {messages.map((msg) => (
              <div key={msg.id} className="chat-message" role="listitem">
                <div className="message-header">
                  <span className="message-username">{msg.username}</span>
                  <time
                    className="message-time"
                    dateTime={msg.timestamp.toISOString()}
                  >
                    {formatTime(msg.timestamp)}
                  </time>
                </div>
                <div className="message-content">{msg.message}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-input-form" onSubmit={handleSendMessage}>
            <label htmlFor="chat-input" className="sr-only">
              Type your message
            </label>
            <input
              id="chat-input"
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a message..."
              className="chat-input"
              maxLength={200}
              autoComplete="off"
            />
            <button
              type="submit"
              className="chat-send-btn"
              disabled={!message.trim()}
            >
              Send
            </button>
          </form>
        </div>
      )}
    </aside>
  );
}
