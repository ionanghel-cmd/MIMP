import streamlit as st
from datetime import datetime, timedelta
from app.managers import OrderManager, ClientManager, FinancialManager
import pandas as pd

def get_order_count_by_status():
    """Get count of orders by status"""
    om = OrderManager()
    orders = om.get_all_orders()
    
    status_counts = {}
    for order in orders:
        status = order.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return status_counts

def get_top_clients(limit=10):
    """Get top clients by purchases"""
    cm = ClientManager()
    clients = cm.get_all_clients()
    
    # Sort by total_purchases
    sorted_clients = sorted(
        clients, 
        key=lambda x: x.get('total_purchases', 0), 
        reverse=True
    )
    
    return sorted_clients[:limit]

def get_delayed_orders():
    """Get orders that are delayed"""
    om = OrderManager()
    orders = om.get_all_orders()
    
    delayed = [
        o for o in orders 
        if o.get('status') in ['în transport', 'comandată la furnizor']
    ]
    
    # Filter by date - older than 7 days
    delayed_old = [
        o for o in delayed 
        if o.get('created_at') and (
            datetime.now() - datetime.fromisoformat(o['created_at'])
        ).days > 7
    ]
    
    return delayed_old

def format_currency(value):
    """Format value as currency"""
    return f"€{value:,.2f}"

def calculate_margin(cost, price):
    """Calculate profit margin percentage"""
    if price == 0:
        return 0
    return ((price - cost) / price) * 100

def get_date_range(range_type='month'):
    """Get date range for reports"""
    today = datetime.now().date()
    
    if range_type == 'day':
        start = today
        end = today
    elif range_type == 'week':
        start = today - timedelta(days=today.weekday())
        end = today
    elif range_type == 'month':
        start = today.replace(day=1)
        end = today
    elif range_type == 'year':
        start = today.replace(month=1, day=1)
        end = today
    else:
        start = today - timedelta(days=30)
        end = today
    
    return start, end
