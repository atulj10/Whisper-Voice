import { useState, useEffect } from "react";
import { FileText } from "lucide-react";
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
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Loading transcripts...</p>
      </div>
    );
  }

  if (transcripts.length === 0) {
    return (
      <div className="max-w-xl mx-auto px-4 mt-8 text-center">
        <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">No transcripts yet. Start recording to see results here.</p>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto px-4 mt-8">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Transcripts</h2>
      <div className="space-y-3">
        {transcripts.map((t) => (
          <div
            key={t.id}
            className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
          >
            <p className="text-gray-800 mb-2">{t.text}</p>
            <p className="text-xs text-gray-400">
              {new Date(t.created_at).toLocaleString()} • {t.status}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TranscriptList;
