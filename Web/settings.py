"""
Django settings for Web project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from pathlib import Path
import os

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Build paths inside the project like this: BASE_DIR / 'subdir'.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3q%frfi_urea*^-23@u&1thgjs(w7zqoagkv+f76ch9=o-idap'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 5 * 60 * 60 #

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Django提供兩種伺服器通道
#   此處選用ASGI
#   支援WebSocket
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# WSGI_APPLICATION = 'Web.wsgi.application'
ASGI_APPLICATION = "Web.asgi.application"


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   使用通道層
#   (部屬建議)Redis
#   或者
#   (開發用)記憶體通道
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }
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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myweb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'aimma.com',
        'PORT': '3306',
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

STATIC_ROOT = './static_file/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   Redirect to home URL after login (Default redirects to /accounts/profile/)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LOGIN_REDIRECT_URL = '/'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#   LDAP 連線部分
#   將LDAP串接到伺服器上
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Django-auth-ldap 配置部分
import ldap
from django_auth_ldap.config import LDAPSearch,GroupOfNamesType

#修改Django认证先走ldap，再走本地认证
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

#ldap的连接基础配置
AUTH_LDAP_SERVER_URI = "ldap://qnap.com:389" # ldap or ad 服务器地址
AUTH_LDAP_BIND_DN = "cn=admin,dc=qnap,dc=com" # 管理员的dn路径
AUTH_LDAP_BIND_PASSWORD = '1234' # 管理员密码

#允许认证用户的路径
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=people,dc=qnap,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)

#通过组进行权限控制
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=groups,dc=qnap,dc=com",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)"
)

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

#is_staff:这个组里的成员可以登录；is_superuser:组成员是django admin的超级管理员；is_active:组成员可以登录django admin后台，但是无权限查看后台内容
# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_staff": "ou=groups,dc=qnap,dc=com",
#     "is_superuser": "cn=admin,dc=qnap,dc=com",
# }
#通过组进行权限控制end

#如果ldap服务器是Windows的AD，需要配置上如下选项
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}

#当ldap用户登录时，从ldap的用户属性对应写到django的user数据库，键为django的属性，值为ldap用户的属性
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "uid",
    "name": "sn",
    "email": "mail",
}

#如果为True，每次组成员都从ldap重新获取，保证组成员的实时性；反之会对组成员进行缓存，提升性能，但是降低实时性
AUTH_LDAP_FIND_GROUP_PERMS = True