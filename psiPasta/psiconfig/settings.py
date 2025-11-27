from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ===================================================================
# VARIÁVEIS DE AMBIENTE (Render + Local)
# ===================================================================

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-unsafe")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]


# ===================================================================
# APPS
# ===================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'psiconnect',
    'channels',
]


# ===================================================================
# MIDDLEWARE
# ===================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'psiconfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'psiconfig.wsgi.application'
ASGI_APPLICATION = 'psiconfig.asgi.application'


# ===================================================================
# CHANNELS
# ===================================================================

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


# ===================================================================
# DATABASE — PostgreSQL (Render)
# ===================================================================

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://psiconnect_db_user:6ApFeLL0jgLGkS4GFo1KOlDvZPZb0uIe@dpg-d4k7sgre5dus73f2c3h0-a/psiconnect_db",
        conn_max_age=600,
        ssl_require=True
    )
}


# ===================================================================
# AUTH USER & LOGIN
# ===================================================================

AUTH_USER_MODEL = 'psiconnect.CustomUser'

AUTHENTICATION_BACKENDS = [
    'psiconnect.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/auth/login_paciente/'
LOGIN_REDIRECT_URL = '/auth/inicio_paciente/'
LOGOUT_REDIRECT_URL = '/auth/login_paciente/'


# ===================================================================
# MEDIA
# ===================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ===================================================================
# PASSWORD VALIDATION
# ===================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===================================================================
# INTERNACIONALIZAÇÃO
# ===================================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ===================================================================
# STATIC FILES
# ===================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
