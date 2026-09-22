"""
Django settings for mundo_animal_web project.
Configuración lista para local, Docker y Render (producción).
"""

import os
from pathlib import Path

# ==========================================================
# RUTAS BASE
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# SEGURIDAD
# ==========================================================
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-cambia-esta-clave-en-produccion-2026'
)

# DEBUG=True en local, False en producción (Render/Docker)
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'


# ==========================================================
# ALLOWED_HOSTS (funciona en local, Docker y Render)
# ==========================================================
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Render inyecta automáticamente esta variable con tu dominio
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Aceptar cualquier subdominio de onrender.com
ALLOWED_HOSTS.append('.onrender.com')

# También lee la variable ALLOWED_HOSTS si la defines manualmente
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
if env_hosts:
    for h in env_hosts.split(','):
        h = h.strip()
        if h and h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h)


# ==========================================================
# CSRF TRUSTED ORIGINS (necesario para formularios)
# ==========================================================
CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

CSRF_TRUSTED_ORIGINS.append('https://*.onrender.com')


# ==========================================================
# APLICACIONES
# ==========================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tienda',  # ← nuestra app
]


# ==========================================================
# MIDDLEWARE
# ==========================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← sirve estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================================
# URLS Y WSGI
# ==========================================================
ROOT_URLCONF = 'mundo_animal_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mundo_animal_web.wsgi.application'


# ==========================================================
# BASE DE DATOS (SQLite en local, PostgreSQL en Docker/Render)
# ==========================================================
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Docker / Render → PostgreSQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local → SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==========================================================
# VALIDACIÓN DE CONTRASEÑAS
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================================
# INTERNACIONALIZACIÓN
# ==========================================================
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# ==========================================================
# ARCHIVOS ESTÁTICOS
# ==========================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ==========================================================
# CONFIGURACIÓN POR DEFECTO
# ==========================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# SEGURIDAD EXTRA EN PRODUCCIÓN
# ==========================================================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # Render maneja HTTPS a nivel de proxy, así que estas quedan en False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False