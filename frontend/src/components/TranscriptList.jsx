import { useState, useEffect } from "react";
import { getTranscripts } from "../services/api";

function TranscriptList() {
  const [transcripts, setTranscripts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTranscripts();
    const interval = setInterval(fetchTranscripts, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchTranscripts = async () => {
    try {
      const data = await getTranscripts();
      if (data.status === "success") {
        setTranscripts(data.data);
      }
    } catch (err) {
      console.error("Failed to fetch transcripts", err);
    }
    setLoading(false);
  };

  if (loading) {
    return <p>Loading transcripts...</p>;
  }

  if (transcripts.length === 0) {
    return (
      <div style={{ marginTop: "40px", textAlign: "center" }}>
        <p>No transcripts yet. Start recording to see results here.</p>
      </div>
    );
  }

  return (
    <div style={{ marginTop: "40px", maxWidth: "600px", margin: "40px auto" }}>
      <h2>Transcripts</h2>
      {transcripts.map((t) => (
        <div
          key={t.id}
          style={{
            border: "1px solid #ddd",
            borderRadius: "5px",
            padding: "15px",
            marginBottom: "10px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <p style={{ margin: "0 0 10px 0" }}>{t.text}</p>
          <small style={{ color: "#666" }}>
            {new Date(t.created_at).toLocaleString()} | Status: {t.status}
          </small>
        </div>
      ))}
    </div>
  );
}

export default TranscriptList;
