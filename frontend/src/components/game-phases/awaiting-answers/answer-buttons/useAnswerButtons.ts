import { ClientEvent } from "@/shared/events";
import socket from "@/shared/socket";
import { useState } from "react";

const buttonColors = [
  "var(--accent-red)",
  "var(--accent-teal)",
  "var(--accent-yellow)",
  "var(--accent-green)",
];

export default function useAnswerButtons() {
  const [answer, setAnswer] = useState<number>(-1);

  const handleAnswerClick = (optionIndex: number) => {
    console.log("[useAnswerButtons] answer clicked", optionIndex);
    setAnswer(optionIndex);
    socket.emit(ClientEvent.SUBMIT_ANSWER, { answer: optionIndex });
  };

  const didAnswer = () => answer !== -1;

  return { buttonColors, answer, handleAnswerClick, didAnswer };
}
