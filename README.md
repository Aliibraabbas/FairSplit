# FairSplit

Application web de partage de dépenses entre amis, inspirée de Tricount.

## 📋 Description

FairSplit permet de créer des groupes, d'ajouter des membres, d'enregistrer des dépenses et de calculer automatiquement les soldes de chaque membre. L'application propose ensuite des remboursements optimisés pour équilibrer les comptes.

## 🚀 Technologies

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL / SQLite
- drf-spectacular (Swagger)

### Frontend
- React 18
- Vite
- React Router DOM
- Axios

## 📁 Structure du projet

```
FairSplit/
├── backend/              # API Django REST Framework
│   ├── config/           # Configuration Django
│   │   ├── settings/     # Settings (base, dev, prod)
│   │   └── urls.py       # Routes principales
│   ├── accounts/         # App authentification
│   ├── groups/           # App gestion des groupes
│   ├── expenses/         # App gestion des dépenses
│   ├── balances/         # App calcul des soldes
│   └── manage.py
├── frontend/             # Application React
│   ├── src/
│   │   ├── api/          # Configuration Axios
│   │   ├── components/   # Composants React
│   │   ├── contexts/     # Contexts (Auth, etc.)
│   │   ├── hooks/        # Custom hooks
│   │   ├── layouts/      # Layouts
│   │   ├── pages/        # Pages
│   │   ├── routes/       # Configuration routes
│   │   ├── services/     # Services API
│   │   └── styles/       # CSS
│   └── package.json
└── PROJECT_PLAN.md       # Plan détaillé du projet
```

## 🛠️ Installation

### Backend

1. Créer et activer l'environnement virtuel :
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
```

4. Appliquer les migrations :
```bash
python manage.py migrate
```

5. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur :
```bash
python manage.py runserver
```

### Frontend

1. Installer les dépendances :
```bash
cd frontend
npm install
```

2. Configurer les variables d'environnement :
```bash
cp .env.example .env
```

3. Lancer le serveur de développement :
```bash
npm run dev
```

## 🌐 Accès

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs/

## 📚 Documentation

Consultez le fichier `PROJECT_PLAN.md` pour le plan détaillé du projet incluant :
- Fonctionnalités complètes
- Modèles de données
- Endpoints API
- Règles métier
- Étapes de développement

## 🔑 Fonctionnalités principales

- ✅ Authentification utilisateur
- ✅ Création et gestion de groupes
- ✅ Ajout de membres aux groupes
- ✅ Enregistrement de dépenses
- ✅ Calcul automatique des soldes
- ✅ Suggestions de remboursements optimisés
- ✅ Interface responsive

## 📝 Licence

Projet académique - IIM A5 2025