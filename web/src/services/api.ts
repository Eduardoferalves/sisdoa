import axios from 'axios';

// A URL base muda de acordo com o ambiente.
// Em dev (npm run dev), bate direto no FastAPI local.
// Em prod (Vercel), usa a raiz para que os rewrites do vercel.json encaminhem para o serverless function.
const getBaseUrl = () => {
  return import.meta.env.DEV ? 'http://localhost:8000' : '';
};

export const api = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Opcional futuro: api.interceptors.response.use() para tratamento global de erros HTTP 404 e 503.
