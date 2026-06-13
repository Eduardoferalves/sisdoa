// Contratos de tipagem baseados na Web API do Sisdoa

export interface DonationItemResponse {
  id: number; // ou string dependendo da persistência do UUID
  name: string;
  quantity: number;
  expiration_date: string; // ISO 8601 date string
  created_at?: string;
  is_expired?: boolean;
}

export interface DonationItemCreate {
  name: string;
  quantity: number;
  expiration_date: string; // Formato YYYY-MM-DD
}
