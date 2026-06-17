from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',

    'accounts',
    'groups',
    'expenses',
    'balances',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'FairSplit API',
    'DESCRIPTION': '''
    API REST complète pour le partage de dépenses entre amis et groupes.
    
    ## Fonctionnalités principales
    
    - **Authentification** : Inscription, connexion avec token
    - **Groupes** : Création, gestion des membres et invités
    - **Dépenses** : Ajout de dépenses avec répartition égale ou personnalisée
    - **Soldes** : Calcul automatique des soldes et remboursements suggérés
    - **Remboursements** : Enregistrement des remboursements effectués
    - **Invitations** : Création de liens d'invitation sécurisés
    - **Export** : Export CSV et Excel des données du groupe
    - **Devises multiples** : Support de EUR, USD, GBP, LBP
    
    ## Authentification
    
    Utilisez le header `Authorization: Token <votre_token>` pour les endpoints protégés.
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api',
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Serveur de développement'},
    ],
    'TAGS': [
        {'name': 'auth', 'description': 'Authentification et gestion des utilisateurs'},
        {'name': 'groups', 'description': 'Gestion des groupes de dépenses'},
        {'name': 'expenses', 'description': 'Gestion des dépenses'},
        {'name': 'balances', 'description': 'Calcul des soldes et remboursements'},
        {'name': 'invitations', 'description': 'Invitations par lien'},
        {'name': 'export', 'description': 'Export CSV et Excel'},
    ],
}
