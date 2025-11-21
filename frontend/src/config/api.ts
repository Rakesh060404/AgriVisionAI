// API Configuration
// Uses environment variable or falls back to localhost for development
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
    PREDICT: `${API_BASE_URL}/api/predict`,
    CHAT: `${API_BASE_URL}/api/chat`,
    HEALTH: `${API_BASE_URL}/api/health`,
} as const;

