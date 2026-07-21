import sys
import os

# Ensure project root is on sys.path so `import app.*` works when Streamlit runs app/app.py directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from app.managers import ClientManager, OrderManager, PartsManager, FinancialManager
from app.database import get_supabase_client, init_db_pool
# Optional AgGrid for nicer tables
try:
    from st_aggrid import AgGrid, GridOptionsBuilder
    AGGRID_AVAILABLE = True
except Exception:
    AGGRID_AVAILABLE = False


def render_table(df):
    if df is None or (hasattr(df, 'empty') and df.empty):
        st.info('No data')
        return
    if AGGRID_AVAILABLE:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(enabled=True)
        gb.configure_default_column(editable=False, groupable=True, sortable=True, filter=True)
        gridOptions = gb.build()
        AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=False, fit_columns_on_grid_load=True)
    else:
        st.dataframe(df, use_container_width=True)

# Page config
st.set_page_config(
    page_title="MotoERP",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Diagnostics: attempt lazy init and show status in sidebar
try:
    client = get_supabase_client()
    if client is None:
        pool_ok = init_db_pool()
        if pool_ok:
            st.sidebar.success("DB pool initialized (direct Postgres)")
        else:
            st.sidebar.warning("Supabase client and DB pool not initialized. Check Streamlit Secrets for SUPABASE_URL/SUPABASE_KEY or SUPABASE_DB_* variables.")
    else:
        st.sidebar.success("Supabase client initialized")
except Exception as _e:
    # Keep diagnostics non-fatal; show a simple message
    st.sidebar.error(f"Diagnostics: error initializing DB/Supabase: {_e}")

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #0066cc;
    }
    .metric-label {
        font-size: 12px;
        color: #666;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def show_dashboard():
    """Dashboard - Main page"""
    st.title("🏍️ MotoERP - Dashboard")
    
    fm = FinancialManager()
    om = OrderManager()
    cm = ClientManager()
    
    # Get data
    profit_today = fm.get_profit_today()
    profit_month = fm.get_profit_month()
    profit_year = fm.get_profit_year()
    
    orders = om.get_all_orders()
    pending_orders = len(om.get_orders_by_status("pending"))
    shipped_orders = len(om.get_orders_by_status("shipped"))
    delayed_orders = len(om.get_orders_by_status("delayed"))
    
    # KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("💰 Profit Azi", f"€{profit_today:.2f}")
    
    with col2:
        st.metric("💰 Profit Luna", f"€{profit_month:.2f}")
    
    with col3:
        st.metric("💰 Profit An", f"€{profit_year:.2f}")
    
    with col4:
        st.metric("📦 Comenzi Așteptare", pending_orders)
    
    with col5:
        st.metric("🚚 Comenzi Expediate", shipped_orders)
    
    with col6:
        st.metric("❗ Comenzi Întârziate", delayed_orders)
    
    st.divider()
    
    # Charts
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("📊 Comenzi Recente")
        if orders:
            df_orders = pd.DataFrame(orders[:10])
            render_table(df_orders)
        else:
            st.info("Nu sunt comenzi")
    
    with right_col:
        st.subheader("📈 Profit pe Zile")
        # Sample data - will be replaced with real data
        days = pd.date_range(end=datetime.now(), periods=30).tolist()
        profits = [100 + i*5 for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=profits, mode='lines+markers', fill='tozeroy'))
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Second row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💸 Cheltuieli", "€0.00")
    
    with col2:
        st.metric("📈 Încasări", "€0.00")
    
    with col3:
        st.metric("👥 Clienți Noi", "0")
    
    with col4:
        st.metric("❤️ Clienți Recurenți", "0")

def show_clients():
    """Client management page"""
    st.title("👥 Clienți")
    
    cm = ClientManager()
    
    tab1, tab2 = st.tabs(["📋 Lista Clienți", "➕ Adaugă Client"])
    
    with tab1:
        clients = cm.get_all_clients()
        if clients:
            # Render as cards for a nicer frontend
            st.write(f"### Clienți (total: {len(clients)})")
            for c in clients:
                # support RealDictRow and dict
                cid = c.get('id') if isinstance(c, dict) or hasattr(c, 'get') else c['id'] if 'id' in c else None
                name = c.get('name') if isinstance(c, dict) or hasattr(c, 'get') else c.get('name', '')
                phone = c.get('phone', '') if isinstance(c, dict) or hasattr(c, 'get') else c.get('phone', '')
                email = c.get('email', '') if isinstance(c, dict) or hasattr(c, 'get') else c.get('email', '')
                city = c.get('city', '') if isinstance(c, dict) or hasattr(c, 'get') else c.get('city', '')
                with st.container():
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.markdown(f"**{name or 'Nume lipsă'}**  ")
                        st.markdown(f"📞 {phone}  ")
                        st.markdown(f"✉️ {email}  ")
                        st.markdown(f"📍 {city}  ")
                        if c.get('observations'):
                            st.markdown(f"_Obs_: {c.get('observations')}")
                    with col2:
                        if st.button('Vizualizează', key=f'view_{cid}'):
                            st.write(dict(c))
                        if st.button('Șterge', key=f'del_{cid}'):
                            ok = cm.delete_client(cid)
                            if ok:
                                st.experimental_rerun()
            st.divider()
        else:
            st.info("Nu sunt clienți")
    
    with tab2:
        st.subheader("Adaugă Client Nou")
        
        with st.form("new_client_form"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Nume")
                phone = st.text_input("Telefon")
                email = st.text_input("Email")
            with cols[1]:
                city = st.text_input("Oraș")
                country = st.text_input("Țară")
                client_type = st.selectbox("Tip", ["persoană", "service", "magazin", "dealer"])
            discount = st.number_input("Discount %", min_value=0, max_value=100, value=0.0)
            credit_limit = st.number_input("Limita de credit €", min_value=0.0, value=0.0)
            observations = st.text_area("Observații")
            
            if st.form_submit_button("Salvează Client"):
                client_data = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "city": city,
                    "country": country,
                    "type": client_type,
                    "discount_percent": float(discount),
                    "credit_limit": float(credit_limit),
                    "observations": observations,
                    "created_at": datetime.now().isoformat()
                }
                
                result = cm.add_client(client_data)
                st.write('Result (raw):', result)
                if result:
                    st.success("✅ Client adăugat cu succes!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Eroare la adăugarea clientului")

def show_orders():
    """Order management page"""
    st.title("📦 Comenzi")
    
    om = OrderManager()
    cm = ClientManager()
    
    tab1, tab2 = st.tabs(["📋 Lista Comenzi", "➕ Adaugă Comandă"])
    
    with tab1:
        status_filter = st.selectbox(
            "Filtrează după status",
            ["toate", "cerere", "ofertă trimisă", "confirmată", "comandată la furnizor", "în transport", "ajunsă", "livrată", "finalizată", "anulată"], index=0
        )
        
        if status_filter == "toate":
            orders = om.get_all_orders()
        else:
            orders = om.get_orders_by_status(status_filter)
        
        if orders:
            st.write(f"### Comenzi (total: {len(orders)})")
            for o in orders:
                oid = o.get('id') if isinstance(o, dict) or hasattr(o, 'get') else o[0]
                client_name = o.get('client_name') if isinstance(o, dict) else o.get('client_name', '')
                operator = o.get('operator', '') if isinstance(o, dict) else ''
                status = o.get('status', '') if isinstance(o, dict) else ''
                total = o.get('total_amount', 0) if isinstance(o, dict) else ''
                with st.container():
                    c1, c2 = st.columns([3,1])
                    with c1:
                        st.markdown(f"**Comandă {str(oid)[:8]}**  ")
                        st.markdown(f"👤 Client: {client_name}  ")
                        st.markdown(f"🧑‍💼 Operator: {operator}  ")
                        st.markdown(f"📊 Status: {status}  ")
                        st.markdown(f"💶 Total: €{total}")
                    with c2:
                        if st.button('Vizualizează', key=f'view_order_{oid}'):
                            st.write(dict(o))
                        if st.button('Șterge', key=f'del_order_{oid}'):
                            ok = om.delete_order(oid)
                            if ok:
                                st.experimental_rerun()
            st.divider()
        else:
            st.info("Nu sunt comenzi")
    
    with tab2:
        st.subheader("Adaugă Comandă Nouă")
        
        with st.form("new_order_form"):
            # Choose client from existing clients (returns UUID)
            clients = cm.get_all_clients()
            client_map = {}
            client_labels = []
            if clients:
                for i, c in enumerate(clients):
                    cid = c.get('id') if isinstance(c, dict) or hasattr(c, 'get') else c[0]
                    name = c.get('name') if isinstance(c, dict) or hasattr(c, 'get') else str(cid)
                    label = f"{name} — {str(cid)[:8]}"
                    client_map[label] = cid
                    client_labels.append(label)
                client_label = st.selectbox("Client", client_labels)
                client_id = client_map.get(client_label)
            else:
                client_id = st.text_input("ID Client (UUID)")

            cols = st.columns(2)
            with cols[0]:
                operator = st.text_input("Operator")
                status = st.selectbox("Status", [
                    "cerere", "ofertă trimisă", "confirmată", 
                    "comandată la furnizor", "în transport", "ajunsă", 
                    "livrată", "finalizată", "anulată"
                ])
            with cols[1]:
                total_amount = st.number_input("Valoare totală €", min_value=0.0, format="%.2f")
                profit = st.number_input("Profit €", min_value=0.0, format="%.2f")
            observations = st.text_area("Observații")
            
            if st.form_submit_button("Salvează Comandă"):
                order_data = {
                    "client_id": client_id,
                    "operator": operator,
                    "status": status,
                    "total_amount": float(total_amount),
                    "profit": float(profit),
                    "observations": observations,
                    "created_at": datetime.now().isoformat()
                }
                
                result = om.add_order(order_data)
                st.write('Result (raw):', result)
                if result:
                    st.success("✅ Comandă adăugată cu succes!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Eroare la adăugarea comenzii")

def show_parts():
    """Parts management page"""
    st.title("⚙️ Piese")
    
    pm = PartsManager()
    
    tab1, tab2 = st.tabs(["🔍 Caută Piese", "➕ Adaugă Piesă"])
    
    with tab1:
        search_term = st.text_input("Caută după cod OEM")
        
        if search_term:
            parts = pm.search_parts(search_term)
            if parts:
                st.write(f"### Piese găsite: {len(parts)}")
                for p in parts:
                    pid = p.get('id') if isinstance(p, dict) or hasattr(p, 'get') else p[0]
                    oem = p.get('oem_code', '')
                    brand = p.get('brand', '')
                    model = p.get('model', '')
                    price = p.get('sale_price', 0)
                    stock = p.get('stock_quantity', 0)
                    with st.container():
                        c1, c2 = st.columns([3,1])
                        with c1:
                            st.markdown(f"**{oem} — {brand} {model}**")
                            st.markdown(f"💶 Preț: €{price}  ")
                            st.markdown(f"📦 Stoc: {stock}")
                        with c2:
                            if st.button('Vizualizează', key=f'view_part_{pid}'):
                                st.write(dict(p))
                            if st.button('Șterge', key=f'del_part_{pid}'):
                                ok = pm.delete_part(pid)
                                if ok:
                                    st.experimental_rerun()
                st.divider()
            else:
                st.info("Nu s-au găsit piese")
        else:
            parts = pm.get_all_parts()
            if parts:
                st.write(f"### Toate piesele (total: {len(parts)})")
                df = pd.DataFrame(parts)
                render_table(df)
    
    with tab2:
        st.subheader("Adaugă Piesă Nouă")
        
        with st.form("new_part_form"):
            cols = st.columns(2)
            with cols[0]:
                oem_code = st.text_input("Cod OEM")
                supplier_code = st.text_input("Cod Furnizor")
                brand = st.text_input("Marcă")
                model = st.text_input("Model")
            with cols[1]:
                year = st.text_input("An")
                category = st.selectbox("Categorie", ["motor", "frâne", "suspensie", "electric", "alt"])
                stock_quantity = st.number_input("Cantitate în stoc", min_value=0, value=0)
            supplier_cost = st.number_input("Cost Furnizor €", min_value=0.0)
            transport_cost = st.number_input("Cost Transport €", min_value=0.0)
            sale_price = st.number_input("Preț Vânzare €", min_value=0.0)
            
            if st.form_submit_button("Salvează Piesă"):
                profit = float(sale_price) - (float(supplier_cost) + float(transport_cost))
                margin = (profit / float(sale_price) * 100) if float(sale_price) > 0 else 0
                
                part_data = {
                    "oem_code": oem_code,
                    "supplier_code": supplier_code,
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "category": category,
                    "supplier_cost": float(supplier_cost),
                    "transport_cost": float(transport_cost),
                    "sale_price": float(sale_price),
                    "profit": float(profit),
                    "margin_percent": float(margin),
                    "stock_quantity": int(stock_quantity),
                    "created_at": datetime.now().isoformat()
                }
                
                result = pm.add_part(part_data)
                st.write('Result (raw):', result)
                if result:
                    st.success("✅ Piesă adăugată cu succes!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Eroare la adăugarea piesei")

def show_reports():
    """Reports and analytics"""
    st.title("📊 Rapoarte")
    
    fm = FinancialManager()
    
    tab1, tab2, tab3 = st.tabs(["💰 Profit", "📈 Statistici", "📋 KPI"])
    
    with tab1:
        st.subheader("Raport Profit")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Pe Zi", f"€{fm.get_profit_today():.2f}")
        with col2:
            st.metric("Pe Lună", f"€{fm.get_profit_month():.2f}")
        with col3:
            st.metric("Pe An", f"€{fm.get_profit_year():.2f}")
        with col4:
            st.metric("Pe Client", "€0.00")
        with col5:
            st.metric("Pe Marcă", "€0.00")
    
    with tab2:
        st.subheader("Statistici")
        st.info("Statistici vor fi implementate în versiuni viitoare")
    
    with tab3:
        st.subheader("KPI")
        st.info("KPI vor fi implementate în versiuni viitoare")

def main():
    """Main app"""
    st.sidebar.title("🏍️ MotoERP")
    
    page = st.sidebar.radio(
        "Meniu Principal",
        ["Dashboard", "Clienți", "Comenzi", "Piese", "Rapoarte", "Furnizori", "Facturi", "Notificări"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Clienți":
        show_clients()
    elif page == "Comenzi":
        show_orders()
    elif page == "Piese":
        show_parts()
    elif page == "Rapoarte":
        show_reports()
    elif page == "Furnizori":
        st.title("🏢 Furnizori")
        st.info("Secțiunea Furnizori va fi implementată în versiuni viitoare")
    elif page == "Facturi":
        st.title("📄 Facturi")
        st.info("Secțiunea Facturi va fi implementată în versiuni viitoare")
    elif page == "Notificări":
        st.title("🔔 Notificări")
        st.info("Secțiunea Notificări va fi implementată în versiuni viitoare")

if __name__ == "__main__":
    main()
