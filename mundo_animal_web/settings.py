"""
Django settings for mundo_animal_web project.
Configuración lista para local y Docker (producción).
"""

from pathlib import Path
import os

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

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,0.0.0.0'
).split(',')

CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
]


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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← para archivos estáticos
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
# BASE DE DATOS
# ==========================================================
# En local → SQLite (por defecto)
# En Docker → PostgreSQL (via variables de entorno)
# ==========================================================
if os.environ.get('DATABASE_URL'):
    # Modo Docker / producción con PostgreSQL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Modo local con SQLite
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
STATIC_ROOT = BASE_DIR / 'staticfiles'   # ← donde collectstatic guarda todo

# WhiteNoise comprime y cachea los estáticos en producción
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
# SEGURIDAD EXTRA EN PRODUCCIÓN (solo si DEBUG=False)
# ==========================================================
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = False   # poner True si usas HTTPS
    CSRF_COOKIE_SECURE = False      # poner True si usas HTTPS
    SECURE_SSL_REDIRECT = False     # poner True si usas HTTPS