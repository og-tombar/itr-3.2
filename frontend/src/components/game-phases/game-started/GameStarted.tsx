export default function GameStartedScreen() {
  return (
    <div className="container-fullscreen">
      <div
        className="card card-large text-center"
        style={{ position: "relative", zIndex: 10 }}
      >
        <h1
          className="title-main animate-bounce"
          style={{
            color: "var(--accent-red)",
            textShadow:
              "3px 3px 0 var(--accent-teal), 6px 6px 0 var(--accent-yellow)",
            marginBottom: "var(--space-xl)",
          }}
        >
          Get Ready!
        </h1>
      </div>

      <div className="decorative-elements">
        <div className="bubble bubble-1"></div>
        <div className="bubble bubble-2"></div>
        <div className="bubble bubble-3"></div>
      </div>
    </div>
  );
}
