export default function History({ history }) {
    return (
      <div className="history">
        <h3>Recent Predictions</h3>
        {history.map((h, i) => (
          <div key={i}>
            {h.time.toLocaleTimeString()} — {h.mode} — {h.data.predicted_class}
          </div>
        ))}
      </div>
    );
  }
  