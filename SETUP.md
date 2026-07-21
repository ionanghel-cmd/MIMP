# Setup Guide - MotoERP

Ghid complet de configurare și implementare a aplicației MotoERP.

## 📋 Prerequisites

1. **Cont Supabase** - https://supabase.com (gratuit)
2. **Python 3.11+** - https://www.python.org
3. **Git** - https://git-scm.com
4. **Docker** (optional) - https://docker.com

---

## 🔧 Pasul 1: Setup Supabase

### 1.1 Creează cont Supabase
- Mergi pe https://supabase.com
- Sign up cu email
- Creează proiect nou
- Alege regiunea cea mai apropiată

### 1.2 Obține credențialele
- În proiect, accesează **Settings → API**
- Copiază:
  - **Project URL** → `SUPABASE_URL`
  - **anon public** key → `SUPABASE_KEY`

### 1.3 Creează tabelele
- În Supabase, deschide **SQL Editor**
- Click **New Query**
- Copiază și rulează codul din `database/schema.sql`
- Confirmă că s-au creat toate tabelele

---

## 🚀 Pasul 2: Setup Local

### 2.1 Clone repo și configurare

```bash
# Clone repo
git clone <repo-url>
cd moto-erp

# Copiază .env.example la .env
cp .env.example .env

# Editează .env (notepad, VS Code, etc.)
# Adaugă valorile de la Supabase:
# SUPABASE_URL=https://xxxxx.supabase.co
# SUPABASE_KEY=eyJhbGc...
```

### 2.2 Instalare dependințe

```bash
# Creează virtual environment (optional dar recomandat)
python -m venv venv

# Activează venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalează dependințe
pip install -r requirements.txt
```

### 2.3 Rulează aplicația

```bash
streamlit run app/app.py
```

Aplicația se va deschide la http://localhost:8501

---

## 🐳 Pasul 3: Deploy cu Docker (Optional)

### 3.1 Build și run

```bash
# Creează fișier .env în root directory

# Build image
docker build -t moto-erp .

# Run container
docker run -p 8501:8501 \
  --env-file .env \
  moto-erp
```

### 3.2 Sau folosind Docker Compose

```bash
# Asigură-te că .env există

# Run
docker-compose up

# Stop
docker-compose down
```

---

## 🌍 Pasul 4: Deploy pe Server (VPS)

### Opțiunea A: Heroku (Gratuit cu limitări)

```bash
# 1. Instalează Heroku CLI
# 2. Login
heroku login

# 3. Creează app
heroku create moto-erp

# 4. Adaugă variabile de mediu
heroku config:set SUPABASE_URL=<url>
heroku config:set SUPABASE_KEY=<key>

# 5. Deploy
git push heroku main
```

### Opțiunea B: DigitalOcean/Linode (5-10$/lună)

```bash
# 1. Creează VPS (Ubuntu 22.04)
# 2. SSH în server
ssh root@<ip>

# 3. Instalează dependințe
apt update && apt install -y python3 python3-pip git

# 4. Clone repo
git clone <repo-url> /opt/moto-erp
cd /opt/moto-erp

# 5. Instalează dependințe
pip install -r requirements.txt

# 6. Creează .env cu credențialele

# 7. Instalează și configurează Nginx reverse proxy
sudo apt install -y nginx

# 8. Creează systemd service pentru autostart
sudo nano /etc/systemd/system/moto-erp.service
```

### Exemplu systemd service:

```ini
[Unit]
Description=MotoERP Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/moto-erp
Environment="PATH=/opt/moto-erp/venv/bin"
ExecStart=/opt/moto-erp/venv/bin/streamlit run app/app.py --server.port=8000 --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start moto-erp
sudo systemctl enable moto-erp
```

---

## 🔐 Configurare Nginx (Reverse Proxy)

```nginx
# /etc/nginx/sites-available/moto-erp

server {
    listen 80;
    server_name moto-erp.com www.moto-erp.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Activează site
sudo ln -s /etc/nginx/sites-available/moto-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📱 Testare și Validare

### 1. Verifică Dashboard
- [ ] Accesează http://localhost:8501
- [ ] Vezi KPI cards
- [ ] Charts se încarcă corect

### 2. Testează CRUD Operații
- [ ] Adaugă client test
- [ ] Adaugă comandă test
- [ ] Adaugă piesă test
- [ ] Verifică în Supabase că datele s-au salvat

### 3. Verifică Rapoarte
- [ ] Dashboard se actualizează
- [ ] Profit calculations sunt corecte

---

## 🛠️ Troubleshooting

### Error: "Supabase URL and KEY must be set"
**Soluție:** Verifică că .env are valorile corecte și aplicația a fost restartată

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Soluție:** Rulează `pip install -r requirements.txt`

### Error: "Connection refused" la Supabase
**Soluție:** 
- Verifică URL-ul Supabase
- Verifică internet connection
- Verifică firewall settings

### Streamlit nu se încarcă
**Soluție:** Deschide http://localhost:8501 în browser

---

## 🚀 Faza 2 - Funcții Avansate

După ce MVP funcționează, implementează:

1. **Autentificare JWT**
   - Login/Register
   - Roluri: Admin, Operator, Contabil

2. **Notificări Email**
   - Comandă importantă
   - Follow-up automat
   - Rapoarte zilnice

3. **AI Features**
   - VIN parser pentru recomandări
   - Smart pricing
   - Predictive analytics

4. **API REST**
   - FastAPI backend
   - Integrări externe
   - Mobile app

---

## 📞 Support

Pentru probleme:
1. Verifică logs: `docker logs moto-erp` sau `streamlit logs`
2. Consulta documentația: https://streamlit.io, https://supabase.com
3. Contactează echipa

---

## 🎯 Next Steps

1. ✅ Setup local și test
2. Populate cu date test
3. Configurare furnizori și clienți reali
4. Deploy pe server
5. Integrare cu email/SMS
6. Training utilizatori
7. Faza 2 features

Good luck! 🚀
