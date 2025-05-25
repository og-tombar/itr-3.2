import LargeButton from "../large-button/LargeButton";
import { LobbyFormProps } from "./types";

export default function LobbyForm(props: LobbyFormProps) {
  return (
    <>
      <input
        type="text"
        placeholder="Enter your name"
        value={props.input}
        onChange={props.onChange}
        className="lobby-input"
        maxLength={20}
      />
      <LargeButton label="Submit" onClick={props.onSubmit} />
    </>
  );
}
