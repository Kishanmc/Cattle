import { useRef, useState } from "react";
import jsPDF from "jspdf";
import "./App.css";

const BREED_API_URL = "http://localhost:8000/predict_breed";
const DISEASE_API_URL = "http://localhost:8000/predict_disease";

export default function App() {
  const fileInputRef = useRef(null);
  const previewImgRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [previewMode, setPreviewMode] = useState("empty");
  const [currentMode, setCurrentMode] = useState("breed");
  const [cameraStream, setCameraStream] = useState(null);
  const [status, setStatus] = useState("");
  const [lastPrediction, setLastPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [resultHTML, setResultHTML] = useState("");
  const [extraHTML, setExtraHTML] = useState("");

  const apiUrl = currentMode === "breed" ? BREED_API_URL : DISEASE_API_URL;

  const handleFileSelect = () => {
    const file = fileInputRef.current.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = e => {
      previewImgRef.current.src = e.target.result;
      setPreviewMode("image");
    };
    reader.readAsDataURL(file);
  };

  const predictFromFile = async file => {
    if (!file) return;
    setStatus(`🔄 Running ${currentMode} prediction...`);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(apiUrl, { method: "POST", body: formData });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Prediction failed");

      renderPrediction(data);
    } catch (err) {
      setStatus("❌ Prediction failed");
    }
  };

  const renderPrediction = data => {
    const conf = (data.confidence * 100).toFixed(2);
    const s = data.static_data || {};

    let historyEntry = `${data.predicted_class} (${conf}%)`;
    setHistory(h => [historyEntry, ...h]);

    if (currentMode === "breed") {
      setResultHTML(`
        <div class="breed-name">${s.breed || data.predicted_class}</div>
        <div class="pred-meta">Confidence: <span class="confidence">${conf}%</span></div>
      `);

      setExtraHTML(`
        <div class="description">
          <div class="description-para-title">Origin</div>
          <div>${s.origin || "N/A"}</div>

          <div class="description-para-title">Milk Yield</div>
          <div>${s.average_milk_yield || "N/A"}</div>
        </div>
      `);
    } else {
      setResultHTML(`
        <div class="breed-name">${s.name || data.predicted_class}</div>
        <div class="pred-meta">Confidence: <span class="confidence">${conf}%</span></div>
      `);

      setExtraHTML(`
        <div class="description">
          <div class="description-para-title">Symptoms</div>
          <div>${(s.symptoms || []).join("<br>")}</div>
        </div>
      `);
    }

    setLastPrediction({
      ...data,
      confidence: conf,
      imageData: previewImgRef.current.src,
      mode: currentMode
    });

    setStatus(`File: ${data.filename}`);
  };

  const startCamera = async () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(t => t.stop());
      setCameraStream(null);
      setPreviewMode("empty");
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    setCameraStream(stream);
    setPreviewMode("camera");
  };

  const captureFromCamera = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    const imgData = canvas.toDataURL("image/jpeg");
    previewImgRef.current.src = imgData;
    setPreviewMode("image");

    canvas.toBlob(blob => {
      predictFromFile(new File([blob], "camera.jpg", { type: "image/jpeg" }));
    });
  };

  const downloadPdfReport = () => {
    if (!lastPrediction) return;

    const pdf = new jsPDF();
    pdf.text("CATTLE ANALYSIS REPORT", 105, 15, { align: "center" });
    pdf.text(`Confidence: ${lastPrediction.confidence}%`, 15, 30);
    pdf.addImage(lastPrediction.imageData, "JPEG", 15, 40, 80, 60);
    pdf.save("cattle_report.pdf");
  };

  return (
    <div className="app-shell">
      <header className="header">
        <h1 className="app-title">Cattle Vision</h1>
        <p className="app-subtitle">AI-powered cattle breed & disease classifier</p>
      </header>

      <div className="layout">
        {/* LEFT CARD */}
        <div className="card">
          <div className="section-label">Input</div>

          <input
            type="file"
            ref={fileInputRef}
            accept="image/*"
            onChange={handleFileSelect}
          />

          <div className="btn-row">
            <button className="btn" onClick={() => predictFromFile(fileInputRef.current.files[0])}>
              ⚡ Predict
            </button>

            <button className="btn secondary" onClick={startCamera}>
              📷 Camera
            </button>

            <button className="btn" onClick={captureFromCamera}>
              🎯 Capture
            </button>
          </div>

          <div className="preview-shell">
            {previewMode === "image" && <img ref={previewImgRef} />}
            {previewMode === "camera" && <video ref={videoRef} autoPlay />}
            {previewMode === "empty" && <div className="preview-placeholder">No image</div>}
          </div>
        </div>

        {/* RESULT CARD */}
        <div className="card">
          <div dangerouslySetInnerHTML={{ __html: resultHTML }} />
          <div dangerouslySetInnerHTML={{ __html: extraHTML }} />

          <div className="status-line">{status}</div>

          <button className="btn secondary" onClick={downloadPdfReport}>
            📄 Download PDF
          </button>

          <div className="history">
            {history.map((h, i) => (
              <div key={i} className="history-item">{h}</div>
            ))}
          </div>
        </div>
      </div>

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
}
