import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from app.managers import ClientManager, OrderManager, PartsManager, FinancialManager

# Page config
st.set_page_config(
    page_title="MotoERP",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            st.dataframe(df_orders, use_container_width=True)
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
            df = pd.DataFrame(clients)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nu sunt clienți")
    
    with tab2:
        st.subheader("Adaugă Client Nou")
        
        with st.form("new_client_form"):
            name = st.text_input("Nume")
            phone = st.text_input("Telefon")
            email = st.text_input("Email")
            city = st.text_input("Oraș")
            country = st.text_input("Țară")
            client_type = st.selectbox("Tip", ["persoană", "service", "magazin", "dealer"])
            discount = st.number_input("Discount %", min_value=0, max_value=100)
            credit_limit = st.number_input("Limita de credit €", min_value=0)
            observations = st.text_area("Observații")
            
            if st.form_submit_button("Salvează Client"):
                client_data = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "city": city,
                    "country": country,
                    "type": client_type,
                    "discount": discount,
                    "credit_limit": credit_limit,
                    "observations": observations,
                    "created_at": datetime.now().isoformat()
                }
                
                result = cm.add_client(client_data)
                if result:
                    st.success("✅ Client adăugat cu succes!")
                else:
                    st.error("❌ Eroare la adăugarea clientului")

def show_orders():
    """Order management page"""
    st.title("📦 Comenzi")
    
    om = OrderManager()
    
    tab1, tab2 = st.tabs(["📋 Lista Comenzi", "➕ Adaugă Comandă"])
    
    with tab1:
        status_filter = st.selectbox(
            "Filtrează după status",
            ["toate", "pending", "confirmed", "shipped", "delivered", "cancelled"]
        )
        
        if status_filter == "toate":
            orders = om.get_all_orders()
        else:
            orders = om.get_orders_by_status(status_filter)
        
        if orders:
            df = pd.DataFrame(orders)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nu sunt comenzi")
    
    with tab2:
        st.subheader("Adaugă Comandă Nouă")
        
        with st.form("new_order_form"):
            client_id = st.text_input("ID Client")
            operator = st.text_input("Operator")
            status = st.selectbox("Status", [
                "cerere", "ofertă trimisă", "confirmată", 
                "comandată la furnizor", "în transport", "ajunsă", 
                "livrată", "finalizată", "anulată"
            ])
            total_amount = st.number_input("Valoare totală €", min_value=0.0)
            profit = st.number_input("Profit €", min_value=0.0)
            observations = st.text_area("Observații")
            
            if st.form_submit_button("Salvează Comandă"):
                order_data = {
                    "client_id": client_id,
                    "operator": operator,
                    "status": status,
                    "total_amount": total_amount,
                    "profit": profit,
                    "observations": observations,
                    "created_at": datetime.now().isoformat()
                }
                
                result = om.add_order(order_data)
                if result:
                    st.success("✅ Comandă adăugată cu succes!")
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
                df = pd.DataFrame(parts)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nu s-au găsit piese")
        else:
            parts = pm.get_all_parts()
            if parts:
                df = pd.DataFrame(parts)
                st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.subheader("Adaugă Piesă Nouă")
        
        with st.form("new_part_form"):
            oem_code = st.text_input("Cod OEM")
            supplier_code = st.text_input("Cod Furnizor")
            brand = st.text_input("Marcă")
            model = st.text_input("Model")
            year = st.text_input("An")
            category = st.selectbox("Categorie", ["motor", "frâne", "suspensie", "electric", "alt"])
            
            supplier_cost = st.number_input("Cost Furnizor €", min_value=0.0)
            transport_cost = st.number_input("Cost Transport €", min_value=0.0)
            sale_price = st.number_input("Preț Vânzare €", min_value=0.0)
            
            if st.form_submit_button("Salvează Piesă"):
                profit = sale_price - (supplier_cost + transport_cost)
                margin = (profit / sale_price * 100) if sale_price > 0 else 0
                
                part_data = {
                    "oem_code": oem_code,
                    "supplier_code": supplier_code,
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "category": category,
                    "supplier_cost": supplier_cost,
                    "transport_cost": transport_cost,
                    "sale_price": sale_price,
                    "profit": profit,
                    "margin": margin,
                    "created_at": datetime.now().isoformat()
                }
                
                result = pm.add_part(part_data)
                if result:
                    st.success("✅ Piesă adăugată cu succes!")
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
