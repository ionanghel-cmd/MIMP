import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configurația de bază a aplicației
    """

    # Flask
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "CHANGE_ME_WITH_RANDOM_SECRET"
    )

    DEBUG = False

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # PostgreSQL (opțional - pentru conexiune directă)
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        if DB_HOST
        else None
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    UPLOAD_FOLDER = "uploads"

    ALLOWED_EXTENSIONS = {
        "xlsx",
        "xls",
        "csv",
        "pdf",
        "png",
        "jpg",
        "jpeg"
    }

    # Pagination
    DEFAULT_PAGE_SIZE = 25

    # Session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"

    # ERP
    COMPANY_NAME = "MotoERP"

    DEFAULT_CURRENCY = "EUR"

    DEFAULT_LANGUAGE = "ro"


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False

    SESSION_COOKIE_SECURE = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
