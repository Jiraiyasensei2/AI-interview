import { useRef, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function UploadForm({ onResult, onError, loading, setLoading }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const fileInputRef = useRef(null);

  const handleFilePick = (e) => {
    const file = e.target.files?.[0];
    if (file) setResumeFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) setResumeFile(file);
  };

  const handleSubmit = async () => {
    if (!resumeFile || !jobDescription.trim()) {
      onError("Upload a resume and paste a job description first.");
      return;
    }

    setLoading(true);
    onError(null);

    try {
      // Step 1: extract text from the uploaded resume
      const formData = new FormData();
      formData.append("file", resumeFile);

      const parseRes = await fetch(`${API_BASE}/parse-resume`, {
        method: "POST",
        body: formData,
      });
      if (!parseRes.ok) {
        const detail = await parseRes.json().catch(() => ({}));
        throw new Error(detail.detail || "Could not read the resume file.");
      }
      const { extracted_text } = await parseRes.json();

      // Step 2: run the embedding match + skill-gap analysis
      const matchRes = await fetch(`${API_BASE}/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          resume_text: extracted_text,
          job_description: jobDescription,
        }),
      });
      if (!matchRes.ok) {
        const detail = await matchRes.json().catch(() => ({}));
        throw new Error(detail.detail || "Matching failed.");
      }
      const result = await matchRes.json();
      onResult(result);
    } catch (err) {
      onError(err.message || "Something went wrong. Is the backend running on :8000?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="grid-two">
        <div>
          <label>Resume (.pdf or .txt)</label>
          <div
            className="dropzone"
            tabIndex={0}
            onClick={() => fileInputRef.current?.click()}
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.txt"
              onChange={handleFilePick}
              style={{ display: "none" }}
            />
            {resumeFile ? (
              <span className="filename">{resumeFile.name}</span>
            ) : (
              <>
                <span>Click or drop a file here</span>
                <span className="hint">PDF or plain text</span>
              </>
            )}
          </div>
        </div>

        <div>
          <label>Job description</label>
          <textarea
            placeholder="Paste the job description text here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>
      </div>

      <div className="actions">
        <button className="primary" onClick={handleSubmit} disabled={loading}>
          {loading ? "Analyzing..." : "Run Match"}
        </button>
      </div>
    </div>
  );
}
