import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# ==========================
# CAMINHO BASE
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def env_list(name: str, default: list[str] | None = None) -> list[str]:
    value = os.getenv(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


# ==========================
# CONFIGURAÇÕES BÁSICAS
# ==========================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-substitua-por-uma-chave-segura")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Mantém comportamento atual, mas permite override por variável de ambiente.
DEBUG = env_bool("DEBUG", default=not bool(RENDER_EXTERNAL_HOSTNAME))

default_hosts = ["localhost", "127.0.0.1"] if DEBUG else [
    "adsjs.com.br",
    "www.adsjs.com.br",
]
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in default_hosts:
    default_hosts.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", default=default_hosts)

# ==========================
# APLICATIVOS
# ==========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "core",
]

# ==========================
# MIDDLEWARE
# ==========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==========================
# ROOT URLCONF
# ==========================
ROOT_URLCONF = "churchmanager.urls"

# ==========================
# TEMPLATES
# ==========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.config",
            ],
        },
    },
]

# ==========================
# WSGI
# ==========================
WSGI_APPLICATION = "churchmanager.wsgi.application"

# ==========================
# BANCO DE DADOS
# ==========================
# Se DATABASE_URL existir (Render), usa Postgres com SSL.
# Caso contrário, usa SQLite (desenvolvimento local).
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,  # força uso de SSL -> evita erros de "SSL connection closed"
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ==========================
# VALIDAÇÃO DE SENHAS
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==========================
# LOCALIZAÇÃO E TEMPO
# ==========================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ==========================
# ARQUIVOS ESTÁTICOS E MÍDIA
# ==========================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
SERVE_MEDIA_IN_PROD = env_bool("SERVE_MEDIA_IN_PROD", default=False)

# WhiteNoise para servir estáticos na Render
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Em produção, habilita proteção padrão recomendada pelo Django.
if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", default=True)
    CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", default=True)
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
    SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", default=True)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    X_FRAME_OPTIONS = "DENY"

    # Mantém flexível para ambiente Render/domínios próprios.
    csrf_origins = env_list("CSRF_TRUSTED_ORIGINS")
    if RENDER_EXTERNAL_HOSTNAME:
        render_origin = f"https://{RENDER_EXTERNAL_HOSTNAME}"
        if render_origin not in csrf_origins:
            csrf_origins.append(render_origin)
    for domain in ("https://adsjs.com.br", "https://www.adsjs.com.br"):
        if domain not in csrf_origins:
            csrf_origins.append(domain)
    CSRF_TRUSTED_ORIGINS = csrf_origins

# ==========================
# LOGIN / LOGOUT
# ==========================
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# ==========================
# PADRÃO DE CHAVE PRIMÁRIA
# ==========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
