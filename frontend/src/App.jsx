import { useState } from "react";
import UploadForm from "./components/UploadForm.jsx";
import ResultsPanel from "./components/ResultsPanel.jsx";

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="app-shell">
      <div className="brand-row">
        <div className="brand">
          <span className="dot" />
          HireLens-AI
        </div>
      </div>
      <p className="tagline">
        Embedding-based resume ↔ job description matching, with an interpretable skill-gap breakdown.
      </p>

      <p className="eyebrow">Step 1 — Upload &amp; Compare</p>
      <UploadForm
        onResult={(r) => {
          setResult(r);
          setError(null);
        }}
        onError={setError}
        loading={loading}
        setLoading={setLoading}
      />

      {error && <div className="error-banner" style={{ marginTop: 20 }}>{error}</div>}

      {result && (
        <>
          <p className="eyebrow" style={{ marginTop: 32 }}>
            Step 2 — Results
          </p>
          <ResultsPanel result={result} />
        </>
      )}
    </div>
  );
}
