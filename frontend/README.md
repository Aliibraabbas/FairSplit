# FairSplit Frontend

Frontend React pour l'application FairSplit - Partage de dépenses entre amis.

## Technologies

- React 18
- Vite
- React Router DOM
- Axios

## Installation

```bash
npm install
```

## Développement

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## Build

```bash
npm run build
```

## Structure du projet

```
src/
├── api/              # Configuration Axios
├── assets/           # Images, fonts, etc.
├── components/       # Composants réutilisables
│   └── common/       # Composants communs (Loader, ErrorMessage, etc.)
├── contexts/         # Contexts React (Auth, etc.)
├── hooks/            # Custom hooks
├── layouts/          # Layouts de pages
├── pages/            # Pages de l'application
├── routes/           # Configuration des routes
├── services/         # Services API
└── styles/           # Fichiers CSS
```
