# MotoERP - Architecture Document

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER (Streamlit)                   │
│  - Dashboard                                                     │
│  - Clients Module                                                │
│  - Orders Module                                                 │
│  - Parts Module                                                  │
│  - Reports Module                                                │
│  - Settings                                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                           │
│  - ClientManager                                                 │
│  - OrderManager                                                  │
│  - PartsManager                                                  │
│  - FinancialManager                                              │
│  - TransportManager (future)                                    │
│  - NotificationManager (future)                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    DATA ACCESS LAYER                             │
│  - Database module (Supabase client)                             │
│  - Query builders                                                │
│  - Cache layer (future)                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              PERSISTENCE LAYER (Supabase/PostgreSQL)             │
│  - clients table                                                 │
│  - orders table                                                  │
│  - parts table                                                   │
│  - suppliers table                                               │
│  - transport table                                               │
│  - invoices table                                                │
│  - expenses table                                                │
│  - price_history table                                           │
│  - wishlist table                                                │
│  - notifications table                                           │
│  - blacklist table                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Project Structure

```
moto-erp/
├── app/
│   ├── __init__.py                 # Package initialization
│   ├── app.py                      # Main Streamlit application
│   ├── database.py                 # Supabase connection
│   ├── managers.py                 # Business logic classes
│   ├── utils.py                    # Utility functions
│   ├── config.py                   # Configuration constants
│   └── pages/                      # (Future) Streamlit pages
│       ├── dashboard.py
│       ├── clients.py
│       ├── orders.py
│       └── reports.py
├── database/
│   └── schema.sql                  # PostgreSQL schema
├── tests/                          # (Future) Unit tests
│   ├── test_managers.py
│   └── test_utils.py
├── docker/                         # Docker files
│   └── Dockerfile
├── docs/                           # Documentation
│   ├── API.md
│   ├── DATABASE.md
│   └── FEATURES.md
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Docker compose config
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project README
├── SETUP.md                        # Setup guide
├── ARCHITECTURE.md                 # This file
└── ROADMAP.md                      # Development roadmap
```

---

## 🔄 Data Flow

### Order Processing Flow

```
1. Client Request
   ↓
2. Create Order (status: "cerere")
   ↓
3. Add Parts to Order
   ↓
4. Generate Quote (status: "ofertă trimisă")
   ↓
5. Client Confirms (status: "confirmată")
   ↓
6. Order to Supplier (status: "comandată la furnizor")
   ↓
7. In Transport (status: "în transport")
   ↓
8. Arrived (status: "ajunsă")
   ↓
9. Delivered (status: "livrată")
   ↓
10. Finalize (status: "finalizată")
    - Create Client Invoice
    - Record Profit
    - Update Client Stats
```

---

## 💾 Database Design

### Key Relationships

```
clients ──────┐
              ├──→ orders ──────┐
              │                 ├──→ order_items ──→ parts
              │                 ├──→ invoices
              │                 └──→ transport
              │
              ├──→ wishlist ────→ parts
              └──→ blacklist

suppliers ────→ transport
parts ────────→ price_history
```

### Query Patterns

**Get Order with Client & Parts**
```sql
SELECT o.*, c.name, c.email, oi.quantity, p.oem_code
FROM orders o
JOIN clients c ON o.client_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN parts p ON oi.part_id = p.id
WHERE o.id = ?
```

**Get Financial Summary**
```sql
SELECT 
  SUM(profit) as total_profit,
  COUNT(*) as order_count,
  AVG(profit) as avg_profit
FROM orders
WHERE status = 'finalizată'
AND created_at >= ?
```

---

## 🔐 Security Considerations

### Current State (MVP)
- No authentication
- Local environment variables
- Supabase RLS disabled

### Phase 2
- [ ] JWT-based authentication
- [ ] Role-based access control (RBAC)
- [ ] Enable Supabase RLS
- [ ] Input validation
- [ ] SQL injection prevention (via ORM)
- [ ] HTTPS enforcement
- [ ] Rate limiting

### Phase 3+
- [ ] Two-factor authentication
- [ ] Audit logging
- [ ] Data encryption at rest
- [ ] API key management

---

## 🚀 Performance Optimization

### Current
- Basic Supabase queries
- No caching
- No indexing (except schema)

### Phase 2
- [ ] Redis cache for frequently accessed data
- [ ] Query result caching
- [ ] Database connection pooling
- [ ] Pagination for large datasets

### Phase 3
- [ ] ElasticSearch for search optimization
- [ ] CDN for static assets
- [ ] Database partitioning (by date)

---

## 🔌 API Future State

```python
# FastAPI Backend (Phase 2)
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(title="MotoERP API")

@app.get("/api/v1/clients/{client_id}")
async def get_client(client_id: str, token: str = Depends(verify_token)):
    return {...}

@app.post("/api/v1/orders")
async def create_order(order: OrderSchema, token: str = Depends(verify_token)):
    return {...}

@app.get("/api/v1/reports/profit")
async def get_profit_report(period: str, token: str = Depends(verify_token)):
    return {...}
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
# test_managers.py
def test_add_client():
    manager = ClientManager()
    client_data = {...}
    result = manager.add_client(client_data)
    assert result is not None
```

### Integration Tests
```python
# test_integration.py
def test_order_workflow():
    # Create client
    # Create order
    # Add parts
    # Generate invoice
    # Verify profit calculation
```

### E2E Tests
```python
# Streamlit tests using streamlit.testing.v1
def test_dashboard_loads():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file("app/app.py")
    at.run()
    assert "MotoERP" in at.title
```

---

## 📈 Scalability Path

### Stage 1: MVP (Current)
- Single Streamlit server
- Supabase managed DB
- ~100 users

### Stage 2: Multi-tier
- FastAPI backend API
- React/Vue frontend
- Redis cache
- Load balancer
- ~1000 users

### Stage 3: Distributed
- Microservices (notifications, analytics, AI)
- Message queue (RabbitMQ/Kafka)
- Data warehouse (BigQuery/Redshift)
- CDN for static assets
- ~10,000 users

### Stage 4: SaaS
- Multi-tenant architecture
- Kubernetes orchestration
- Advanced analytics
- AI/ML features
- Unlimited users

---

## 🔄 Deployment Strategy

### Development
```bash
streamlit run app/app.py --logger.level=debug
```

### Staging
```bash
docker-compose -f docker-compose.staging.yml up
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
# With automatic backups, monitoring, alerts
```

---

## 📊 Monitoring & Analytics

### Metrics to Track (Future)
- Active users
- Order processing time
- Error rates
- API response times
- Database query performance
- User engagement

### Logging Strategy
- Application logs → stdout
- Error tracking → Sentry
- User actions → Analytics service
- Audit trail → Database

---

## 🎓 Development Workflow

1. **Feature Planning** → Write issue/spec
2. **Implementation** → Create branch
3. **Testing** → Unit + Integration tests
4. **Review** → Code review
5. **Merge** → To main branch
6. **Deploy** → Automated CI/CD

---

## 🔗 Technologies Summary

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Streamlit | Rapid development, built-in widgets |
| Backend (Phase 2) | FastAPI | Modern, fast, async, great for APIs |
| Database | PostgreSQL | Reliable, powerful, great for business logic |
| Database Layer | Supabase | Managed, includes auth, real-time |
| Caching (Phase 2) | Redis | Fast, in-memory, perfect for cache |
| Search (Phase 3) | ElasticSearch | Full-text search, analytics |
| Deployment | Docker | Containerization, consistency |
| Orchestration (Phase 3) | Kubernetes | Scalable, resilient |

---

## 📚 References

- Streamlit: https://streamlit.io/docs
- Supabase: https://supabase.com/docs
- PostgreSQL: https://www.postgresql.org/docs
- FastAPI: https://fastapi.tiangolo.com
- Docker: https://docs.docker.com

---

**Last Updated:** 2026-07-21
**Version:** 0.1.0
