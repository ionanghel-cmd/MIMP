# MotoERP - Implementation Checklist

Ghid pas cu pas pentru a pune în funcțiune aplicația.

## ✅ Phase 1 - MVP Setup (3-4 zile)

### A. Configurare Supabase (1 ora)

- [ ] Creează cont pe https://supabase.com
- [ ] Creează proiect nou (alege regiunea EU)
- [ ] Accesează Settings → API
- [ ] Copiază Project URL și copy anon public key
- [ ] Salvează credențialele temporar (vor fi în .env)
- [ ] În SQL Editor, copiază și rulează `database/schema.sql`
  - [ ] Verifică că 13 tabele sunt create
  - [ ] Verifică că index-urile s-au creat
  - [ ] Verifică că RLS e enabled

### B. Setup Local (2-3 ore)

- [ ] Clone repo:
  ```bash
  git clone <url>
  cd moto-erp
  ```
- [ ] Creează `.env` din ``.env.example`:
  ```bash
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_KEY=eyJhbGc...
  ```
- [ ] Creează virtual environment:
  ```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # Mac/Linux:
  source venv/bin/activate
  ```
- [ ] Instalează dependințe:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Testează import:
  ```bash
  python -c "import streamlit; print('OK')"
  ```

### C. First Run (1 ora)

- [ ] Rulează aplicația:
  ```bash
  streamlit run app/app.py
  ```
- [ ] Verifică că se deschide la http://localhost:8501
- [ ] Navigează pe fiecare pagină din meniu
- [ ] Verifică că nu sunt erori în console

### D. Test Manual (2 ore)

#### Dashboard
- [ ] Se încarcă fără erori
- [ ] KPI cards sunt vizibile
- [ ] Valorile sunt 0 (normal, nu avem date)
- [ ] Charts sunt prezente (dar goale)

#### Clienți
- [ ] Click pe "Adaugă Client"
- [ ] Completează form:
  - Nume: "Test Client 1"
  - Telefon: "0700000000"
  - Email: "test@example.com"
  - Oraș: "București"
  - Țară: "România"
  - Tip: "magazin"
  - Discount: 5
  - Credit limit: 5000
- [ ] Click "Salvează Client"
- [ ] Verifică success message
- [ ] Merge în Supabase SQL Editor:
  ```sql
  SELECT * FROM clients;
  ```
- [ ] Verifică că clientul e acolo
- [ ] Reîncarcă pagina și verifica că apare în "Lista Clienți"

#### Comenzi
- [ ] Adaugă o comandă:
  - Client ID: (copiază din tabela clienți)
  - Status: "confirmată"
  - Total: 250
  - Profit: 50
- [ ] Verifica că apare în listă
- [ ] Mergi la Supabase și verifică

#### Piese
- [ ] Adaugă o piesă:
  - OEM: "12345-HONDA-01"
  - Furnizor: "SUP001"
  - Marcă: "Honda"
  - Cost: 50
  - Preț: 75
- [ ] Verifica că profit e 25
- [ ] Merge în Supabase și verifica

---

## 🐳 Phase 2 - Docker Setup (1 ora)

### A. Testează Docker Build

```bash
# Build image
docker build -t moto-erp:latest .

# Rulează container
docker run -p 8501:8501 \
  --env-file .env \
  moto-erp:latest
```

### B. Testează Docker Compose

```bash
# Asigură-te că .env există în root
docker-compose up

# Accesează http://localhost:8501
# Ctrl+C pentru stop

# Verifică că funcționează
```

### C. Validare
- [ ] Se construiește image fără erori
- [ ] Container ruleaza fără crash
- [ ] Aplicația accesibilă pe port 8501
- [ ] Datele se salvează în Supabase

---

## 🚀 Phase 3 - Deployment Test (2-3 ore)

### A. Deploy pe Server Test (ex: Railway, Render)

#### Railway.app (Cel mai ușor)

```bash
# 1. Creează cont railway.app
# 2. Conectează GitHub repo
# 3. Creează proiect nou
# 4. Adaugă variabile de mediu:
#    SUPABASE_URL=...
#    SUPABASE_KEY=...
# 5. Deploy automata de pe main branch
```

#### Render.com (Alternativ)

```bash
# 1. Creează cont render.com
# 2. New → Web Service
# 3. Conectează GitHub
# 4. Alege branch: main
# 5. Build: pip install -r requirements.txt
# 6. Start: streamlit run app/app.py
# 7. Adaugă env vars
# 8. Deploy
```

### B. Post-Deploy Checks
- [ ] Aplicația se încarcă
- [ ] Dashboard funcționează
- [ ] CRUD operations funcționează
- [ ] Nu sunt erori în logs

---

## 📊 Phase 4 - Data Population (4-5 ore)

### A. Adaugă Date Test

```python
# Creează script populate_test_data.py

clients_data = [
    {"name": "Service Moto Chișinău", ...},
    {"name": "Magazin Piese Auto", ...},
    # ... 10-20 clienți
]

for client in clients_data:
    db.table("clients").insert(client).execute()
```

### B. Populate via Supabase UI

- [ ] Accesează Supabase Dashboard
- [ ] Fiecare tabel → Insert
- [ ] Adaugă manual 10-20 înregistrări per tabel

### C. Populate via CSV Import (Future)

```python
# Script pentru importat din CSV
import pandas as pd
df = pd.read_csv("clients.csv")
for _, row in df.iterrows():
    db.table("clients").insert(row.to_dict()).execute()
```

---

## 🎯 Phase 5 - Validare Funcționare (2 ore)

### Dashboard Metrics

- [ ] Profit azi: 0 (OK)
- [ ] Profit luna: 0 (OK)
- [ ] Comenzi în așteptare: N > 0
- [ ] Comenzi expediate: N > 0
- [ ] Profit charts: afișează curba (cu date populate)

### CRUD Operations

- [ ] ✅ Clienți: Create, Read, Update (edit), Delete
- [ ] ✅ Comenzi: Create, Read, Update, Delete
- [ ] ✅ Piese: Create, Read, Search, Update, Delete
- [ ] ✅ Transport: Add to order
- [ ] ✅ Rapoarte: View profit, stats

### Error Handling

- [ ] Submitează form gol → error message
- [ ] Disconnect DB → error message handled
- [ ] Invalid email → validation error
- [ ] Duplicate OEM code → error handled

### Performance

- [ ] Dashboard se încarcă < 3 secunde
- [ ] Lista 100 comenzi se încarcă < 2 secunde
- [ ] Search 1000 piese: instant
- [ ] Nicio timeout

---

## 🔐 Phase 6 - Security Check (1 ora)

- [ ] `.env` NU e în git (verifică .gitignore)
- [ ] Supabase URL și KEY sunt secrete
- [ ] `.git/config` nu conține credențiale
- [ ] Docker image NU conține .env
- [ ] SQL injection: nu poți injecta SQL prin forme

---

## 📝 Phase 7 - Documentation Audit (30 min)

- [ ] README.md e complet și clear
- [ ] SETUP.md are toți pașii
- [ ] ARCHITECTURE.md e detaliat
- [ ] ROADMAP.md e realist
- [ ] Code are comments acolo unde e necesar

---

## 🎓 Phase 8 - Knowledge Transfer (Dacă altcineva va lucra pe proiect)

- [ ] Documentare: Toate pașii pentru setup
- [ ] Code walkthrough: Core components
- [ ] Database schema: Explained relationships
- [ ] Deployment: How to deploy la production
- [ ] Troubleshooting: Common issues & solutions

---

## ✨ Phase 9 - Production Readiness

### Pre-Launch Checklist

- [ ] SSL/HTTPS configured
- [ ] Backups enabled în Supabase
- [ ] Error monitoring set up (ex: Sentry)
- [ ] Uptime monitoring (ex: UptimeRobot)
- [ ] Database performance baseline
- [ ] Load testing done
- [ ] Documentation finalized
- [ ] Support process defined

### Go-Live

- [ ] Deploy to production
- [ ] Smoke test all features
- [ ] Monitor logs for errors
- [ ] Have rollback plan ready
- [ ] Notify users

---

## 🔄 Phase 10 - Continuous Improvement

### Weekly
- [ ] Check error logs
- [ ] Check performance metrics
- [ ] User feedback
- [ ] Bug fixes

### Monthly
- [ ] Feature requests review
- [ ] Roadmap adjustment
- [ ] Security updates
- [ ] Database optimization

### Quarterly
- [ ] Architecture review
- [ ] Scalability assessment
- [ ] Next phase planning

---

## 📞 Troubleshooting Common Issues

### Issue: "Supabase URL and KEY must be set"
**Fix:** 
```bash
# Verifică .env file
cat .env

# Asigură-te că ai copiat valorile corecte
# Restart aplicația după schimbari în .env
```

### Issue: "Connection refused" la Supabase
**Fix:**
```bash
# Verifică internet connection
ping supabase.co

# Verifică firewall
# Verifica dacă Supabase project e activ
```

### Issue: "ModuleNotFoundError: No module named 'supabase'"
**Fix:**
```bash
pip install supabase
# Sau reinstalează din requirements:
pip install -r requirements.txt
```

### Issue: Streamlit crashes random
**Fix:**
```bash
# Check memory:
streamlit run app/app.py --logger.level=debug

# Reduce cache if needed
# Check for infinite loops in code
```

### Issue: Docker image fails to build
**Fix:**
```bash
# Clear docker cache:
docker system prune -a

# Rebuild:
docker build --no-cache -t moto-erp .
```

---

## 🎉 Completion Status

- **Phase 1 MVP:** ✅ DONE
- **Phase 2 Setup:** ✅ DONE
- **Phase 3 Docker:** ⏳ IN PROGRESS
- **Phase 4 Data:** ⏳ PENDING
- **Phase 5 Validation:** ⏳ PENDING
- **Phase 6 Security:** ⏳ PENDING
- **Phase 7 Docs:** ✅ DONE
- **Phase 8 Transfer:** ⏳ PENDING
- **Phase 9 Production:** ⏳ PENDING
- **Phase 10 Continuous:** ⏳ ONGOING

---

**Next Steps:**
1. Setup local environment (Phase 1-2)
2. Populate test data (Phase 4)
3. Run validation tests (Phase 5)
4. Deploy to production (Phase 9)
5. Monitor and iterate (Phase 10)

**Estimated Time:** 8-12 ore pentru setup complet
**Support:** Toate pașii sunt detaliate mai sus

Good luck! 🚀
