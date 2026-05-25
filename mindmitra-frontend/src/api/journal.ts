import axios from 'axios';

export const fetchJournalEntries = async (token: string) =>
  axios.get('/api/v1/journal', { headers: { Authorization: `Bearer ${token}` } });

export const saveJournalEntry = async (entry: { mood: number; text: string }, token: string) =>
  axios.post('/api/v1/journal', entry, { headers: { Authorization: `Bearer ${token}` } }); 