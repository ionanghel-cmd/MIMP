import os

# Application Configuration

APP_NAME = os.getenv("APP_NAME", "MotoERP")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Order statuses
ORDER_STATUSES = [
    "cerere",
    "ofertă trimisă",
    "confirmată",
    "comandată la furnizor",
    "în transport",
    "ajunsă",
    "livrată",
    "finalizată",
    "anulată"
]

# Client types
CLIENT_TYPES = ["persoană", "service", "magazin", "dealer"]

# Part categories
PART_CATEGORIES = ["motor", "frâne", "suspensie", "electric", "alt"]

# Expense categories
EXPENSE_CATEGORIES = [
    "internet", "marketing", "transport", "comisioane bancă",
    "combustibil", "ambalaje", "salarii", "alt"
]

# Transport distribution methods
DISTRIBUTION_METHODS = ["greutate", "volum", "egal", "manual"]

# Currency
DEFAULT_CURRENCY = "EUR"
DEFAULT_CURRENCY_SYMBOL = "€"

# Colors for status badges
STATUS_COLORS = {
    "cerere": "🟡",
    "ofertă trimisă": "🟠",
    "confirmată": "🔵",
    "comandată la furnizor": "🟣",
    "în transport": "🚢",
    "ajunsă": "📦",
    "livrată": "🚚",
    "finalizată": "✅",
    "anulată": "❌"
}

# Streamlit page config
PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": "🏍️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
