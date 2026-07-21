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

# Clients (lazy-initialized)
_supabase_client = None
_db_pool = None


def init_supabase_client() -> bool:
    """Attempt to initialize the Supabase client. Returns True on success."""
    global _supabase_client
    if _supabase_client is not None:
        return True
    if not (SUPABASE_URL and SUPABASE_KEY and create_client):
        logger.debug("Supabase URL/KEY or create_client not available")
        return False
    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized")
        return True
    except Exception as e:
        logger.exception("Failed to initialize Supabase client: %s", e)
        _supabase_client = None
        return False


def init_db_pool() -> bool:
    """Attempt to initialize a threaded Postgres connection pool. Returns True on success."""
    global _db_pool
    if _db_pool is not None:
        return True
    if ThreadedConnectionPool is None:
        logger.debug("psycopg2 ThreadedConnectionPool not available in environment")
        return False
    if not DB_HOST:
        logger.debug("DB_HOST not provided; skipping pool init")
        return False
    try:
        port = int(DB_PORT) if DB_PORT else 5432
        _db_pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=port,
            sslmode="require",
        )
        logger.info("Postgres connection pool initialized")
        return True
    except Exception as e:
        logger.exception("Failed to initialize Postgres pool: %s", e)
        _db_pool = None
        return False


def get_supabase_client():
    """Return a configured Supabase client or None if not available."""
    if _supabase_client is None:
        init_supabase_client()
    return _supabase_client


def get_db_conn():
    """Get a connection from the pool. Caller must release it with release_db_conn()."""
    if _db_pool is None:
        ok = init_db_pool()
        if not ok:
            raise RuntimeError(
                "Database pool is not initialized. Check SUPABASE_DB_* secrets or SUPABASE_URL/SUPABASE_KEY."
            )
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
