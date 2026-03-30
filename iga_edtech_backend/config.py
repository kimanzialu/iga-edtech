import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-me-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30))
    )
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    MAIL_SERVER   = os.getenv("MAIL_SERVER",  "smtp-relay.brevo.com")
    MAIL_PORT     = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS  = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    # Sender must match your verified Brevo account email
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
    MAIL_SUPPRESS_SEND  = os.getenv("MAIL_SUPPRESS_SEND", "False") == "True"
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    OTP_EXPIRES_MINUTES  = int(os.getenv("OTP_EXPIRES_MINUTES",  10))
    MAX_LOGIN_ATTEMPTS   = int(os.getenv("MAX_LOGIN_ATTEMPTS",    5))
    ACCOUNT_LOCK_MINUTES = int(os.getenv("ACCOUNT_LOCK_MINUTES", 30))


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///iga_edtech_dev.db"
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///iga_edtech_dev.db"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)
    MAIL_SUPPRESS_SEND = True


config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "testing":     TestingConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)