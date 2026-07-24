import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, Plus, X } from 'lucide-react';

const API_URL = 'https://good-ange-vdm-da4c7af1.koyeb.app/api';

function App() {
  const [page, setPage] = useState('dashboard');
  const [clients, setClients] = useState([]);
  const [comenzi, setComenzi] = useState([]);
  const [dashboard, setDashboard] = useState({});
  const [loading, setLoading] = useState(false);

  // Formulare
  const [showClientForm, setShowClientForm] = useState(false);
  const [showComandaForm, setShowComandaForm] = useState(false);
  const [editingComanda, setEditingComanda] = useState(null);

  const [clientForm, setClientForm] = useState({
    nume: '',
    telefon: '',
    email: '',
    oras: '',
    tip: 'persoana'
  });

  const [comandaForm, setComandaForm] = useState({
    client_id: '',
    cost_transport_total: '',
    observatii: '',
    piese: [{ cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
  });

  const [editForm, setEditForm] = useState({ status: '', observatii: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [clientsRes, comenziRes, dashRes] = await Promise.all([
        axios.get(`${API_URL}/clients/`),
        axios.get(`${API_URL}/comenzi/`),
        axios.get(`${API_URL}/dashboard/`)
      ]);
      setClients(clientsRes.data || []);
      setComenzi(comenziRes.data || []);
      setDashboard(dashRes.data || {});
    } catch (err) {
      console.error(err);
    }
  };

  // ==================== ADAUGĂ CLIENT ====================
  const handleAddClient = async () => {
    if (!clientForm.nume || !clientForm.telefon) {
      alert('Nume și Telefon sunt obligatorii!');
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API_URL}/clients/`, {
        name: clientForm.nume,
        telefon: clientForm.telefon,
        email: clientForm.email,
        oras: clientForm.oras,
        tip: clientForm.tip
      });
      alert('Client adăugat cu succes!');
      setShowClientForm(false);
      setClientForm({ nume: '', telefon: '', email: '', oras: '', tip: 'persoana' });
      fetchData();
    } catch (err) {
      alert(JSON.stringify(err.response?.data || err.message));
    } finally {
      setLoading(false);
    }
  };

  // ==================== ADAUGĂ COMANDĂ ====================
  const handleAddComanda = async () => {
    if (!comandaForm.client_id || !comandaForm.cost_transport_total) {
      alert('Selectează client și introdu costul de transport!');
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API_URL}/comenzi/`, {
        ...comandaForm,
        cost_transport_total: Number(comandaForm.cost_transport_total),
        piese: comandaForm.piese.map(p => ({
          ...p,
          cantitate: Number(p.cantitate) || 1,
          pret_cumparare: Number(p.pret_cumparare) || 0,
          pret_vanzare: Number(p.pret_vanzare) || 0
        }))
      });
      alert('Comandă salvată cu succes!');
      setShowComandaForm(false);
      setComandaForm({
        client_id: '',
        cost_transport_total: '',
        observatii: '',
        piese: [{ cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
      });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Eroare la salvare comandă');
    } finally {
      setLoading(false);
    }
  };

  // ==================== UPDATE COMANDĂ ====================
  const handleUpdateComanda = async () => {
    if (!editingComanda) return;
    setLoading(true);
    try {
      await axios.put(`${API_URL}/comenzi/${editingComanda.id}`, {
        status: editForm.status,
        observatii: editForm.observatii
      });
      alert('Comandă actualizată!');
      setEditingComanda(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Eroare la actualizare');
    } finally {
      setLoading(false);
    }
  };

  const adaugaPiesa = () => {
    setComandaForm({
      ...comandaForm,
      piese: [...comandaForm.piese, { cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
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
          <button onClick={() => setPage('dashboard')} className={`w-full text-left px-4 py-3 rounded-xl ${page === 'dashboard' ? 'bg-emerald-600' : 'hover:bg-gray-800'}`}>
            Dashboard
          </button>
          <button onClick={() => setPage('comenzi')} className={`w-full text-left px-4 py-3 rounded-xl ${page === 'comenzi' ? 'bg-emerald-600' : 'hover:bg-gray-800'}`}>
            Comenzi
          </button>
          <button onClick={() => setPage('clienti')} className={`w-full text-left px-4 py-3 rounded-xl ${page === 'clienti' ? 'bg-emerald-600' : 'hover:bg-gray-800'}`}>
            Clienți
          </button>
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
        {/* DASHBOARD */}
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
                <p className="text-4xl font-bold mt-2">{dashboard.clienti || 0}</p>
              </div>
            </div>
          </div>
        )}

        {/* COMENZI */}
        {page === 'comenzi' && (
          <div className="p-8">
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold">Comenzi</h1>
              <button
                onClick={() => setShowComandaForm(true)}
                className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium flex items-center gap-2"
              >
                <Plus size={20} /> Comandă Nouă
              </button>
            </div>

            <div className="space-y-4">
              {comenzi.length === 0 ? (
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 text-center text-gray-400">
                  Nu există comenzi. Adaugă prima comandă!
                </div>
              ) : (
                comenzi.map((c) => (
                  <div key={c.id} className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-xl font-semibold">#{c.id?.slice(0, 8)}</h3>
                        <p className="text-gray-400 text-sm">{c.data} • {c.status}</p>
                        {c.observatii && (
                          <p className="text-sm text-gray-500 mt-1">📝 {c.observatii}</p>
                        )}
                      </div>
                      <div className="text-right flex flex-col items-end gap-2">
                        <p className="text-emerald-500 font-bold text-lg">{c.profit} € profit</p>
                        <p className="text-sm text-gray-400">Total: {c.total_vanzare} €</p>
                        <button
                          onClick={() => {
                            setEditingComanda(c);
                            setEditForm({ status: c.status || 'Cerere', observatii: c.observatii || '' });
                          }}
                          className="text-sm bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg"
                        >
                          Editează
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* CLIENTI */}
        {page === 'clienti' && (
          <div className="p-8">
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold">Clienți</h1>
              <button
                onClick={() => setShowClientForm(true)}
                className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium flex items-center gap-2"
              >
                <Plus size={20} /> Client Nou
              </button>
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden">
              {clients.length === 0 ? (
                <div className="p-8 text-center text-gray-400">Nu există clienți. Adaugă primul client!</div>
              ) : (
                <table className="w-full">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-800">
                      <th className="p-4">Nume</th>
                      <th className="p-4">Telefon</th>
                      <th className="p-4">Oraș</th>
                      <th className="p-4">Tip</th>
                    </tr>
                  </thead>
                  <tbody>
                    {clients.map((c) => (
                      <tr key={c.id} className="border-b border-gray-800 hover:bg-gray-800/50">
                        <td className="p-4 font-medium">{c.nume || c.name}</td>
                        <td className="p-4">{c.telefon}</td>
                        <td className="p-4">{c.oras || '-'}</td>
                        <td className="p-4">
                          <span className="bg-gray-800 px-3 py-1 rounded-full text-xs">{c.tip}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}
      </div>

      {/* ========== FORMULAR CLIENT NOU ========== */}
      {showClientForm && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-md">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Client Nou</h2>
              <button onClick={() => setShowClientForm(false)}><X size={24} /></button>
            </div>

            <div className="space-y-4">
              <input
                placeholder="Nume complet *"
                value={clientForm.nume}
                onChange={(e) => setClientForm({ ...clientForm, nume: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
              />
              <input
                placeholder="Telefon *"
                value={clientForm.telefon}
                onChange={(e) => setClientForm({ ...clientForm, telefon: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
              />
              <input
                placeholder="Email"
                value={clientForm.email}
                onChange={(e) => setClientForm({ ...clientForm, email: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
              />
              <input
                placeholder="Oraș"
                value={clientForm.oras}
                onChange={(e) => setClientForm({ ...clientForm, oras: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
              />
              <select
                value={clientForm.tip}
                onChange={(e) => setClientForm({ ...clientForm, tip: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
              >
                <option value="persoana">Persoană fizică</option>
                <option value="service">Service</option>
                <option value="magazin">Magazin</option>
                <option value="dealer">Dealer</option>
              </select>
            </div>

            <div className="flex gap-4 mt-8">
              <button
                onClick={handleAddClient}
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium flex-1 disabled:opacity-50"
              >
                {loading ? 'Se salvează...' : 'Salvează Client'}
              </button>
              <button onClick={() => setShowClientForm(false)} className="bg-gray-700 px-6 py-3 rounded-xl">
                Anulează
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========== FORMULAR COMANDĂ NOUĂ ========== */}
      {showComandaForm && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Comandă Nouă</h2>
              <button onClick={() => setShowComandaForm(false)}><X size={24} /></button>
            </div>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Client *</label>
                <select
                  value={comandaForm.client_id}
                  onChange={(e) => setComandaForm({ ...comandaForm, client_id: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
                >
                  <option value="">Selectează client</option>
                  {clients.map((c) => (
                    <option key={c.id} value={c.id}>{c.nume || c.name} — {c.telefon}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-1">Cost Transport Total (€) *</label>
                <input
                  type="number"
                  value={comandaForm.cost_transport_total}
                  onChange={(e) => setComandaForm({ ...comandaForm, cost_transport_total: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
                  placeholder="Ex: 80"
                />
              </div>
            </div>

            <h3 className="font-semibold mb-3">Piese</h3>
            {comandaForm.piese.map((p, index) => (
              <div key={index} className="grid grid-cols-5 gap-3 mb-3">
                <input
                  placeholder="Cod OEM"
                  value={p.cod_oem}
                  onChange={(e) => {
                    const newPiese = [...comandaForm.piese];
                    newPiese[index].cod_oem = e.target.value;
                    setComandaForm({ ...comandaForm, piese: newPiese });
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input
                  placeholder="Denumire"
                  value={p.denumire}
                  onChange={(e) => {
                    const newPiese = [...comandaForm.piese];
                    newPiese[index].denumire = e.target.value;
                    setComandaForm({ ...comandaForm, piese: newPiese });
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input
                  type="number"
                  placeholder="Cant"
                  value={p.cantitate}
                  onChange={(e) => {
                    const newPiese = [...comandaForm.piese];
                    newPiese[index].cantitate = e.target.value;
                    setComandaForm({ ...comandaForm, piese: newPiese });
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input
                  type="number"
                  placeholder="Preț cumpărare"
                  value={p.pret_cumparare}
                  onChange={(e) => {
                    const newPiese = [...comandaForm.piese];
                    newPiese[index].pret_cumparare = e.target.value;
                    setComandaForm({ ...comandaForm, piese: newPiese });
                  }}
                  className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm"
                />
                <input
                  type="number"
                  placeholder="Preț vânzare"
                  value={p.pret_vanzare}
                  onChange={(e) => {
                    const newPiese = [...comandaForm.piese];
                    newPiese[index].pret_vanzare = e.target.value;
                    setComandaForm({ ...comandaForm, piese: newPiese });
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
              <button onClick={() => setShowComandaForm(false)} className="bg-gray-700 px-8 py-3 rounded-xl">
                Anulează
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========== FORMULAR EDITARE COMANDĂ ========== */}
      {editingComanda && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 w-full max-w-md">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Editează Comanda</h2>
              <button onClick={() => setEditingComanda(null)}>
                <X size={24} />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Status</label>
                <select
                  value={editForm.status}
                  onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3"
                >
                  <option value="Cerere">Cerere</option>
                  <option value="Oferta trimisa">Ofertă trimisă</option>
                  <option value="Confirmata">Confirmată</option>
                  <option value="Comandata la furnizor">Comandată la furnizor</option>
                  <option value="In transport">În transport</option>
                  <option value="Ajunsa">Ajunsă</option>
                  <option value="Livrata">Livrată</option>
                  <option value="Finalizata">Finalizată</option>
                  <option value="Anulata">Anulată</option>
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-1">Observații / Comentarii</label>
                <textarea
                  value={editForm.observatii}
                  onChange={(e) => setEditForm({ ...editForm, observatii: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 h-28"
                  placeholder="Adaugă comentarii..."
                />
              </div>
            </div>

            <div className="flex gap-4 mt-8">
              <button
                onClick={handleUpdateComanda}
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium flex-1 disabled:opacity-50"
              >
                {loading ? 'Se salvează...' : 'Salvează'}
              </button>
              <button onClick={() => setEditingComanda(null)} className="bg-gray-700 px-6 py-3 rounded-xl">
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
