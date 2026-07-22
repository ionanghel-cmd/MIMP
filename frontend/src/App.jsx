import { useState } from 'react';
import { Package, Truck, Users, DollarSign, LogOut } from 'lucide-react';

function App() {
  const [page, setPage] = useState('dashboard');

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 p-6 border-r border-gray-800 flex flex-col">
        <div className="flex items-center gap-3 mb-12">
          <Package className="text-emerald-500" size={36} />
          <h1 className="text-2xl font-bold">MotoParts Manager</h1>
        </div>
        <nav className="flex-1 space-y-2">
          <button onClick={() => setPage('dashboard')} className="w-full text-left p-4 rounded-2xl hover:bg-gray-800 flex items-center gap-3">Dashboard</button>
          <button onClick={() => setPage('comenzi')} className="w-full text-left p-4 rounded-2xl hover:bg-gray-800 flex items-center gap-3">Comenzi</button>
          <button onClick={() => setPage('clienti')} className="w-full text-left p-4 rounded-2xl hover:bg-gray-800 flex items-center gap-3">Clienți</button>
        </nav>
        <button className="flex items-center gap-3 text-red-500 mt-auto">
          <LogOut /> Logout
        </button>
      </div>

      <div className="flex-1 p-8 overflow-auto">
        {page === 'dashboard' && <Dashboard />}
        {page === 'comenzi' && <Comenzi />}
        {page === 'clienti' && <Clienți />}
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <div>
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-gray-900 p-8 rounded-3xl">
          <DollarSign className="text-emerald-500 mb-4" size={40} />
          <p className="text-5xl font-bold">12.540 €</p>
          <p className="text-emerald-500">Profit Total</p>
        </div>
        <div className="bg-gray-900 p-8 rounded-3xl">
          <Truck className="text-blue-500 mb-4" size={40} />
          <p className="text-5xl font-bold">23</p>
          <p className="text-blue-500">În Transport</p>
        </div>
      </div>
    </div>
  );
}

function Comenzi() {
  return <div className="text-2xl">Pagina Comenzi - Aici vei adăuga comenzi + cost transport</div>;
}

function Clienți() {
  return <div className="text-2xl">Pagina Clienți</div>;
}

export default App;
