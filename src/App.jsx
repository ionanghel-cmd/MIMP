import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'https://good-ange-vdm-da4c7af1.koyeb.app/api';  // schimbă cu link-ul tău

function App() {
  const [clients, setClients] = useState([]);
  const [comenzi, setComenzi] = useState([]);
  const [newClient, setNewClient] = useState({ nume: '', telefon: '' });

  useEffect(() => {
    axios.get(`${API_URL}/clients/`).then(res => setClients(res.data));
  }, []);

  const addClient = () => {
    axios.post(`${API_URL}/clients/`, newClient).then(() => {
      setNewClient({ nume: '', telefon: '' });
      window.location.reload();
    });
  };

  return (
    <div className="p-8 bg-gray-950 text-white min-h-screen">
      <h1 className="text-4xl font-bold mb-8">OEM Parts ERP</h1>

      {/* Dashboard */}
      <div className="grid grid-cols-4 gap-6 mb-12">
        <div className="bg-gray-900 p-6 rounded-2xl">Comenzi Așteptare: {comenzi.length}</div>
        <div className="bg-gray-900 p-6 rounded-2xl">Profit Estimat: 8450 €</div>
      </div>

      {/* Adaugă Client */}
      <div className="mb-12">
        <h2 className="text-2xl mb-4">Adaugă Client</h2>
        <input placeholder="Nume" value={newClient.nume} onChange={e => setNewClient({...newClient, nume: e.target.value})} className="p-4 bg-gray-800 rounded-xl mr-4" />
        <input placeholder="Telefon" value={newClient.telefon} onChange={e => setNewClient({...newClient, telefon: e.target.value})} className="p-4 bg-gray-800 rounded-xl mr-4" />
        <button onClick={addClient} className="bg-emerald-600 px-8 py-4 rounded-xl">Salvează</button>
      </div>

      {/* Lista Clienți */}
      <h2 className="text-2xl mb-4">Clienți</h2>
      <div className="grid gap-4">
        {clients.map(c => <div key={c.id} className="bg-gray-900 p-6 rounded-2xl">{c.nume} - {c.telefon}</div>)}
      </div>
    </div>
  );
}

export default App;
