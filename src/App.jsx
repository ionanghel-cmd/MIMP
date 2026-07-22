import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, Users, Truck, DollarSign, LogOut } from 'lucide-react';

const API_URL = 'https://good-ange-vdm-da4c7af1.koyeb.app/api';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [page, setPage] = useState('dashboard');
  const [comenzi, setComenzi] = useState([]);

  const login = async (username, password) => {
    try {
      const res = await axios.post(`${API_URL}/auth/login`, { username, password });
      localStorage.setItem('token', res.data.access_token);
      setToken(res.data.access_token);
    } catch (e) {
      alert("Login greșit");
    }
  };

  if (!token) {
    return <LoginPage onLogin={login} />;
  }

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      <Sidebar setPage={setPage} setToken={setToken} />
      <MainContent page={page} comenzi={comenzi} setComenzi={setComenzi} />
    </div>
  );
}

function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950">
      <div className="bg-gray-900 p-10 rounded-3xl w-96">
        <h1 className="text-3xl font-bold text-center mb-8">MotoParts Manager</h1>
        <input placeholder="Username" className="w-full p-4 bg-gray-800 rounded-2xl mb-4" value={username} onChange={e => setUsername(e.target.value)} />
        <input type="password" placeholder="Parolă" className="w-full p-4 bg-gray-800 rounded-2xl mb-6" value={password} onChange={e => setPassword(e.target.value)} />
        <button onClick={() => onLogin(username, password)} className="w-full bg-emerald-600 py-4 rounded-2xl font-semibold">Login</button>
      </div>
    </div>
  );
}

function Sidebar({ setPage, setToken }) {
  return (
    <div className="w-64 bg-gray-900 p-6 border-r border-gray-800 flex flex-col">
      <div className="flex items-center gap-3 mb-12">
        <Package className="text-emerald-500" size={36} />
        <h1 className="text-2xl font-bold">MotoParts</h1>
      </div>
      <nav className="flex-1 space-y-2">
        <button onClick={() => setPage('dashboard')} className="w-full text-left p-4 rounded-2xl hover:bg-gray-800 flex items-center gap-3">Dashboard</button>
        <button onClick={() => setPage('comenzi')} className="w-full text-left p-4 rounded-2xl hover:bg-gray-800 flex items-center gap-3">Comenzi</button>
        <button onClick={() => setPage('clienti')} className="w-full text-left p-4 rounded-2xl hover:bg-gray-800 flex items-center gap-3">Clienți</button>
      </nav>
      <button onClick={() => { localStorage.clear(); setToken(null); }} className="flex items-center gap-3 text-red-500 mt-auto">
        <LogOut /> Logout
      </button>
    </div>
  );
}

function MainContent({ page, comenzi, setComenzi }) {
  if (page === 'comenzi') return <ComenziPage comenzi={comenzi} setComenzi={setComenzi} />;
  return <DashboardPage />;
}

function DashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-gray-900 p-8 rounded-3xl">
          <DollarSign className="text-emerald-500 mb-4" size={40} />
          <p className="text-5xl font-bold">12.540 €</p>
          <p className="text-emerald-500">Profit Total</p>
        </div>
        {/* Adaugă mai multe carduri */}
      </div>
    </div>
  );
}

function ComenziPage({ comenzi, setComenzi }) {
  const [newComanda, setNewComanda] = useState({ client_id: '', observatii: '', cost_transport: 0 });

  const addComanda = () => {
    // Aici vei adăuga logica de alocare transport
    alert("Comandă adăugată + cost transport alocat automat!");
  };

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-8">Comenzi</h1>
      <div className="bg-gray-900 p-8 rounded-3xl mb-8">
        <h3 className="text-xl mb-6">Adaugă Comandă Nouă</h3>
        <input placeholder="ID Client" className="p-4 bg-gray-800 rounded-xl w-full mb-4" onChange={e => setNewComanda({...newComanda, client_id: e.target.value})} />
        <input placeholder="Cost Transport Total (€)" type="number" className="p-4 bg-gray-800 rounded-xl w-full mb-6" onChange={e => setNewComanda({...newComanda, cost_transport: parseFloat(e.target.value)})} />
        <button onClick={addComanda} className="bg-emerald-600 px-10 py-4 rounded-2xl font-semibold">Salvează + Alocă Costuri</button>
      </div>
    </div>
  );
}

export default App;
