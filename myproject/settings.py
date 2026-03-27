# from pathlib import Path
# import os
# import pymysql

# pymysql.install_as_MySQLdb()

# BASE_DIR = Path(__file__).resolve().parent.parent

# # ✅ SECRET KEY (from Render env)
# SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')

# # ✅ DEBUG OFF in production
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS = ['*']

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'corsheaders',
#     'myapp'
# ]

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # moved up
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'myproject.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'myproject.wsgi.application'

# # ⚠️ IMPORTANT: Use environment variables
# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.mysql',
# #         'NAME': os.environ.get('DB_NAME'),
# #         'USER': os.environ.get('DB_USER'),
# #         'PASSWORD': os.environ.get('DB_PASSWORD'),
# #         'HOST': os.environ.get('DB_HOST'),
# #         'PORT': '3306',
# #     }
# # }

# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.mysql',
# #         'NAME': 'Brolichi',
# #         'USER': 'root',
# #         'PASSWORD': 'Saikumar278',
# #         'HOST': 'localhost',
# #         'PORT': '3306',
# #     }
# # }
# import dj_database_url

# DATABASES = {
#     'default': dj_database_url.parse(
#         "postgresql://postgres.taewjreakljsmdmfzaqt:Saikumar278@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres"
#     )
# }

# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS_ALLOW_ALL_ORIGINS = True

# # Triggering auto-reload for WhiteNoise to find the new logo

# # --- SECURITY IMPROVEMENTS ---
# # Only applied in production on Render (set PRODUCTION=True env var on Render dashboard).
# # NOT applied locally even if DEBUG is False, to avoid HTTPS timeout issues during development.
# if os.environ.get('PRODUCTION') == 'True':
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_SSL_REDIRECT = True
#     SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#     SESSION_COOKIE_AGE = 3600  # 1 hour expiry





from pathlib import Path
import os
import dj_database_url

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
    # ✅ SQLite (NO sslmode issue)
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

# 🌐 CORS
CORS_ALLOW_ALL_ORIGINS = True

# 🔒 Security (Production only)
if os.environ.get('PRODUCTION') == 'True':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_AGE = 3600


    