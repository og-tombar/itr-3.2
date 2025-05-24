"use client";

import { useState } from "react";

export function useChatToggle() {
  const [isOpen, setIsOpen] = useState(false);

  const onToggleChat = () => {
    setIsOpen(!isOpen);
  };

  return { isOpen, onToggleChat };
}
