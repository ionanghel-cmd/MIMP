import { useState, useEffect } from 'react';
import axios from 'axios';
import { Package, Plus, X, Search, Trash2, Menu, LogOut } from 'lucide-react';

const API_URL = 'https://good-ange-vdm-da4c7af1.koyeb.app/api';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || 'null'));
  const [page, setPage] = useState('dashboard');
  const [clients, setClients] = useState([]);
  const [comenzi, setComenzi] = useState([]);
  const [dashboard, setDashboard] = useState({});
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Login form
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [loginError, setLoginError] = useState('');

  // Căutare
  const [search, setSearch] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  // Formulare
  const [showClientForm, setShowClientForm] = useState(false);
  const [showComandaForm, setShowComandaForm] = useState(false);
  const [editingComanda, setEditingComanda] = useState(null);
  const [selectedComanda, setSelectedComanda] = useState(null);

  const [clientForm, setClientForm] = useState({
    nume: '', telefon: '', email: '', oras: '', tip: 'persoana'
  });

  const [comandaForm, setComandaForm] = useState({
    client_id: '',
    cost_transport_total: '',
    observatii: '',
    piese: [{ cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
  });

  const [editForm, setEditForm] = useState({ status: '', observatii: '' });

  // Axios cu token
  const api = axios.create({
    baseURL: API_URL,
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  });

  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token]);

  const fetchData = async () => {
    try {
      const [clientsRes, comenziRes, dashRes] = await Promise.all([
        api.get('/clients/'),
        api.get('/comenzi/'),
        api.get('/dashboard/')
      ]);
      setClients(clientsRes.data || []);
      setComenzi(comenziRes.data || []);
      setDashboard(dashRes.data || {});
    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
        handleLogout();
      }
    }
  };

  // ==================== LOGIN ====================
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', loginForm.username);
      formData.append('password', loginForm.password);

      const res = await axios.post(`${API_URL}/auth/login`, formData);
      const { access_token, username, role } = res.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify({ username, role }));
      setToken(access_token);
      setUser({ username, role });
    } catch (err) {
      setLoginError(err.response?.data?.detail || 'Utilizator sau parolă greșită');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken('');
    setUser(null);
  };

  // Filtrare
  const filteredComenzi = comenzi.filter(c => {
    const matchSearch =
      !search ||
      (c.client_nume || '').toLowerCase().includes(search.toLowerCase()) ||
      String(c.numar || '').includes(search);
    const matchStatus = !filterStatus || c.status === filterStatus;
    return matchSearch && matchStatus;
  });

  // ==================== CLIENT ====================
  const handleAddClient = async () => {
    if (!clientForm.nume || !clientForm.telefon) {
      alert('Nume și Telefon sunt obligatorii!');
      return;
    }
    setLoading(true);
    try {
      await api.post('/clients/', {
        name: clientForm.nume,
        telefon: clientForm.telefon,
        email: clientForm.email,
        oras: clientForm.oras,
        tip: clientForm.tip
      });
      alert('Client adăugat!');
      setShowClientForm(false);
      setClientForm({ nume: '', telefon: '', email: '', oras: '', tip: 'persoana' });
      fetchData();
    } catch (err) {
      alert(JSON.stringify(err.response?.data || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClient = async (id, nume) => {
    if (!confirm(`Ștergi clientul "${nume}"?`)) return;
    try {
      await api.delete(`/clients/${id}`);
      alert('Client șters!');
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Eroare');
    }
  };

  // ==================== COMANDĂ ====================
  const handleAddComanda = async () => {
    if (!comandaForm.client_id || !comandaForm.cost_transport_total) {
      alert('Selectează client și cost transport!');
      return;
    }
    setLoading(true);
    try {
      await api.post('/comenzi/', {
        ...comandaForm,
        cost_transport_total: Number(comandaForm.cost_transport_total),
        piese: comandaForm.piese.map(p => ({
          ...p,
          cantitate: Number(p.cantitate) || 1,
          pret_cumparare: Number(p.pret_cumparare) || 0,
          pret_vanzare: Number(p.pret_vanzare) || 0
        }))
      });
      alert('Comandă salvată!');
      setShowComandaForm(false);
      setComandaForm({
        client_id: '', cost_transport_total: '', observatii: '',
        piese: [{ cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
      });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Eroare');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateComanda = async () => {
    if (!editingComanda) return;
    setLoading(true);
    try {
      await api.put(`/comenzi/${editingComanda.id}`, {
        status: editForm.status,
        observatii: editForm.observatii
      });
      alert('Comandă actualizată!');
      setEditingComanda(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Eroare');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteComanda = async (id, numar) => {
    if (!confirm(`Ștergi comanda #${numar}?`)) return;
    try {
      await api.delete(`/comenzi/${id}`);
      alert('Comandă ștearsă!');
      setSelectedComanda(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Eroare');
    }
  };

  const adaugaPiesa = () => {
    setComandaForm({
      ...comandaForm,
      piese: [...comandaForm.piese, { cod_oem: '', denumire: '', cantitate: 1, pret_cumparare: '', pret_vanzare: '' }]
    });
  };

  const changePage = (p) => {
    setPage(p);
    setSidebarOpen(false);
  };

  // ==================== LOGIN PAGE ====================
  if (!token) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 w-full max-w-md">
          <div className="flex items-center justify-center gap-3 mb-8">
            <div className="bg-emerald-600 p-3 rounded-xl">
              <Package size={28} />
            </div>
            <h1 className="text-2xl font-bold text-white">MotoParts Manager</h1>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Utilizator</label>
              <input
                type="text"
                value={loginForm.username}
                onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white"
                placeholder="admin"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Parolă</label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white"
                placeholder="••••••••"
                required
              />
            </div>

            {loginError && (
              <p className="text-red-400 text-sm text-center">{loginError}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-600 hover:bg-emerald-700 py-3 rounded-xl font-medium text-white disabled:opacity-50"
            >
              {loading ? 'Se autentifică...' : 'Autentificare'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // ==================== APP PRINCIPAL ====================
  return (
    <div className="flex h-screen bg-gray-950 text-white overflow-hidden">
      {/* OVERLAY mobil */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/60 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      {/* SIDEBAR */}
      <div className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-64 bg-gray-900 border-r border-gray-800 p-6 flex flex-col
        transform transition-transform duration-300
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="flex items-center justify-between mb-12">
          <div className="flex items-center gap-3">
            <div className="bg-emerald-600 p-2 rounded-xl">
              <Package size={24} />
            </div>
            <h1 className="text-lg font-bold">MotoParts Manager</h1>
          </div>
          <button className="lg:hidden" onClick={() => setSidebarOpen(false)}>
            <X size={24} />
          </button>
        </div>

        <nav className="flex-1 space-y-2">
          <button onClick={() => changePage('dashboard')} className={`w-full text-left px-4 py-3 rounded-xl ${page === 'dashboard' ? 'bg-emerald-600' : 'hover:bg-gray-800'}`}>
            Dashboard
          </button>
          <button onClick={() => changePage('comenzi')} className={`w-full text-left px-4 py-3 rounded-xl ${page === 'comenzi' ? 'bg-emerald-600' : 'hover:bg-gray-800'}`}>
            Comenzi
          </button>
          <button onClick={() => changePage('clienti')} className={`w-full text-left px-4 py-3 rounded-xl ${page === 'clienti' ? 'bg-emerald-600' : 'hover:bg-gray-800'}`}>
            Clienți
          </button>
        </nav>

        <div className="mt-auto pt-6 border-t border-gray-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-emerald-600 rounded-full flex items-center justify-center font-bold">
                {user?.username?.[0]?.toUpperCase() || 'A'}
              </div>
              <div>
                <p className="font-medium text-sm">{user?.username}</p>
                <p className="text-xs text-gray-400">{user?.role}</p>
              </div>
            </div>
            <button onClick={handleLogout} className="text-gray-400 hover:text-red-400" title="Logout">
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* MAIN */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="lg:hidden flex items-center gap-4 p-4 border-b border-gray-800">
          <button onClick={() => setSidebarOpen(true)}>
            <Menu size={24} />
          </button>
          <h1 className="font-bold text-lg">MotoParts Manager</h1>
        </div>

        <div className="flex-1 overflow-y-auto">
          {/* DASHBOARD */}
          {page === 'dashboard' && (
            <div className="p-4 md:p-8">
              <h1 className="text-2xl md:text-3xl font-bold mb-6">Dashboard</h1>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-4 md:p-6">
                  <p className="text-emerald-500 text-xs md:text-sm">PROFIT TOTAL</p>
                  <p className="text-2xl md:text-4xl font-bold mt-2">{(dashboard.profit_total || 0).toFixed(0)} €</p>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-4 md:p-6">
                  <p className="text-blue-400 text-xs md:text-sm">COMENZI</p>
                  <p className="text-2xl md:text-4xl font-bold mt-2">{dashboard.comenzi_totale || 0}</p>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-4 md:p-6">
                  <p className="text-orange-400 text-xs md:text-sm">TRANSPORT</p>
                  <p className="text-2xl md:text-4xl font-bold mt-2">{dashboard.in_transport || 0}</p>
                </div>
                <div className="bg-gray-900 border border-gray-800 rounded-2xl p-4 md:p-6">
                  <p className="text-purple-400 text-xs md:text-sm">CLIENȚI</p>
                  <p className="text-2xl md:text-4xl font-bold mt-2">{dashboard.clienti || 0}</p>
                </div>
              </div>
            </div>
          )}

          {/* COMENZI */}
          {page === 'comenzi' && (
            <div className="p-4 md:p-8">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <h1 className="text-2xl md:text-3xl font-bold">Comenzi</h1>
                <button onClick={() => setShowComandaForm(true)} className="bg-emerald-600 hover:bg-emerald-700 px-5 py-2.5 rounded-xl font-medium flex items-center gap-2 text-sm">
                  <Plus size={18} /> Comandă Nouă
                </button>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 mb-6">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 text-gray-400" size={18} />
                  <input
                    type="text"
                    placeholder="Caută client sau număr..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full bg-gray-900 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-sm"
                  />
                </div>
                <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-sm">
                  <option value="">Toate statusurile</option>
                  <option value="Cerere">Cerere</option>
                  <option value="Confirmata">Confirmată</option>
                  <option value="In transport">În transport</option>
                  <option value="Livrata">Livrată</option>
                  <option value="Finalizata">Finalizată</option>
                  <option value="Anulata">Anulată</option>
                </select>
              </div>

              <div className="space-y-3">
                {filteredComenzi.length === 0 ? (
                  <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 text-center text-gray-400">Nu există comenzi.</div>
                ) : (
                  filteredComenzi.map((c) => (
                    <div key={c.id} className="bg-gray-900 border border-gray-800 rounded-2xl p-4 md:p-5 cursor-pointer hover:border-emerald-600 transition" onClick={() => setSelectedComanda(c)}>
                      <div className="flex justify-between items-start gap-3">
                        <div className="min-w-0">
                          <h3 className="text-lg font-semibold">#{c.numar || '—'}</h3>
                          <p className="text-emerald-400 font-medium text-sm truncate">{c.client_nume}</p>
                          <p className="text-gray-400 text-xs mt-1">{c.data} • {c.status}</p>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <p className="text-emerald-500 font-bold">{c.profit} €</p>
                          <p className="text-xs text-gray-400">{c.total_vanzare} €</p>
                          <div className="flex gap-2 mt-2 justify-end">
                            <button onClick={(e) => { e.stopPropagation(); setEditingComanda(c); setEditForm({ status: c.status || 'Cerere', observatii: c.observatii || '' }); }} className="text-xs bg-gray-700 hover:bg-gray-600 px-3 py-1.5 rounded-lg">Edit</button>
                            <button onClick={(e) => { e.stopPropagation(); handleDeleteComanda(c.id, c.numar); }} className="text-xs bg-red-600/20 text-red-400 px-2 py-1.5 rounded-lg"><Trash2 size={14} /></button>
                          </div>
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
            <div className="p-4 md:p-8">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <h1 className="text-2xl md:text-3xl font-bold">Clienți</h1>
                <button onClick={() => setShowClientForm(true)} className="bg-emerald-600 hover:bg-emerald-700 px-5 py-2.5 rounded-xl font-medium flex items-center gap-2 text-sm">
                  <Plus size={18} /> Client Nou
                </button>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden">
                {clients.length === 0 ? (
                  <div className="p-8 text-center text-gray-400">Nu există clienți.</div>
                ) : (
                  <div className="divide-y divide-gray-800">
                    {clients.map((c) => (
                      <div key={c.id} className="p-4 flex justify-between items-center">
                        <div>
                          <p className="font-medium">{c.nume || c.name}</p>
                          <p className="text-sm text-gray-400">{c.telefon} • {c.oras || '-'}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="bg-gray-800 px-2 py-1 rounded-full text-xs">{c.tip}</span>
                          <button onClick={() => handleDeleteClient(c.id, c.nume || c.name)} className="text-red-400"><Trash2 size={16} /></button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ========== MODALS ========== */}
      {showClientForm && (
        <div className="fixed inset-0 bg-black/70 flex items-end sm:items-center justify-center z-50 p-0 sm:p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-t-2xl sm:rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold">Client Nou</h2>
              <button onClick={() => setShowClientForm(false)}><X size={22} /></button>
            </div>
            <div className="space-y-3">
              <input placeholder="Nume *" value={clientForm.nume} onChange={(e) => setClientForm({ ...clientForm, nume: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3" />
              <input placeholder="Telefon *" value={clientForm.telefon} onChange={(e) => setClientForm({ ...clientForm, telefon: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3" />
              <input placeholder="Email" value={clientForm.email} onChange={(e) => setClientForm({ ...clientForm, email: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3" />
              <input placeholder="Oraș" value={clientForm.oras} onChange={(e) => setClientForm({ ...clientForm, oras: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3" />
              <select value={clientForm.tip} onChange={(e) => setClientForm({ ...clientForm, tip: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3">
                <option value="persoana">Persoană fizică</option>
                <option value="service">Service</option>
                <option value="magazin">Magazin</option>
                <option value="dealer">Dealer</option>
              </select>
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={handleAddClient} disabled={loading} className="bg-emerald-600 hover:bg-emerald-700 px-5 py-3 rounded-xl font-medium flex-1 disabled:opacity-50">{loading ? '...' : 'Salvează'}</button>
              <button onClick={() => setShowClientForm(false)} className="bg-gray-700 px-5 py-3 rounded-xl">Anulează</button>
            </div>
          </div>
        </div>
      )}

      {showComandaForm && (
        <div className="fixed inset-0 bg-black/70 flex items-end sm:items-center justify-center z-50 p-0 sm:p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-t-2xl sm:rounded-2xl p-6 w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold">Comandă Nouă</h2>
              <button onClick={() => setShowComandaForm(false)}><X size={22} /></button>
            </div>
            <div className="space-y-4 mb-4">
              <select value={comandaForm.client_id} onChange={(e) => setComandaForm({ ...comandaForm, client_id: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3">
                <option value="">Selectează client *</option>
                {clients.map((c) => (<option key={c.id} value={c.id}>{c.nume || c.name} — {c.telefon}</option>))}
              </select>
              <input type="number" placeholder="Cost Transport (€) *" value={comandaForm.cost_transport_total} onChange={(e) => setComandaForm({ ...comandaForm, cost_transport_total: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3" />
            </div>
            <h3 className="font-semibold mb-3 text-sm">Piese</h3>
            {comandaForm.piese.map((p, index) => (
              <div key={index} className="grid grid-cols-2 sm:grid-cols-5 gap-2 mb-3">
                <input placeholder="Cod OEM" value={p.cod_oem} onChange={(e) => { const n = [...comandaForm.piese]; n[index].cod_oem = e.target.value; setComandaForm({ ...comandaForm, piese: n }); }} className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm" />
                <input placeholder="Denumire" value={p.denumire} onChange={(e) => { const n = [...comandaForm.piese]; n[index].denumire = e.target.value; setComandaForm({ ...comandaForm, piese: n }); }} className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm" />
                <input type="number" placeholder="Cant" value={p.cantitate} onChange={(e) => { const n = [...comandaForm.piese]; n[index].cantitate = e.target.value; setComandaForm({ ...comandaForm, piese: n }); }} className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm" />
                <input type="number" placeholder="Cumpărare" value={p.pret_cumparare} onChange={(e) => { const n = [...comandaForm.piese]; n[index].pret_cumparare = e.target.value; setComandaForm({ ...comandaForm, piese: n }); }} className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm" />
                <input type="number" placeholder="Vânzare" value={p.pret_vanzare} onChange={(e) => { const n = [...comandaForm.piese]; n[index].pret_vanzare = e.target.value; setComandaForm({ ...comandaForm, piese: n }); }} className="bg-gray-800 border border-gray-700 rounded-xl px-3 py-2 text-sm" />
              </div>
            ))}
            <button onClick={adaugaPiesa} className="text-emerald-500 text-sm mb-6">+ Adaugă piesă</button>
            <div className="flex gap-3">
              <button onClick={handleAddComanda} disabled={loading} className="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl font-medium disabled:opacity-50">{loading ? '...' : 'Salvează'}</button>
              <button onClick={() => setShowComandaForm(false)} className="bg-gray-700 px-6 py-3 rounded-xl">Anulează</button>
            </div>
          </div>
        </div>
      )}

      {editingComanda && (
        <div className="fixed inset-0 bg-black/70 flex items-end sm:items-center justify-center z-50 p-0 sm:p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-t-2xl sm:rounded-2xl p-6 w-full max-w-md">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold">Editează #{editingComanda.numar}</h2>
              <button onClick={() => setEditingComanda(null)}><X size={22} /></button>
            </div>
            <div className="space-y-4">
              <select value={editForm.status} onChange={(e) => setEditForm({ ...editForm, status: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3">
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
              <textarea value={editForm.observatii} onChange={(e) => setEditForm({ ...editForm, observatii: e.target.value })} className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 h-24" placeholder="Observații..." />
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={handleUpdateComanda} disabled={loading} className="bg-emerald-600 hover:bg-emerald-700 px-5 py-3 rounded-xl font-medium flex-1 disabled:opacity-50">{loading ? '...' : 'Salvează'}</button>
              <button onClick={() => setEditingComanda(null)} className="bg-gray-700 px-5 py-3 rounded-xl">Anulează</button>
            </div>
          </div>
        </div>
      )}

      {selectedComanda && (
        <div className="fixed inset-0 bg-black/70 flex items-end sm:items-center justify-center z-50 p-0 sm:p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-t-2xl sm:rounded-2xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-xl font-bold">#{selectedComanda.numar}</h2>
                <p className="text-emerald-400 text-sm mt-1">{selectedComanda.client_nume}</p>
                <p className="text-gray-400 text-xs">{selectedComanda.data} • {selectedComanda.status}</p>
              </div>
              <button onClick={() => setSelectedComanda(null)}><X size={22} /></button>
            </div>
            {selectedComanda.piese?.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm min-w-[500px]">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-700">
                      <th className="pb-2">OEM</th>
                      <th className="pb-2">Denumire</th>
                      <th className="pb-2">Cant</th>
                      <th className="pb-2">Cumpărare</th>
                      <th className="pb-2">Livrare</th>
                      <th className="pb-2">Vânzare</th>
                      <th className="pb-2">Profit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedComanda.piese.map((p, i) => (
                      <tr key={i} className="border-b border-gray-800">
                        <td className="py-2">{p.cod_oem}</td>
                        <td className="py-2">{p.denumire}</td>
                        <td className="py-2">{p.cantitate}</td>
                        <td className="py-2">{p.pret_cumparare}€</td>
                        <td className="py-2">{p.cost_livrare}€</td>
                        <td className="py-2">{p.pret_vanzare}€</td>
                        <td className="py-2 text-emerald-500">{p.profit}€</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-400">Nu există piese.</p>
            )}
            <div className="mt-6 grid grid-cols-3 gap-3">
              <div className="bg-gray-800 rounded-xl p-3 text-center">
                <p className="text-xs text-gray-400">Transport</p>
                <p className="font-bold">{selectedComanda.cost_transport_total}€</p>
              </div>
              <div className="bg-gray-800 rounded-xl p-3 text-center">
                <p className="text-xs text-gray-400">Vânzare</p>
                <p className="font-bold">{selectedComanda.total_vanzare}€</p>
              </div>
              <div className="bg-gray-800 rounded-xl p-3 text-center">
                <p className="text-xs text-gray-400">Profit</p>
                <p className="font-bold text-emerald-500">{selectedComanda.profit}€</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
