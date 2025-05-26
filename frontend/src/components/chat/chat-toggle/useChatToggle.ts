"use client";

import { useState } from "react";

export function useChatToggle() {
  const [isOpen, setIsOpen] = useState(true);

  const onToggleChat = () => {
    setIsOpen(!isOpen);
  };

  return { isOpen, onToggleChat };
}
