# 🚀 MotoERP - QUICK START (5 Minute Setup)

## 1️⃣ **Supabase Setup (2 minute)**

### A. Create Supabase Project
1. Go to https://supabase.com
2. Click **New Project**
3. Name: `moto-erp`
4. Region: Europe (choose nearest)
5. Click **Create**

### B. Get Credentials
1. Go to **Settings → API**
2. Copy **Project URL** 
3. Copy **anon public** key
4. Keep them safe

### C. Create Database Schema
1. In Supabase, go to **SQL Editor**
2. Click **New Query**
3. Copy ALL content from `database/schema.sql`
4. Paste into query window
5. Click **Run**
6. ✅ All 13 tables created!

---

## 2️⃣ **Local Setup (2 minute)**

### Windows Users
```bash
# Double-click to run:
quick-start.bat
```

### Mac/Linux Users
```bash
# Run script:
chmod +x quick-start.sh
./quick-start.sh
```

### Manual Setup (Any OS)
```bash
# 1. Copy .env template
cp .env.example .env

# 2. Edit .env - add your Supabase credentials:
#    SUPABASE_URL=https://xxxxx.supabase.co
#    SUPABASE_KEY=eyJhbGc...

# 3. Create virtual environment
python -m venv venv

# 4. Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

---

## 3️⃣ **Run Application (1 minute)**

```bash
streamlit run app/app.py
```

✅ App opens at: **http://localhost:8501**

---

## ✨ **First Steps**

1. Click **Clienți** in sidebar
2. Click **Adaugă Client**
3. Fill form with test data:
   ```
   Nume: Test Client
   Telefon: 0700000000
   Email: test@example.com
   Oraș: București
   Țară: România
   Tip: magazin
   Discount: 5%
   Credit limit: 5000€
   ```
4. Click **Salvează Client** ✅
5. Go back to **Dashboard** - see it update!
6. Try **Comenzi** → Add order
7. Try **Piese** → Add part

---

## 🐳 **Docker (Optional - 1 minute)**

### With Docker Compose:
```bash
docker-compose up
```
✅ App at: http://localhost:8501

### Manual Docker:
```bash
docker build -t moto-erp .
docker run -p 8501:8501 --env-file .env moto-erp
```

---

## 🚀 **Deploy to Cloud (5 minutes)**

### Option A: Railway.app (Easiest)
1. Go to https://railway.app
2. Create account
3. Create new project
4. Click **GitHub** → Connect repo
5. Deploy
6. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
7. Done! ✅

### Option B: Render.com
1. Go to https://render.com
2. Create account
3. New → Web Service
4. Connect GitHub
5. Name: `moto-erp`
6. Build command: (leave empty)
7. Start command: `streamlit run app/app.py`
8. Add environment variables
9. Deploy ✅

---

## 📊 **File Structure**

```
moto-erp/
├── app/                          # Main application
│   ├── app.py                   # Streamlit app
│   ├── database.py              # Supabase connection
│   ├── managers.py              # Business logic
│   ├── config.py                # Configuration
│   └── utils.py                 # Utilities
├── database/
│   └── schema.sql               # 13 database tables
├── requirements.txt             # Python packages
├── .env.example                 # Template for secrets
├── quick-start.bat/sh           # Auto setup
├── docker-compose.yml           # Docker config
├── Dockerfile                   # Container definition
├── README.md                    # Full documentation
├── SETUP.md                     # Detailed setup
├── ARCHITECTURE.md              # System design
├── ROADMAP.md                   # Development plan
└── IMPLEMENTATION_CHECKLIST.md  # Validation steps
```

---

## ⚠️ **Troubleshooting**

### Error: "Supabase URL and KEY must be set"
✅ **Fix:** Edit `.env` with correct values and restart app

### Error: "ModuleNotFoundError: No module named 'streamlit'"
✅ **Fix:** Run `pip install -r requirements.txt`

### Error: "Connection refused" from Supabase
✅ **Fix:** Check internet connection and .env URL is correct

### Port 8501 already in use
✅ **Fix:** `streamlit run app/app.py --server.port 8502`

---

## 🎯 **What's Included**

✅ **Complete Streamlit App** with 8 modules
✅ **13 Database Tables** pre-designed
✅ **Business Logic** (Client, Order, Parts, Financial managers)
✅ **Docker Ready** for production
✅ **Full Documentation** (4 guides + roadmap)
✅ **Quick Start Scripts** for Windows/Mac/Linux

---

## 📚 **Documentation**

| Document | Purpose |
|----------|---------|
| **README.md** | Overview & features |
| **SETUP.md** | Detailed installation & deployment |
| **ARCHITECTURE.md** | System design & patterns |
| **ROADMAP.md** | 4-phase development plan |
| **IMPLEMENTATION_CHECKLIST.md** | Validation & testing |

---

## 🔐 **Features Included**

### Dashboard
- 💰 Profit tracking (today, month, year)
- 📦 Order status overview
- 📊 Charts and KPIs
- 📈 Recent orders list

### Clients Module
- ➕ Add/Edit/Delete clients
- 🏷️ Client types (person, service, shop, dealer)
- 💳 Discounts & credit limits
- 📋 Client search

### Orders Module
- ➕ Create orders with 9 statuses
- 📊 Filter by status
- 💰 Automatic profit calculation
- 🔍 Order details view

### Parts Module
- ➕ Add OEM parts
- 🔍 Search by code
- 💵 Cost & pricing
- 📈 Profit margins

### Reports Module
- 💰 Profit by period
- 📊 Financial analytics
- 🔍 KPI tracking

---

## 💡 **Next: Phase 2 Features**

After MVP is running:
- 🔐 Authentication (JWT)
- 🤖 AI recommendations
- 📧 Email notifications
- 📅 Calendar & scheduling
- 🔌 API integrations

See **ROADMAP.md** for full plan!

---

## 🎉 **You're Ready!**

```bash
# 3 commands to start:
1. cp .env.example .env          # Copy template
2. pip install -r requirements.txt  # Install packages
3. streamlit run app/app.py      # Run app
```

**Questions?** Check:
- SETUP.md for detailed steps
- ARCHITECTURE.md for system design
- Code comments in app/*.py

**Happy building! 🚀**
