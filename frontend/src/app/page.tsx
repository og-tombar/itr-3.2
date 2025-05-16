import Lobby from "../components/Lobby/LobbyView";

export default function Page() {
  return (
    <main style={{ fontFamily: "sans-serif", padding: 20 }}>
      <h1>Matchmaking Lobby</h1>
      <Lobby />
    </main>
  );
}
