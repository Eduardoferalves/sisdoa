import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateDonation } from '../services/queries';

// 1. Definição do Schema (Espelho do Pydantic no Backend)
const donationSchema = z.object({
  ean: z.string().optional(),
  name: z.string().min(2, 'O nome deve ter no mínimo 2 caracteres').optional().or(z.literal('')),
  quantity: z.number().min(1, 'A quantidade deve ser no mínimo 1'),
  expiration_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Use o formato AAAA-MM-DD'),
}).refine(data => data.ean || data.name, {
  message: "Forneça o EAN ou o Nome do produto",
  path: ["name"],
});

type DonationFormInputs = z.infer<typeof donationSchema>;

export function DonationForm() {
  const { mutate, isPending, isError } = useCreateDonation();
  
  const { register, handleSubmit, formState: { errors }, reset } = useForm<DonationFormInputs>({
    resolver: zodResolver(donationSchema),
    defaultValues: {
      ean: '',
      name: '',
      quantity: 1,
      expiration_date: '',
    }
  });

  const onSubmit = (data: DonationFormInputs) => {
    // Transforma o payload para o formato esperado pela API (DonationItemCreate)
    const payload = {
      name: data.name || 'Produto via EAN', 
      quantity: data.quantity,
      expiration_date: data.expiration_date,
    };

    // A mutation já cuidará de invalidar o cache e atualizar a tabela
    mutate({ payload, ean: data.ean || undefined }, {
      onSuccess: () => {
        reset(); // Limpa o formulário após o sucesso
      }
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 className="text-lg font-bold text-gray-800 mb-4">Nova Doação</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">EAN (Código de Barras)</label>
          <input 
            {...register('ean')} 
            type="text" 
            placeholder="Opcional se informar o Nome"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Nome do Produto</label>
          <input 
            {...register('name')} 
            type="text" 
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
          />
          {errors.name && <span className="text-red-500 text-xs">{errors.name.message}</span>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Quantidade</label>
          <input 
            {...register('quantity', { valueAsNumber: true })} 
            type="number" 
            min="1"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
          />
          {errors.quantity && <span className="text-red-500 text-xs">{errors.quantity.message}</span>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Data de Validade</label>
          <input 
            {...register('expiration_date')} 
            type="date" 
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border"
          />
          {errors.expiration_date && <span className="text-red-500 text-xs">{errors.expiration_date.message}</span>}
        </div>
      </div>

      {isError && (
        <div className="mt-4 text-red-600 text-sm font-medium">
           Erro ao cadastrar: Verifique se o EAN existe no OpenFoodFacts ou se a API está online.
        </div>
      )}

      <button 
        type="submit" 
        disabled={isPending}
        className="mt-6 w-full bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50 transition-colors"
      >
        {isPending ? 'Cadastrando...' : 'Registrar Doação'}
      </button>
    </form>
  );
}
