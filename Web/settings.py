from pathlib import Path
import os
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Build paths inside the project like this: BASE_DIR / 'subdir'.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '3q%frfi_urea*^-23@u&1thgjs(w7zqoagkv+f76ch9=o-idap'
DEBUG = True
ALLOWED_HOSTS = ['*']
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 5 * 60 * 60

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Application definition
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index.apps.IndexConfig',
    'werkzeug_debugger_runserver',
    'django_extensions',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ASGI_APPLICATION = "Web.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Database
#   https://docs.djangoproject.com/en/3.1/ref/settings/#databases
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     os.getenv('WEB_DB_NAME', 'pandian'),
        'USER':     os.getenv('WEB_DB_USER', 'root'),
        'PASSWORD': os.getenv('WEB_DB_PW', 'root'),
        'HOST':     os.getenv('WEB_DB_ADDR', '127.0.0.1'),
        'PORT':     os.getenv('WEB_DB_PORT', '3306'),
    }
}

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Password validation
#   https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Internationalization
#   https://docs.djangoproject.com/en/3.1/topics/i18n/
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_L10N = True
USE_TZ = True

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#    Static files (CSS, JavaScript, Images)
#   https://docs.djangoproject.com/en/3.1/howto/static-files/
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    BASE_DIR / "static_file"
]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Redirect to home URL after login (Default redirects to /accounts/profile/)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LOGIN_REDIRECT_URL = '/'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   LDAP 連線部分
#   將LDAP串接到伺服器上
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import ldap
from django_auth_ldap.config import LDAPSearch,GroupOfNamesType

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'django_auth_ldap.backend.LDAPBackend',
]
AUTH_LDAP_SERVER_URI = "ldap://qnap.com:389"
AUTH_LDAP_BIND_DN = "cn=admin,dc=qnap,dc=com"
AUTH_LDAP_BIND_PASSWORD = '1234'
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=people,dc=qnap,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=groups,dc=qnap,dc=com",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)"
)
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "uid",
    "name": "sn",
    "email": "mail",
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600