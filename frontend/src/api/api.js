// src/api/api.js
const getHostPort = () => {
  // If app served from same host, use that host + port; otherwise fallback to localhost:8000
  const host = window.location.hostname || "localhost";
  const port = window.location.port || "8000";
  return { host, port };
};

const { host, port } = getHostPort();
const BASE = `http://${host}:${port}`;

export async function predictFile(file, mode = "breed") {
  const url = mode === "breed" ? `${BASE}/predict_breed` : `${BASE}/predict_disease`;
  const fd = new FormData();
  fd.append("file", file, file.name || "upload.jpg");

  const res = await fetch(url, { method: "POST", body: fd });
  const data = await res.json().catch(() => ({ detail: "Invalid JSON response" }));
  if (!res.ok) {
    const err = data && data.detail ? data.detail : res.statusText;
    throw new Error(err);
  }
  return data;
}

export async function predictCrossbreed(fileA, fileB) {
  const url = `${BASE}/predict_crossbreed`;
  const fd = new FormData();
  fd.append("parent_a", fileA, fileA.name || "a.jpg");
  fd.append("parent_b", fileB, fileB.name || "b.jpg");

  const res = await fetch(url, { method: "POST", body: fd });
  const data = await res.json();
  if (!res.ok) {
    const err = data && data.detail ? data.detail : res.statusText;
    throw new Error(err);
  }
  return data;
}
