# Architecture du projet FairSplit

## 📂 Arborescence complète

```
FairSplit/
├── .git/
├── .gitignore
├── README.md
├── PROJECT_PLAN.md
├── ARCHITECTURE.md
│
├── venv/                          # Environnement virtuel Python
│
├── backend/                       # Backend Django REST Framework
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md
│   ├── requirements.txt
│   ├── manage.py
│   │
│   ├── config/                    # Configuration principale Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   ├── urls.py                # Routes principales API
│   │   └── settings/              # Configuration par environnement
│   │       ├── __init__.py
│   │       ├── base.py            # Configuration commune
│   │       ├── dev.py             # Configuration développement
│   │       └── prod.py            # Configuration production
│   │
│   ├── accounts/                  # App authentification
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── groups/                    # App gestion des groupes
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── expenses/                  # App gestion des dépenses
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   └── balances/                  # App calcul des soldes
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── serializers.py
│       ├── services.py            # Logique métier des calculs
│       ├── tests.py
│       └── migrations/
│
└── frontend/                      # Frontend React + Vite
    ├── .env
    ├── .env.example
    ├── .gitignore
    ├── README.md
    ├── package.json
    ├── vite.config.js
    ├── index.html
    │
    └── src/
        ├── main.jsx               # Point d'entrée React
        ├── App.jsx                # Composant racine
        │
        ├── api/                   # Configuration Axios
        │   └── axiosConfig.js
        │
        ├── assets/                # Images, fonts, etc.
        │   └── .gitkeep
        │
        ├── components/            # Composants réutilisables
        │   └── common/
        │       ├── Loader.jsx
        │       └── ErrorMessage.jsx
        │
        ├── contexts/              # React Contexts
        │   └── AuthContext.jsx
        │
        ├── hooks/                 # Custom hooks
        │   └── useAuth.js
        │
        ├── layouts/               # Layouts de pages
        │   └── MainLayout.jsx
        │
        ├── pages/                 # Pages de l'application
        │   └── HomePage.jsx
        │
        ├── routes/                # Configuration des routes
        │   └── AppRoutes.jsx
        │
        ├── services/              # Services API
        │   ├── authService.js
        │   ├── groupService.js
        │   ├── expenseService.js
        │   └── balanceService.js
        │
        └── styles/                # Fichiers CSS
            └── index.css
```

## 🔧 Configuration Backend

### Settings Django

**`config/settings/base.py`**
- Configuration commune à tous les environnements
- Apps installées (DRF, CORS, drf-spectacular, apps métier)
- Middleware
- Configuration REST Framework
- Configuration Swagger

**`config/settings/dev.py`**
- DEBUG = True
- SQLite
- CORS pour localhost:5173

**`config/settings/prod.py`**
- DEBUG = False
- PostgreSQL
- Sécurité renforcée (SSL, cookies sécurisés)

### Apps Django

**accounts/**
- Authentification utilisateur
- Inscription, connexion, déconnexion
- Gestion du profil utilisateur

**groups/**
- Création et gestion des groupes
- Gestion des membres
- Permissions par groupe

**expenses/**
- Enregistrement des dépenses
- Gestion des participants
- Répartition des montants

**balances/**
- Calcul des soldes par membre
- Algorithme de remboursements optimisés
- Logique métier dans `services.py`

## 🎨 Configuration Frontend

### Structure React

**`src/api/`**
- Configuration Axios centralisée
- Intercepteurs pour la gestion des erreurs
- Base URL et credentials

**`src/services/`**
- Services pour chaque domaine métier
- Abstraction des appels API
- Gestion des endpoints

**`src/contexts/`**
- AuthContext : état global de l'authentification
- Futurs contexts (GroupContext, etc.)

**`src/routes/`**
- Configuration React Router
- Routes publiques et privées
- Protection des routes

**`src/components/`**
- Composants réutilisables
- Composants communs (Loader, ErrorMessage, etc.)
- Futurs composants métier

**`src/pages/`**
- Pages de l'application
- Une page = une route

**`src/layouts/`**
- Layouts partagés
- Header, Footer, Navigation

## 📦 Dépendances

### Backend
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
python-decouple==3.8
psycopg2-binary==2.9.9
drf-spectacular==0.27.0
```

### Frontend
```
react: ^18.2.0
react-dom: ^18.2.0
react-router-dom: ^6.20.0
axios: ^1.6.2
vite: ^5.0.8
@vitejs/plugin-react: ^4.2.1
```

## 🚀 Prochaines étapes

L'architecture est maintenant en place. Les prochaines étapes de développement seront :

1. **Étape 2 : Authentification**
   - Modèle User Django
   - Endpoints API auth
   - Pages login/register frontend

2. **Étape 3 : Gestion des groupes**
   - Modèles Group et GroupMember
   - API CRUD groupes
   - Interface frontend groupes

3. **Étape 4 : Gestion des dépenses**
   - Modèles Expense et ExpenseParticipant
   - API CRUD dépenses
   - Formulaires frontend

4. **Étape 5 : Calcul des soldes**
   - Logique de calcul dans services.py
   - Algorithme de remboursements
   - Affichage frontend

## 📝 Notes importantes

- **Aucun modèle Django n'a été créé** - uniquement la structure
- **Aucune API métier n'est implémentée** - uniquement les fichiers vides
- **Aucun composant métier frontend** - uniquement la fondation
- **Les migrations Django ne sont pas encore créées**
- **Les dépendances npm ne sont pas encore installées**

Cette architecture est prête pour le développement des fonctionnalités métier.
