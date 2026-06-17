# FairSplit Backend

Backend Django REST Framework pour l'application FairSplit - Partage de dépenses entre amis.

## Technologies

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL (production) / SQLite (développement)
- drf-spectacular (documentation API)

## Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venv
```

### 2. Activer l'environnement virtuel

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copier `.env.example` vers `.env` et configurer les variables d'environnement.

### 5. Migrations

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

## Développement

```bash
python manage.py runserver
```

L'API sera accessible sur `http://localhost:8000`

## Documentation API

- Swagger UI: `http://localhost:8000/api/docs/`
- Schema OpenAPI: `http://localhost:8000/api/schema/`

## Structure du projet

```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py      # Configuration commune
│   │   ├── dev.py       # Configuration développement
│   │   └── prod.py      # Configuration production
│   ├── urls.py          # Routes principales
│   ├── wsgi.py
│   └── asgi.py
├── accounts/            # App authentification
├── groups/              # App gestion des groupes
├── expenses/            # App gestion des dépenses
├── balances/            # App calcul des soldes
└── manage.py
```

## Apps Django

### accounts
Gestion de l'authentification et des utilisateurs.

### groups
Gestion des groupes de dépenses et des membres.

### expenses
Gestion des dépenses et des participants.

### balances
Calcul des soldes et suggestions de remboursements.
