import os
from pathlib import Path
import dj_database_url

# ==========================
# CAMINHO BASE
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# CONFIGURAÇÕES BÁSICAS
# ==========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-substitua-por-uma-chave-segura')

# Detecta automaticamente se está em modo local ou Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    DEBUG = False
    ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'adsjs.onrender.com',
    'adsjs.com.br',
    'www.adsjs.com.br',
]
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# ==========================
# APLICATIVOS
# ==========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # ✅ Necessário para o template humanize
    'core',
]

# ==========================
# MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================
# ROOT URLCONF
# ==========================
ROOT_URLCONF = 'churchmanager.urls'

# ==========================
# TEMPLATES
# ==========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Templates globais (opcional)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.config',  # ✅ seu context processor
            ],
        },
    },
]

# ==========================
# WSGI
# ==========================
WSGI_APPLICATION = 'churchmanager.wsgi.application'

# ==========================
# BANCO DE DADOS
# ==========================
if RENDER_EXTERNAL_HOSTNAME:
    # Render — usa variável DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
            conn_max_age=600
        )
    }
else:
    # Ambiente local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==========================
# VALIDAÇÃO DE SENHAS
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================
# LOCALIZAÇÃO E TEMPO
# ==========================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ==========================
# ARQUIVOS ESTÁTICOS E MÍDIA
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# WhiteNoise para o Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==========================
# LOGIN / LOGOUT
# ==========================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ==========================
# PADRÃO DE CHAVE PRIMÁRIA
# ==========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
