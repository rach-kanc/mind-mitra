import axios from 'axios';

export const sendChatMessage = async (message: string, token: string) =>
  axios.post('/api/v1/chat', { message }, { headers: { Authorization: `Bearer ${token}` } }); 