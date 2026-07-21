import streamlit as st
from app.database import get_supabase_client
from datetime import datetime, timedelta

# Optional dependency: pandas is used for some data transformations in the app UI.
# Import lazily to avoid startup failures if pandas isn't yet installed in the host
# environment (Streamlit will install requirements but this protects early imports).
try:
    import pandas as pd
except Exception:
    pd = None

class ClientManager:
    def __init__(self):
        self.db = get_supabase_client()
    
    def get_all_clients(self):
        """Get all clients"""
        try:
            response = self.db.table("clients").select("*").execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching clients: {e}")
            return []
    
    def get_client(self, client_id):
        """Get specific client"""
        try:
            response = self.db.table("clients").select("*").eq("id", client_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error fetching client: {e}")
            return None
    
    def add_client(self, client_data):
        """Add new client"""
        try:
            response = self.db.table("clients").insert(client_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error adding client: {e}")
            return None
    
    def update_client(self, client_id, client_data):
        """Update client"""
        try:
            response = self.db.table("clients").update(client_data).eq("id", client_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error updating client: {e}")
            return None

class OrderManager:
    def __init__(self):
        self.db = get_supabase_client()
    
    def get_all_orders(self):
        """Get all orders"""
        try:
            response = self.db.table("orders").select("*").order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching orders: {e}")
            return []
    
    def get_orders_by_status(self, status):
        """Get orders by status"""
        try:
            response = self.db.table("orders").select("*").eq("status", status).execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching orders: {e}")
            return []
    
    def add_order(self, order_data):
        """Add new order"""
        try:
            response = self.db.table("orders").insert(order_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error adding order: {e}")
            return None
    
    def update_order(self, order_id, order_data):
        """Update order"""
        try:
            response = self.db.table("orders").update(order_data).eq("id", order_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error updating order: {e}")
            return None

class PartsManager:
    def __init__(self):
        self.db = get_supabase_client()
    
    def get_all_parts(self):
        """Get all parts"""
        try:
            response = self.db.table("parts").select("*").execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching parts: {e}")
            return []
    
    def search_parts(self, query):
        """Search parts by OEM code or name"""
        try:
            response = self.db.table("parts").select("*").ilike("oem_code", f"%{query}%").execute()
            return response.data
        except Exception as e:
            st.error(f"Error searching parts: {e}")
            return []
    
    def add_part(self, part_data):
        """Add new part"""
        try:
            response = self.db.table("parts").insert(part_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error adding part: {e}")
            return None

class FinancialManager:
    def __init__(self):
        self.db = get_supabase_client()
    
    def get_profit_today(self):
        """Get profit for today"""
        try:
            today = datetime.now().date()
            response = self.db.table("orders").select("profit").gte("created_at", str(today)).execute()
            total = sum([order.get("profit", 0) for order in response.data])
            return total
        except Exception as e:
            return 0
    
    def get_profit_month(self):
        """Get profit for current month"""
        try:
            now = datetime.now()
            first_day = now.replace(day=1).date()
            response = self.db.table("orders").select("profit").gte("created_at", str(first_day)).execute()
            total = sum([order.get("profit", 0) for order in response.data])
            return total
        except Exception as e:
            return 0
    
    def get_profit_year(self):
        """Get profit for current year"""
        try:
            year_start = datetime.now().replace(month=1, day=1).date()
            response = self.db.table("orders").select("profit").gte("created_at", str(year_start)).execute()
            total = sum([order.get("profit", 0) for order in response.data])
            return total
        except Exception as e:
            return 0
