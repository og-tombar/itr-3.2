import { ClientEvent } from "@/shared/events";
import socket from "@/shared/socket";
import { useState } from "react";

export default function useCategoryButtons() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const handleCategoryClick = (category: string) => {
    console.log("[useCategoryButtons] category clicked", category);
    setSelectedCategory(category);
    socket.emit(ClientEvent.SELECT_CATEGORY, { category });
  };

  return { selectedCategory, handleCategoryClick };
}
