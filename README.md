# MotoERP - OEM Parts Distribution ERP

Aplicație Streamlit + Supabase pentru gestionarea distribuției de piese OEM (motociclete, mașini, etc.)

## 🚀 Funcționalități

### Dashboard
- 💰 Profit azi, lună, an
- 📦 Comenzi în așteptare, expediate, întârziate
- 📈 Grafice de performanță
- 👥 Clienți noi și recurenți
- ⭐ Top 10 clienți și produse

### Gestionare Clienți
- Fișă completă per client
- Tip client (persoană, service, magazin, dealer)
- Limita de credit și discount
- Istoric cumpărături și profit generat
- Ultimă comandă

### Gestionare Comenzi
- Status comenzi (9 statușuri)
- Dată, client, operator, observații
- Conectare piese și transport
- Urmărire în timp real

### Gestionare Piese
- Cod OEM și furnizor
- Marcă, model, an
- Categorie (motor, frâne, suspensie, electric)
- Cost furnizor, transport, taxe, TVA
- Preț vânzare și profit
- Marjă procentuală

### Transport
- Urmărire colete
- Distribuire cost transport (greutate, volum, egal, manual)
- Furnizor și curier
- Date plecare/sosire

### Rapoarte și Analize
- Profit pe zile, luni, ani
- Profit per client, marcă, categorie, operator, furnizor
- KPI (rată conversie, valoare medie comandă, timp livrare)
- Istoric preț OEM
- Statistici (cele mai căutate, profitabile, lente, retururi)

### CRM
- Istoric comenzi per client
- Istoric piese
- Istoric oferte
- Mesaje și follow-up

### Funcții Avansate
- Wishlist pentru clienți
- Follow-up automat (6 luni)
- Blacklist clienți
- Notificări automate
- Căutare după VIN, OEM, telefon, nume
- AI recommendations (în faza 2)

## 📋 Structura Proiectului

```
moto-erp/
├── app/
│   ├── __init__.py
│   ├── app.py              # Aplicația Streamlit
│   ├── database.py         # Conexiune Supabase
│   ├── managers.py         # Business logic
│   └── utils.py            # Funcții utilitare
├── database/
│   └── schema.sql          # Schema Supabase
├── requirements.txt        # Dependințe Python
├── Dockerfile              # Containerizare
├── docker-compose.yml      # Orchestrare Docker
├── .env.example            # Template variabile de mediu
└── README.md               # Documentație
```

## 🛠️ Setup și Instalare

### Prerequisite
- Python 3.11+
- Docker și Docker Compose (optional)
- Cont Supabase (https://supabase.com)

### 1. Clonează Repo
```bash
git clone <repo-url>
cd moto-erp
```

### 2. Configurare Supabase
- Creează cont pe Supabase
- Creează proiect nou
- Accesează SQL Editor și rulează schema din `database/schema.sql`
- Copiază URL și API Key din Settings → API

### 3. Configurare Variabile de Mediu
```bash
cp .env.example .env
# Editează .env și adaugă:
# SUPABASE_URL=https://xxx.supabase.co
# SUPABASE_KEY=eyJhbGc...
```

### 4. Instalare Dependințe
```bash
pip install -r requirements.txt
```

### 5. Rulare Aplicație

**Local:**
```bash
streamlit run app/app.py
```

**Docker:**
```bash
docker-compose up
```

Accesează aplicația la `http://localhost:8501`

## 📊 Bază de Date - Tabele

### clients
- id (PK)
- name
- phone
- email
- city
- country
- type (person, service, shop, dealer)
- discount_percent
- credit_limit
- total_purchases
- profit_generated
- last_order_date
- observations
- created_at
- updated_at

### orders
- id (PK)
- client_id (FK)
- operator
- status (9 statuse)
- total_amount
- profit
- observations
- created_at
- updated_at

### parts
- id (PK)
- oem_code
- supplier_code
- brand
- model
- year
- category
- supplier_cost
- transport_cost
- taxes
- tva
- final_cost
- sale_price
- profit
- margin_percent
- created_at
- updated_at

### suppliers
- id (PK)
- name
- country
- contact_person
- email
- phone
- website
- currency
- avg_delivery_time
- discount
- created_at
- updated_at

### transport
- id (PK)
- order_id (FK)
- supplier
- tracking_number
- courier
- weight
- volume
- total_cost
- departure_date
- arrival_date
- created_at
- updated_at

### invoices
- id (PK)
- order_id (FK)
- type (supplier, client)
- invoice_number
- amount
- vat
- paid_amount
- outstanding_amount
- created_at
- updated_at

### expenses
- id (PK)
- category (internet, marketing, transport, etc.)
- amount
- description
- date
- created_at

## 🔐 Autentificare

**Faza 1:** Dezvoltare fără autentificare
**Faza 2:** JWT + Roluri (Administrator, Operator, Contabil)

## 📈 Roadmap

### MVP (Faza 1) - CURRENT
- ✅ Dashboard cu KPI-uri de bază
- ✅ CRUD Clienți
- ✅ CRUD Comenzi
- ✅ CRUD Piese
- ✅ Rapoarte simple

### Faza 2
- [ ] Autentificare și roluri
- [ ] Notificări avansate
- [ ] AI recommendations (VIN parsing, part suggestions)
- [ ] Calendar și agenda
- [ ] Export PDF/Excel
- [ ] Email integration

### Faza 3
- [ ] Multi-user collaboration
- [ ] API REST pentru integrări
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Stock management
- [ ] Supplier auto-updates

### Faza 4 (Produsul)
- [ ] SaaS version
- [ ] White-label
- [ ] API marketplace
- [ ] Integrații 3rd party

## 📝 Licență

MIT License

## 👤 Contact

Pentru întrebări sau sugestii, contactează development team.