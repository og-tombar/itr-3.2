import { ClientEvent } from "@/shared/events";
import socket from "@/shared/socket";

export default function usePowerupButtons() {
  const handlePowerupClick = (powerup: string) => {
    console.log("[usePowerupButtons] powerup clicked", powerup);
    socket.emit(ClientEvent.USE_POWERUP, { powerup });
  };

  return { handlePowerupClick };
}
