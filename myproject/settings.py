from pathlib import Path
import os
import dj_database_url
import pymysql

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECRET KEY
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')

# 🔧 DEBUG
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# 📦 Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'myapp',
]

# ⚙️ Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

# 🧾 Templates
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

WSGI_APPLICATION = 'myproject.wsgi.application'

# 🗄️ DATABASE (FINAL FIX ✅)
db_url = os.environ.get("DATABASE_URL", "postgresql://postgres.taewjreakljsmdmfzaqt:Saikumar278@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres")

# If a stale MySQL URL is found in local environment variables, override it
if db_url and db_url.startswith("mysql://"):
    db_url = "postgresql://postgres.taewjreakljsmdmfzaqt:Saikumar278@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"

if db_url:
    # Fix bytes issue
    if isinstance(db_url, bytes):
        db_url = db_url.decode("utf-8")

    # ✅ PostgreSQL (Supabase)
    DATABASES = {
        "default": dj_database_url.parse(
            db_url,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # ✅ SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# 🔐 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📁 Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 🔥 WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 📁 Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🆔 Default PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🌐 CORS & CSRF
CORS_ALLOWED_ORIGINS = [
    "https://brolichi.com",
    "https://www.brolichi.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "https://brolichi.com",
    "https://www.brolichi.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# 🔒 Security (Production only)
if os.environ.get('PRODUCTION') == 'True':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_AGE = 3600