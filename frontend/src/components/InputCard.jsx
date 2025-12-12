import { useRef } from "react";

export default function InputCard({ predict, startCamera, stopCamera }) {
  const fileRef = useRef(null);
  const videoRef = useRef(null);

  function upload() {
    const file = fileRef.current.files[0];
    if (!file) return alert("Select image");
    predict(file);
  }

  function capture() {
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext("2d").drawImage(videoRef.current, 0, 0);
    canvas.toBlob(b => predict(new File([b], "cam.jpg", { type: "image/jpeg" })));
  }

  return (
    <div className="card">
      <input ref={fileRef} type="file" accept="image/*" />
      <button onClick={upload}>Predict Image</button>

      <video ref={videoRef} autoPlay />
      <button onClick={() => startCamera(videoRef)}>Start Camera</button>
      <button onClick={capture}>Capture</button>
      <button onClick={() => stopCamera(videoRef)}>Stop</button>
    </div>
  );
}
