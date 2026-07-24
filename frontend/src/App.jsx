import { useState } from 'react';
import { Package, Truck, Users, DollarSign, TrendingUp, LogOut, Bell, Settings } from 'lucide-react';

function App() {
  const [page, setPage] = useState('dashboard');

  return (
    <div className="flex h-screen bg-gray-950 text-white overflow-hidden">
      {/* SIDEBAR */}
      <div className="w-64 bg-gray-900 border-r border-gray-800 p-6 flex flex-col">
        <div className="flex items-center gap-3 mb-12">
          <div className="bg-emerald-600 p-2 rounded-xl">
            <Package size={28} />
          </div>
          <h1 className="text-xl font-bold">MotoParts Manager</h1>
        </div>

        <nav className="flex-1 space-y-2">
          <button
            onClick={() => setPage('dashboard')}
            className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition ${
              page === 'dashboard' ? 'bg-emerald-600' : 'hover:bg-gray-800'
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setPage('comenzi')}
            className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition ${
              page === 'comenzi' ? 'bg-emerald-600' : 'hover:bg-gray-800'
            }`}
          >
            Comenzi
          </button>
          <button
            onClick={() => setPage('clienti')}
            className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition ${
              page === 'clienti' ? 'bg-emerald-600' : 'hover:bg-gray-800'
            }`}
          >
            Clienți
          </button>
          <button
            onClick={() => setPage('piese')}
            className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition ${
              page === 'piese' ? 'bg-emerald-600' : 'hover:bg-gray-800'
            }`}
          >
            Piese
          </button>
          <button
            onClick={() => setPage('profit')}
            className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition ${
              page === 'profit' ? 'bg-emerald-600' : 'hover:bg-gray-800'
            }`}
          >
            Raport Profit
          </button>
        </nav>

        <div className="mt-auto pt-6 border-t border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-emerald-600 rounded-full flex items-center justify-center font-bold">
              A
            </div>
            <div>
              <p className="font-medium">Alexandru</p>
              <p className="text-xs text-gray-400">Administrator</p>
            </div>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto">
        {page === 'dashboard' && <Dashboard />}
        {page === 'comenzi' && <Comenzi />}
        {page === 'clienti' && <Clienti />}
        {page === 'piese' && <Piese />}
        {page === 'profit' && <Profit />}
      </div>
    </div>
  );
}

// ==================== DASHBOARD ====================
function Dashboard() {
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="text-sm text-gray-400">01 Iulie – 22 Iulie 2026</div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-emerald-500 text-sm font-medium">PROFIT TOTAL</p>
              <p className="text-4xl font-bold mt-2">12.540,75 €</p>
              <p className="text-emerald-500 text-sm mt-2">+18.6% față de luna trecută</p>
            </div>
            <DollarSign className="text-emerald-500" size={32} />
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-blue-400 text-sm font-medium">COMENZI TOTALE</p>
              <p className="text-4xl font-bold mt-2">48</p>
              <p className="text-blue-400 text-sm mt-2">+12.5% față de luna trecută</p>
            </div>
            <Package className="text-blue-400" size={32} />
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-orange-400 text-sm font-medium">ÎN TRANSPORT</p>
              <p className="text-4xl font-bold mt-2">23</p>
              <p className="text-orange-400 text-sm mt-2">Estimat să ajungă în 10 zile</p>
            </div>
            <Truck className="text-orange-400" size={32} />
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-purple-400 text-sm font-medium">CLIENȚI NOI</p>
              <p className="text-4xl font-bold mt-2">7</p>
              <p className="text-purple-400 text-sm mt-2">+40% față de luna trecută</p>
            </div>
            <Users className="text-purple-400" size={32} />
          </div>
        </div>
      </div>

      {/* Comenzi Recente */}
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Comenzi Recente</h2>
          <button className="text-emerald-500 text-sm hover:underline">Vezi toate comenzile →</button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left text-gray-400 text-sm border-b border-gray-800">
                <th className="pb-4 font-medium">ID Comanda</th>
                <th className="pb-4 font-medium">Client</th>
                <th className="pb-4 font-medium">Data</th>
                <th className="pb-4 font-medium">Status</th>
                <th className="pb-4 font-medium">Total</th>
                <th className="pb-4 font-medium">Profit</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              <tr className="border-b border-gray-800 hover:bg-gray-800/50">
                <td className="py-4 font-medium">#1048</td>
                <td className="py-4">Service Moto Chișinău</td>
                <td className="py-4">31 Iulie 2026</td>
                <td className="py-4">
                  <span className="bg-orange-500/20 text-orange-400 px-3 py-1 rounded-full text-xs">
                    În transport
                  </span>
                </td>
                <td className="py-4">256,80 €</td>
                <td className="py-4 text-emerald-500 font-medium">58,40 €</td>
              </tr>
              <tr className="border-b border-gray-800 hover:bg-gray-800/50">
                <td className="py-4 font-medium">#1047</td>
                <td className="py-4">Ion Popescu</td>
                <td className="py-4">31 Iulie 2026</td>
                <td className="py-4">
                  <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-xs">
                    Confirmată
                  </span>
                </td>
                <td className="py-4">123,50 €</td>
                <td className="py-4 text-emerald-500 font-medium">28,75 €</td>
              </tr>
              <tr className="border-b border-gray-800 hover:bg-gray-800/50">
                <td className="py-4 font-medium">#1046</td>
                <td className="py-4">MoldMoto SRL</td>
                <td className="py-4">30 Iulie 2026</td>
                <td className="py-4">
                  <span className="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-xs">
                    De livrat
                  </span>
                </td>
                <td className="py-4">542,00 €</td>
                <td className="py-4 text-emerald-500 font-medium">112,30 €</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ==================== COMENZI ====================
function Comenzi() {
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Comenzi</h1>
        <button className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium transition">
          + Comandă Nouă
        </button>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <p className="text-gray-400">
          Aici vei putea adăuga comenzi, aloca costul de transport automat și vedea profitul per piesă.
        </p>
      </div>
    </div>
  );
}

// ==================== CLIENTI ====================
function Clienti() {
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Clienți</h1>
        <button className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium transition">
          + Client Nou
        </button>
      </div>
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <p className="text-gray-400">Lista clienților va apărea aici.</p>
      </div>
    </div>
  );
}

// ==================== PIESE ====================
function Piese() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Piese</h1>
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <p className="text-gray-400">Catalog piese OEM.</p>
      </div>
    </div>
  );
}

// ==================== PROFIT ====================
function Profit() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Raport Profit</h1>
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
        <p className="text-gray-400">Grafice și rapoarte de profitabilitate.</p>
      </div>
    </div>
  );
}

export default App;
