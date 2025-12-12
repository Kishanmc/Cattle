import React from "react";

export default function Preview({ src, mode }) {
  if (!src) return <div className="preview-placeholder">No image selected.</div>;
  return <img src={src} alt="preview" id="preview" style={{ maxWidth: "100%", maxHeight: 360 }} />;
}
