const API_BASE_URL = "http://localhost:5000";

export const initializeListener = async () => {
  const response = await fetch(`${API_BASE_URL}/initialize-listener`, {
    method: "POST",
  });
  return response.json();
};

export const stopListener = async () => {
  const response = await fetch(`${API_BASE_URL}/stop-listener`, {
    method: "POST",
  });
  return response.json();
};

export const getListenerStatus = async () => {
  const response = await fetch(`${API_BASE_URL}/listener-status`);
  return response.json();
};

export const getTranscripts = async () => {
  const response = await fetch(`${API_BASE_URL}/transcripts`);
  return response.json();
};

export const healthCheck = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
};
