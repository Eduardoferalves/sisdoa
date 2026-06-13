import { useDonations } from '../services/queries';

export function DonationList() {
  const { data: donations, isLoading, isError } = useDonations();

  if (isLoading) return <div className="p-4 text-gray-500">Carregando doações...</div>;
  if (isError) return <div className="p-4 text-red-500">Erro ao carregar o estoque.</div>;
  if (!donations || donations.length === 0) return <div className="p-4 text-gray-500">Estoque vazio.</div>;

  return (
    <div className="overflow-x-auto shadow-md sm:rounded-lg mt-6">
      <table className="w-full text-sm text-left text-gray-700">
        <thead className="text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3">ID</th>
            <th scope="col" className="px-6 py-3">Produto</th>
            <th scope="col" className="px-6 py-3">Quantidade</th>
            <th scope="col" className="px-6 py-3">Validade</th>
          </tr>
        </thead>
        <tbody>
          {donations.map((item) => (
            <tr key={item.id} className="bg-white border-b hover:bg-gray-50">
              <td className="px-6 py-4 font-medium text-gray-900">{item.id}</td>
              <td className="px-6 py-4">{item.name}</td>
              <td className="px-6 py-4">{item.quantity}</td>
              <td className={`px-6 py-4 ${item.is_expired ? 'text-red-600 font-bold' : ''}`}>
                {new Date(item.expiration_date).toLocaleDateString('pt-BR')}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
