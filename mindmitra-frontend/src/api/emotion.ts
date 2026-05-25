import axios from 'axios';

export const detectEmotion = async (text: string, token: string) =>
  axios.post('/api/v1/emotion', { text }, { headers: { Authorization: `Bearer ${token}` } });

export const detectEmotionFromImage = async (image_base64: string, token: string) =>
  axios.post('/api/v1/emotion', { image_base64 }, { headers: { Authorization: `Bearer ${token}` } }); 