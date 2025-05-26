import { ClientEvent } from "@/shared/events";
import socket from "@/shared/socket";
import { useState } from "react";

export default function useBotLevelButtons() {
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null);

  const handleLevelClick = (level: string) => {
    console.log("[useBotLevelButtons] level clicked", level);
    setSelectedLevel(level);
    socket.emit(ClientEvent.SET_BOT_LEVEL, { level });
  };

  return { selectedLevel, handleLevelClick };
}
