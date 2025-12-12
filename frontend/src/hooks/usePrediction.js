import { useState, useRef } from "react";

const BREED_API = "http://localhost:8000/predict_breed";
const DISEASE_API = "http://localhost:8000/predict_disease";

export function usePrediction() {
  const [mode, setMode] = useState("breed");
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [status, setStatus] = useState("");
  const [history, setHistory] = useState([]);

  const cameraStream = useRef(null);

  const api = mode === "breed" ? BREED_API : DISEASE_API;

  async function predict(file) {
    setLoading(true);
    setStatus("Running prediction...");

    const fd = new FormData();
    fd.append("file", file);

    try {
      const res = await fetch(api, { method: "POST", body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail);

      setPrediction(data);
      setHistory(h => [{ time: new Date(), mode, data }, ...h]);
      setStatus(`File: ${data.filename}`);
    } catch (e) {
      setPrediction(null);
      setStatus(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function startCamera(videoRef) {
    cameraStream.current = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" }
    });
    videoRef.current.srcObject = cameraStream.current;
  }

  function stopCamera(videoRef) {
    cameraStream.current?.getTracks().forEach(t => t.stop());
    cameraStream.current = null;
    videoRef.current.srcObject = null;
  }

  return {
    mode,
    setMode,
    loading,
    prediction,
    status,
    history,
    predict,
    startCamera,
    stopCamera
  };
}
