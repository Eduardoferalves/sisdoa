import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import type { DonationItemResponse, DonationItemCreate } from '../types/api';

export const useDonations = () => {
  return useQuery({
    queryKey: ['donations'],
    queryFn: async () => {
      const { data } = await api.get<DonationItemResponse[]>('/donations/');
      return data;
    },
  });
};

export const useExpiredDonations = () => {
  return useQuery({
    queryKey: ['donations', 'expired'],
    queryFn: async () => {
      const { data } = await api.get<DonationItemResponse[]>('/donations/expired');
      return data;
    },
  });
};

export const useCreateDonation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ payload, ean }: { payload: DonationItemCreate; ean?: string }) => {
      const url = ean ? `/donations/?ean=${ean}` : '/donations/';
      const { data } = await api.post<DonationItemResponse>(url, payload);
      return data;
    },
    onSuccess: () => {
      // Invalida o cache para forçar a atualização da tabela automaticamente
      queryClient.invalidateQueries({ queryKey: ['donations'] });
    },
  });
};
