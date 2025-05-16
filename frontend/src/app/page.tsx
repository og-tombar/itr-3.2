"use client";

import { useEffect } from "react";
import socket from "../socket";

export default function Home() {
  useEffect(() => {
    socket.on("connect", () => {
      console.log("[frontend] connected, id =", socket.id);
      socket.emit("ping_event", { time: Date.now() });
    });

    socket.on("pong_event", (data) => {
      console.log("[frontend] received pong:", data);
    });

    return () => {
      socket.off("connect");
      socket.off("pong_event");
    };
  }, []);

  return (
    <main style={{ fontFamily: "sans-serif", padding: 20 }}>
      <h1>Socket.IO Ping-Pong Test</h1>
      <p>Check your browser console for “ping” → “pong” logs.</p>
    </main>
  );
}
