import { DonationList } from './components/DonationList';
import { DonationForm } from './components/DonationForm';

function App() {
  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-5xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900">
            Sisdoa <span className="text-blue-600 text-xl font-normal">Gestão de Estoque Solidário</span>
          </h1>
        </header>
        
        <DonationForm />
        
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 border-b pb-4">
            Estoque Atual
          </h2>
          <DonationList />
        </div>
      </div>
    </main>
  );
}

export default App;
