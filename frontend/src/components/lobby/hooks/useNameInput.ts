import { ClientEvent } from "@/shared/events";
import socket from "@/shared/socket";
import { useState } from "react";

export default function useNameInput() {
  const [nameInput, setNameInput] = useState("");

  const onChangeName = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNameInput(e.target.value);
  };

  const onSubmitName = () => {
    socket.emit(ClientEvent.NEW_PLAYER, { name: nameInput });
  };

  return { nameInput, onChangeName, onSubmitName };
}
