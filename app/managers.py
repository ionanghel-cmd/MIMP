import streamlit as st
from app.database import get_supabase_client, get_db_conn, get_db_cursor, release_db_conn
from datetime import datetime, timedelta

# Optional dependency: pandas is used for some data transformations in the app UI.
# Import lazily to avoid startup failures if pandas isn't yet installed in the host
# environment (Streamlit will install requirements but this protects early imports).
try:
    import pandas as pd
except Exception:
    pd = None


# Helpers: safe SQL operations that inspect the database schema and only use existing columns.
# This prevents errors like "column X does not exist" when the local DB schema differs.
def _get_table_columns_sql(table_name: str):
    """Return a set of column names for a given table using the DB pool."""
    try:
        conn = get_db_conn()
        cur = get_db_cursor(conn)
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
        rows = cur.fetchall()
        cur.close()
        release_db_conn(conn)
        # rows may be dicts (RealDictCursor) or tuples
        return set([r.get('column_name') if isinstance(r, dict) else r[0] for r in rows])
    except Exception as e:
        # Non-fatal: return empty set to force supabase path or safe failure upstream
        st.error(f"Error fetching table columns for {table_name}: {e}")
        return set()


def _insert_row_sql_safe(table_name: str, data: dict):
    """Insert a row into table_name using only columns that exist in the DB."""
    allowed = _get_table_columns_sql(table_name)
    if not allowed:
        raise RuntimeError(f"Could not determine columns for table {table_name}")
    filtered = {k: v for k, v in data.items() if k in allowed}
    if not filtered:
        raise RuntimeError("No valid columns to insert after filtering by table schema")
    cols = list(filtered.keys())
    vals_placeholders = ["%s"] * len(cols)
    params = [filtered[c] for c in cols]
    sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(vals_placeholders)}) RETURNING *"
    conn = get_db_conn()
    cur = get_db_cursor(conn)
    cur.execute(sql, tuple(params))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    release_db_conn(conn)
    return row


def _update_row_sql_safe(table_name: str, pk_name: str, pk_value, data: dict):
    allowed = _get_table_columns_sql(table_name)
    if not allowed:
        raise RuntimeError(f"Could not determine columns for table {table_name}")
    filtered = {k: v for k, v in data.items() if k in allowed and k != pk_name}
    if not filtered:
        raise RuntimeError("No valid columns to update after filtering by table schema")
    set_parts = [f"{k} = %s" for k in filtered.keys()]
    params = list(filtered.values())
    params.append(pk_value)
    sql = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE {pk_name} = %s RETURNING *"
    conn = get_db_conn()
    cur = get_db_cursor(conn)
    cur.execute(sql, tuple(params))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    release_db_conn(conn)
    return row


class ClientManager:
    def __init__(self):
        self.client = get_supabase_client()

    def _use_supabase(self):
        return self.client is not None

    def get_all_clients(self):
        """Get all clients"""
        if self._use_supabase():
            try:
                response = self.client.table("clients").select("*").execute()
                return response.data or []
            except Exception as e:
                st.error(f"Error fetching clients: {e}")
                return []
        # Fallback to direct SQL
        try:
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT * FROM clients ORDER BY created_at DESC")
            rows = cur.fetchall()
            cur.close()
            release_db_conn(conn)
            return rows
        except Exception as e:
            st.error(f"Error fetching clients (SQL): {e}")
            return []

    def get_client(self, client_id):
        """Get specific client"""
        if self._use_supabase():
            try:
                response = self.client.table("clients").select("*").eq("id", client_id).execute()
                return (response.data[0] if response.data else None)
            except Exception as e:
                st.error(f"Error fetching client: {e}")
                return None
        try:
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
            row = cur.fetchone()
            cur.close()
            release_db_conn(conn)
            return row
        except Exception as e:
            st.error(f"Error fetching client (SQL): {e}")
            return None

    def add_client(self, client_data):
        """Add new client"""
        if self._use_supabase():
            try:
                response = self.client.table("clients").insert(client_data).execute()
                return (response.data[0] if response.data else None)
            except Exception as e:
                st.error(f"Error adding client: {e}")
                return None
        # SQL fallback
        try:
            cols = []
            vals = []
            params = []
            for k, v in client_data.items():
                cols.append(k)
                vals.append('%s')
                params.append(v)
            sql = f"INSERT INTO clients ({', '.join(cols)}) VALUES ({', '.join(vals)}) RETURNING *"
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            conn.commit()
            cur.close()
            release_db_conn(conn)
            return row
        except Exception as e:
            st.error(f"Error adding client (SQL): {e}")
            return None

    def update_client(self, client_id, client_data):
        """Update client"""
        if self._use_supabase():
            try:
                response = self.client.table("clients").update(client_data).eq("id", client_id).execute()
                return (response.data[0] if response.data else None)
            except Exception as e:
                st.error(f"Error updating client: {e}")
                return None
        try:
            set_parts = []
            params = []
            for k, v in client_data.items():
                set_parts.append(f"{k} = %s")
                params.append(v)
            params.append(client_id)
            sql = f"UPDATE clients SET {', '.join(set_parts)} WHERE id = %s RETURNING *"
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            conn.commit()
            cur.close()
            release_db_conn(conn)
            return row
        except Exception as e:
            st.error(f"Error updating client (SQL): {e}")
            return None


class OrderManager:
    def __init__(self):
        self.client = get_supabase_client()

    def _use_supabase(self):
        return self.client is not None

    def get_all_orders(self):
        """Get all orders"""
        if self._use_supabase():
            try:
                response = self.client.table("orders").select("*").order("created_at", desc=True).execute()
                return response.data or []
            except Exception as e:
                st.error(f"Error fetching orders: {e}")
                return []
        try:
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
            rows = cur.fetchall()
            cur.close()
            release_db_conn(conn)
            return rows
        except Exception as e:
            st.error(f"Error fetching orders (SQL): {e}")
            return []

    def get_orders_by_status(self, status):
        """Get orders by status"""
        if self._use_supabase():
            try:
                response = self.client.table("orders").select("*").eq("status", status).execute()
                return response.data or []
            except Exception as e:
                st.error(f"Error fetching orders: {e}")
                return []
        try:
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT * FROM orders WHERE status = %s ORDER BY created_at DESC", (status,))
            rows = cur.fetchall()
            cur.close()
            release_db_conn(conn)
            return rows
        except Exception as e:
            st.error(f"Error fetching orders (SQL): {e}")
            return []

    def add_order(self, order_data):
        """Add new order"""
        if self._use_supabase():
            try:
                response = self.client.table("orders").insert(order_data).execute()
                return (response.data[0] if response.data else None)
            except Exception as e:
                st.error(f"Error adding order: {e}")
                return None
        try:
            cols = []
            vals = []
            params = []
            for k, v in order_data.items():
                cols.append(k)
                vals.append('%s')
                params.append(v)
            sql = f"INSERT INTO orders ({', '.join(cols)}) VALUES ({', '.join(vals)}) RETURNING *"
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            conn.commit()
            cur.close()
            release_db_conn(conn)
            return row
        except Exception as e:
            st.error(f"Error adding order (SQL): {e}")
            return None

    def update_order(self, order_id, order_data):
        """Update order"""
        if self._use_supabase():
            try:
                response = self.client.table("orders").update(order_data).eq("id", order_id).execute()
                return (response.data[0] if response.data else None)
            except Exception as e:
                st.error(f"Error updating order: {e}")
                return None
        try:
            set_parts = []
            params = []
            for k, v in order_data.items():
                set_parts.append(f"{k} = %s")
                params.append(v)
            params.append(order_id)
            sql = f"UPDATE orders SET {', '.join(set_parts)} WHERE id = %s RETURNING *"
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            conn.commit()
            cur.close()
            release_db_conn(conn)
            return row
        except Exception as e:
            st.error(f"Error updating order (SQL): {e}")
            return None


class PartsManager:
    def __init__(self):
        self.client = get_supabase_client()

    def _use_supabase(self):
        return self.client is not None

    def get_all_parts(self):
        """Get all parts"""
        if self._use_supabase():
            try:
                response = self.client.table("parts").select("*").execute()
                return response.data or []
            except Exception as e:
                st.error(f"Error fetching parts: {e}")
                return []
        try:
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT * FROM parts ORDER BY created_at DESC")
            rows = cur.fetchall()
            cur.close()
            release_db_conn(conn)
            return rows
        except Exception as e:
            st.error(f"Error fetching parts (SQL): {e}")
            return []

    def search_parts(self, query):
        """Search parts by OEM code or name"""
        if self._use_supabase():
            try:
                response = self.client.table("parts").select("*").ilike("oem_code", f"%{query}%").execute()
                return response.data or []
            except Exception as e:
                st.error(f"Error searching parts: {e}")
                return []
        try:
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT * FROM parts WHERE oem_code ILIKE %s OR supplier_code ILIKE %s", (f"%{query}%", f"%{query}%"))
            rows = cur.fetchall()
            cur.close()
            release_db_conn(conn)
            return rows
        except Exception as e:
            st.error(f"Error searching parts (SQL): {e}")
            return []

    def add_part(self, part_data):
        """Add new part"""
        if self._use_supabase():
            try:
                response = self.client.table("parts").insert(part_data).execute()
                return (response.data[0] if response.data else None)
            except Exception as e:
                st.error(f"Error adding part: {e}")
                return None
        try:
            cols = []
            vals = []
            params = []
            for k, v in part_data.items():
                cols.append(k)
                vals.append('%s')
                params.append(v)
            sql = f"INSERT INTO parts ({', '.join(cols)}) VALUES ({', '.join(vals)}) RETURNING *"
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            conn.commit()
            cur.close()
            release_db_conn(conn)
            return row
        except Exception as e:
            st.error(f"Error adding part (SQL): {e}")
            return None


class FinancialManager:
    def __init__(self):
        self.client = get_supabase_client()

    def _use_supabase(self):
        return self.client is not None

    def get_profit_today(self):
        """Get profit for today"""
        try:
            today = datetime.now().date()
            if self._use_supabase():
                response = self.client.table("orders").select("profit").gte("created_at", str(today)).execute()
                total = sum([order.get("profit", 0) for order in (response.data or [])])
                return total
            # SQL fallback
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT COALESCE(SUM(profit),0) as total FROM orders WHERE created_at >= %s", (str(today),))
            row = cur.fetchone()
            cur.close()
            release_db_conn(conn)
            return row.get('total', 0) if row else 0
        except Exception:
            return 0

    def get_profit_month(self):
        """Get profit for current month"""
        try:
            now = datetime.now()
            first_day = now.replace(day=1).date()
            if self._use_supabase():
                response = self.client.table("orders").select("profit").gte("created_at", str(first_day)).execute()
                total = sum([order.get("profit", 0) for order in (response.data or [])])
                return total
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT COALESCE(SUM(profit),0) as total FROM orders WHERE created_at >= %s", (str(first_day),))
            row = cur.fetchone()
            cur.close()
            release_db_conn(conn)
            return row.get('total', 0) if row else 0
        except Exception:
            return 0

    def get_profit_year(self):
        """Get profit for current year"""
        try:
            year_start = datetime.now().replace(month=1, day=1).date()
            if self._use_supabase():
                response = self.client.table("orders").select("profit").gte("created_at", str(year_start)).execute()
                total = sum([order.get("profit", 0) for order in (response.data or [])])
                return total
            conn = get_db_conn()
            cur = get_db_cursor(conn)
            cur.execute("SELECT COALESCE(SUM(profit),0) as total FROM orders WHERE created_at >= %s", (str(year_start),))
            row = cur.fetchone()
            cur.close()
            release_db_conn(conn)
            return row.get('total', 0) if row else 0
        except Exception:
            return 0
