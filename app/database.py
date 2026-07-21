import os
import logging
from dotenv import load_dotenv

# Optional imports (don't fail import if not available)
try:
    from supabase import create_client, Client
except Exception:
    create_client = None
    Client = None

try:
    import psycopg2
    from psycopg2.pool import ThreadedConnectionPool
    from psycopg2.extras import RealDictCursor
except Exception:
    psycopg2 = None
    ThreadedConnectionPool = None
    RealDictCursor = None

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# DB fallback vars (for direct Postgres connection)
DB_HOST = os.getenv("SUPABASE_DB_HOST")
DB_NAME = os.getenv("SUPABASE_DB_NAME")
DB_USER = os.getenv("SUPABASE_DB_USER")
DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
DB_PORT = os.getenv("SUPABASE_DB_PORT")

# Clients
_supabase_client = None
_db_pool = None

# Prefer Supabase client when URL+KEY are provided
if SUPABASE_URL and SUPABASE_KEY and create_client:
    try:
        _supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized")
    except Exception as e:
        logger.exception("Failed to initialize Supabase client: %s", e)
        _supabase_client = None

# Fallback: initialize a threaded connection pool to Postgres if DB details provided
if not _supabase_client and DB_HOST and ThreadedConnectionPool is not None:
    try:
        _db_pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            sslmode="require",
        )
        logger.info("Postgres connection pool initialized")
    except Exception as e:
        logger.exception("Failed to initialize Postgres pool: %s", e)
        _db_pool = None

if not _supabase_client and not _db_pool:
    logger.warning(
        "No Supabase client or DB pool initialized. Set SUPABASE_URL+SUPABASE_KEY or DB connection environment variables."
    )

def get_supabase_client():
    """Return a configured Supabase client or None if not available."""
    return _supabase_client

def get_db_conn():
    """Get a connection from the pool. Caller must release it with release_db_conn()."""
    if _db_pool is None:
        raise RuntimeError("Database pool is not initialized")
    conn = _db_pool.getconn()
    return conn

def release_db_conn(conn):
    """Return a connection back to the pool."""
    if _db_pool is None:
        return
    _db_pool.putconn(conn)

def get_db_cursor(conn):
    """Helper to get a RealDictCursor from a connection."""
    if RealDictCursor is None:
        raise RuntimeError("psycopg2 extras are not available")
    return conn.cursor(cursor_factory=RealDictCursor)
