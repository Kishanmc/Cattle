import { downloadPdf } from "../utils/pdf";

export default function PredictionCard({ prediction, mode, setMode, status }) {
  return (
    <div className="card">
      <div>
        <button onClick={() => setMode("breed")}>Breed</button>
        <button onClick={() => setMode("disease")}>Disease</button>
      </div>

      {prediction && (
        <>
          <h2>{prediction.predicted_class}</h2>
          <p>Confidence: {(prediction.confidence * 100).toFixed(2)}%</p>
          <button onClick={() => downloadPdf(prediction)}>Download PDF</button>
        </>
      )}

      <div className="status">{status}</div>
    </div>
  );
}
