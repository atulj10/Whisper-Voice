import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Mic, Square, Activity } from "lucide-react";
import {
  initializeListener,
  stopListener,
  getListenerStatus,
} from "../services/api";

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
        setMessage("Listener started! Press Ctrl + Space to record.");
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

  const statusColor = isRecording
    ? "bg-yellow-100 text-yellow-800"
    : isActive
      ? "bg-green-100 text-green-700"
      : "bg-red-100 text-red-700";

  const statusText = isRecording
    ? "Recording"
    : isActive
      ? "Active"
      : "Inactive";

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-xl bg-white shadow-xl rounded-2xl p-8 border border-gray-100"
      >
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-semibold text-black tracking-tight">
            Voice Clipboard Assistant
          </h1>
          <p className="text-sm text-gray-500 mt-2">
            Use <span className="font-medium text-black">Ctrl + Space</span> to
            start recording
          </p>
        </div>

        {/* Status Card */}
        <div className="flex items-center justify-between bg-gray-50 rounded-xl p-4 border border-gray-100 mb-6">
          <div className="flex items-center gap-3">
            <div
              className={`w-3 h-3 rounded-full ${
                isRecording ? "bg-red-500 animate-pulse" : "bg-gray-400"
              }`}
            />

            <div>
              <p className="text-sm text-gray-500">Status</p>
              <p
                className={`text-base font-medium ${statusColor} px-2 py-0.5 rounded-md inline-block`}
              >
                {statusText}
              </p>
            </div>
          </div>

          <Activity className="w-5 h-5 text-gray-400" />
        </div>

        {/* Actions */}
        <div className="grid grid-cols-2 gap-4">
          <button
            onClick={handleStart}
            disabled={loading || isActive}
            className={`flex items-center justify-center gap-2 px-4 py-3 rounded-xl font-medium text-white transition-all duration-200 shadow-sm ${
              loading || isActive
                ? "bg-gray-300 cursor-not-allowed"
                : "bg-[#5147f3] hover:bg-[#4338ca] active:scale-[0.98]"
            }`}
          >
            <Mic size={18} />
            {loading ? "Starting..." : "Initialize"}
          </button>

          <button
            onClick={handleStop}
            disabled={loading || !isActive}
            className={`flex items-center justify-center gap-2 px-4 py-3 rounded-xl font-medium text-white transition-all duration-200 shadow-sm ${
              loading || !isActive
                ? "bg-gray-300 cursor-not-allowed"
                : "bg-red-500 hover:bg-red-600 active:scale-[0.98]"
            }`}
          >
            <Square size={18} />
            {loading ? "Stopping..." : "Stop"}
          </button>
        </div>

        {/* Helper Text */}
        <div className="mt-6 text-center text-sm text-gray-500">
          {isRecording
            ? "Release Ctrl + Space to stop recording"
            : isActive
              ? "Hold Ctrl + Space to record"
              : "Click Initialize to start listener"}
        </div>

        {/* Message */}
        {message && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 text-center text-sm text-gray-600"
          >
            {message}
          </motion.p>
        )}
      </motion.div>
    </div>
  );
}

export default InitializeListener;
