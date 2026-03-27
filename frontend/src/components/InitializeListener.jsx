import { useState, useEffect } from "react";
import { initializeListener, stopListener, getListenerStatus } from "../services/api";

function InitializeListener() {
  const [isActive, setIsActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const data = await getListenerStatus();
        setIsActive(data.is_active);
        setIsRecording(data.is_recording);
      } catch (err) {
        console.error("Failed to check listener status", err);
      }
    };
    checkStatus();
    const interval = setInterval(checkStatus, 500);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    setLoading(true);
    setMessage("");
    try {
      const data = await initializeListener();
      if (data.status === "success") {
        setIsActive(true);
        setMessage("Listener started! Press Ctrl+Space to record.");
      } else {
        setMessage(data.message);
      }
    } catch (err) {
      setMessage("Failed to start listener");
    }
    setLoading(false);
  };

  const handleStop = async () => {
    setLoading(true);
    setMessage("");
    try {
      const data = await stopListener();
      if (data.status === "success") {
        setIsActive(false);
        setIsRecording(false);
        setMessage("Listener stopped");
      } else {
        setMessage(data.message);
      }
    } catch (err) {
      setMessage("Failed to stop listener");
    }
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Voice Clipboard Assistant</h1>
      <p>Hotkey: <strong>Ctrl + Space</strong></p>
      
      <div style={{ margin: "20px 0" }}>
        <button
          onClick={handleStart}
          disabled={loading || isActive}
          style={{
            padding: "15px 30px",
            fontSize: "18px",
            marginRight: "10px",
            backgroundColor: isActive ? "#ccc" : "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: loading || isActive ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Starting..." : "Initialize Listener"}
        </button>
        
        <button
          onClick={handleStop}
          disabled={loading || !isActive}
          style={{
            padding: "15px 30px",
            fontSize: "18px",
            backgroundColor: !isActive ? "#ccc" : "#f44336",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: !isActive ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Stopping..." : "Stop Listener"}
        </button>
      </div>

      <div
        style={{
          marginTop: "20px",
          padding: "15px",
          borderRadius: "5px",
          backgroundColor: isRecording ? "#ffeb3b" : isActive ? "#e8f5e9" : "#ffebee",
          display: "inline-block",
          minWidth: "300px",
          transition: "background-color 0.3s ease",
        }}
      >
        <strong>Status:</strong> 
        {isRecording ? "Recording..." : isActive ? "Active" : "Inactive"}
        <br />
        <small>
          {isRecording ? "Release Ctrl+Space to stop" : 
           isActive ? "Hold Ctrl+Space to record..." : 
           "Click Initialize to start"}
        </small>
        {isRecording && (
          <div style={{ marginTop: "10px" }}>
            <span style={{ 
              display: "inline-block",
              width: "12px",
              height: "12px",
              borderRadius: "50%",
              backgroundColor: "#f44336",
              animation: "pulse 1s infinite",
            }} />
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.4; }
          100% { opacity: 1; }
        }
      `}</style>

      {message && (
        <p style={{ marginTop: "20px", color: "#666" }}>{message}</p>
      )}
    </div>
  );
}

export default InitializeListener;
