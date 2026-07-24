import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, Truck, Users, DollarSign, Plus, X } from 'lucide-react';

const API_URL = 'https://good-ange-vdm-da4c7af1.koyeb.app/api';

function App() {
  const [page, setPage] = useState('dashboard');
  const [comenzi, setComenzi] = useState([]);
  const [clients, setClients] = useState([]);
  const [dashboard, setDashboard] = useState({});
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    client_id: '',
    cost_transport_total: '',
    observatii: '',
    piese: [{ cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
  });

  // Încarcă datele la pornire
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [comenziRes, clientsRes, dashRes] = await Promise.all([
        axios.get(`${API_URL}/comenzi/`),
        axios.get(`${API_URL}/clients/`),
        axios.get(`${API_URL}/dashboard/`)
      ]);
      setComenzi(comenziRes.data);
      setClients(clientsRes.data);
      setDashboard(dashRes.data);
    } catch (err) {
      console.error('Eroare la încărcare date:', err);
    }
  };

  const handleAddComanda = async () => {
    if (!formData.client_id || !formData.cost_transport_total) {
      alert('Completează Client și Cost Transport!');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API_URL}/comenzi/`, {
        client_id: formData.client_id,
        cost_transport_total: Number(formData.cost_transport_total),
        observatii: formData.observatii,
        piese: formData.piese.map(p => ({
          ...p,
          cantitate: Number(p.cantitate),
          pret_cumparare: Number(p.pret_cumparare),
          pret_vanzare: Number(p.pret_vanzare)
        }))
      });

      alert('Comandă salvată cu succes!');
      setShowForm(false);
      setFormData({
        client_id: '',
        cost_transport_total: '',
        observatii: '',
        piese: [{ cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
      });
      fetchData(); // reîncarcă lista
    } catch (err) {
      console.error(err);
      alert('Eroare la salvare. Verifică dacă backend-ul rulează.');
    } finally {
      setLoading(false);
    }
  };

  const adaugaPiesa = () => {
    setFormData({
      ...formData,
      piese: [...formData.piese, { cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
    });
  };

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
          {['dashboard', 'comenzi', 'clienti'].map((p) => (
            <button
              key={p}
              onClick={() => setPage(p)}
              className={`w-full text-left px-4 py-3 rounded-xl transition ${
                page === p ? 'bg-emerald-600' : 'hover:bg-gray-800'
              }`}
            >
              {p === 'dashboard' ? 'Dashboard' : p === 'comenzi' ? 'Comenzi' : 'Clienți'}
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-emerald-600 rounded-full flex items-center justify-center font-bold">A</div>
            <div>
              <p className="font-medium">Alexandru</p>
              <p className="text-xs text-gray-400">Administrator</p>
            </div>
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto">
        {page === 'dashboard' && (
          <div className="p-8">
            <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <p className="text-emerald-500 text-sm">PROFIT TOTAL</p>
                <p className="text-4xl font-bold mt-2">{(dashboard.profit_total || 0).toFixed(2)} €</p>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <p className="text-blue-400 text-sm">COMENZI TOTALE</p>
                <p className="text-4xl font-bold mt-2">{dashboard.comenzi_totale || 0}</p>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <p className="text-orange-400 text-sm">ÎN TRANSPORT</p>
                <p className="text-4xl font-bold mt-2">{dashboard.in_transport || 0}</p>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <p className="text-purple-400 text-sm">CLIENȚI</p>
                <p className="text-4xl font-bold mt-2">{dashboard.clienti_noi || 0}</p>
              </div>
            </div>
          </div>
        )}

        {page === 'comenzi' && (
          <div className="p-8">
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold">Comenzi</h1>
              <button
                onClick={() => setShowForm(true)}
                className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium flex items-center gap-2"
              >
                <Plus size={20} /> Comandă Nouă
              </button>
            </div>

            <div className="space-y-4">
              {comenzi.length === 0 ? (
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 text-center text-gray-400">
                  Nu există comenzi încă. Adaugă prima comandă!
                </div>
              ) : (
                comenzi.map((c) => (
                  <div key={c.id} className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                    <div className="flex justify-between">
                      <div>
                        <h3 className="text-xl font-semibold">Comandă #{c.numar || c.id?.slice(0,8)}</h3>
                        <p className="text-gray-400 text-sm">{c.data} • {c.status}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-emerald-500 font-bold text-lg">{c.profit} € profit</p>
                        <p className="text-sm text-gray-400">Total: {c.total_vanzare} €</p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {page === 'clienti' && (
          <div className="p-8">
            <h1 className="text-3xl font-bold mb-8">Clienți</h1>
            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
              {clients.length === 0 ? (
                <p className="text-gray-400">Nu există clienți încă.</p>
              ) : (
                <div className="space-y-3">
                  {clients.map(c => (
                    <div key={c.id} className="flex justify-between items-center py-3 border-b border-gray-800">
                      <div>
                        <p className="font-medium">{c.nume}</p>
                        <p className="text-sm text-gray-400">{c.telefon}</p>
                      </div>
                      <span className="text-xs bg-gray-800 px-3 py-1 rounded-full">{c.tip}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* FORMULAR COMANDĂ NOUĂ */}
      {showForm && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Comandă Nouă</h2>
              <button onClick={() => setShowForm(false)}>
                <X size={24} />
              </button>
            </div>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Client *</label>
                <select
                  value={formData.client_id}
                  onChange={e => setFormData({...formData, client_id: e.target.value})}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
                >
                  <option value="">Selectează client</option>
                  {clients.map(c => (
                    <option key={c.id} value={c.id}>{c.nume} - {c.telefon}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-1">Cost Transport Total (€) *</label>
                <input
                  type="number"
                  value={formData.cost_transport_total}
                  onChange={e => setFormData({...formData, cost_transport_total: e.target.value})}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
                  placeholder="Ex: 80"
                />
              </div>
            </div>

            <h3 className="font-semibold mb-3">Piese</h3>
            {formData.piese.map((p, index) => (
              <div key={index} className="grid grid-cols-5 gap-3 mb-3">
                <input placeholder="Cod OEM" value={p.cod_oem}
                  onChange={e => {
                    const newPiese = [...formData.piese];
                    newPiese[index].cod_oem = e.target.value;
                    setFormData({...formData, piese: newPiese});
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input placeholder="Denumire" value={p.denumire}
                  onChange={e => {
                    const newPiese = [...formData.piese];
                    newPiese[index].denumire = e.target.value;
                    setFormData({...formData, piese: newPiese});
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input type="number" placeholder="Cant" value={p.cantitate}
                  onChange={e => {
                    const newPiese = [...formData.piese];
                    newPiese[index].cantitate = e.target.value;
                    setFormData({...formData, piese: newPiese});
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input type="number" placeholder="Preț cumpărare" value={p.pret_cumparare}
                  onChange={e => {
                    const newPiese = [...formData.piese];
                    newPiese[index].pret_cumparare = e.target.value;
                    setFormData({...formData, piese: newPiese});
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input type="number" placeholder="Preț vânzare" value={p.pret_vanzare}
                  onChange={e => {
                    const newPiese = [...formData.piese];
                    newPiese[index].pret_vanzare = e.target.value;
                    setFormData({...formData, piese: newPiese});
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
              </div>
            ))}

            <button onClick={adaugaPiesa} className="text-emerald-500 text-sm mb-6 hover:underline">
              + Adaugă altă piesă
            </button>

            <div className="flex gap-4">
              <button
                onClick={handleAddComanda}
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700 px-8 py-3 rounded-xl font-medium disabled:opacity-50"
              >
                {loading ? 'Se salvează...' : 'Salvează Comanda'}
              </button>
              <button onClick={() => setShowForm(false)} className="bg-gray-700 px-8 py-3 rounded-xl">
                Anulează
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
