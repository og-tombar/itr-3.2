import { LargeButtonProps } from "./types";

export default function LargeButton(props: LargeButtonProps) {
  return (
    <button className="btn btn-primary btn-large" onClick={props.onClick}>
      {props.label}
    </button>
  );
}
