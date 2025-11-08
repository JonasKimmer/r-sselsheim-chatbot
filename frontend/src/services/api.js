import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatService = {
  /**
   * Send a chat message
   * @param {string} message - User message
   * @param {string|null} sessionId - Optional session ID
   * @returns {Promise} Response with message and session ID
   */
  sendMessage: async (message, sessionId = null) => {
    const response = await api.post('/api/chat/', {
      message,
      session_id: sessionId,
    });
    return response.data;
  },

  /**
   * Get chat history for a session
   * @param {string} sessionId - Session ID
   * @returns {Promise} Chat history
   */
  getHistory: async (sessionId) => {
    const response = await api.get(`/api/chat/${sessionId}/history`);
    return response.data;
  },
};

export const documentService = {
  /**
   * Search for documents
   * @param {string} query - Search query
   * @param {number} limit - Maximum results
   * @returns {Promise} Search results
   */
  search: async (query, limit = 5) => {
    const response = await api.post('/api/documents/search', {
      query,
      limit,
    });
    return response.data;
  },
};

export const healthService = {
  /**
   * Check API health
   * @returns {Promise} Health status
   */
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
