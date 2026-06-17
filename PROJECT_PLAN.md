# Projet Django - Partage de dépenses entre amis

## 1. Objectif du projet

Créer une application web de partage de dépenses entre amis, inspirée de Tricount.

L'application permet à un utilisateur de créer un groupe, ajouter des membres, enregistrer des dépenses, calculer automatiquement les soldes de chaque membre, puis proposer des remboursements pour équilibrer les comptes.

---

## 2. Stack technique

### Backend

* Django
* Django REST Framework
* PostgreSQL ou SQLite en développement
* Authentification utilisateur
* Permissions par groupe
* Logique métier isolée dans `services.py` 

### Frontend

* React ou HTML/CSS/JS
* Interface responsive
* Gestion des erreurs
* Gestion des chargements
* Appels API vers Django REST Framework

### Bonus

* Docker
* docker-compose
* Documentation API Swagger
* Export PDF ou CSV
* Invitation par lien
* Devises multiples

---

## 3. Fonctionnalités principales

### Authentification

* Inscription utilisateur
* Connexion utilisateur
* Déconnexion
* Protection des pages privées
* Gestion de l'utilisateur connecté

---

## 4. Fonctionnalités Backend

### Application `accounts` 

* Modèle utilisateur Django
* API inscription
* API connexion
* API profil utilisateur
* Permissions pour protéger les routes privées

### Application `groups` 

* Créer un groupe de dépenses
* Modifier un groupe
* Supprimer un groupe
* Voir la liste de mes groupes
* Voir le détail d'un groupe
* Ajouter des membres à un groupe
* Supprimer un membre d'un groupe
* Vérifier qu'un utilisateur ne peut voir que ses groupes
* Invitation par lien, en bonus

### Application `expenses` 

* Créer une dépense
* Modifier une dépense
* Supprimer une dépense
* Voir la liste des dépenses d'un groupe
* Choisir le payeur
* Choisir les participants
* Répartition égale entre participants
* Répartition inégale, en bonus
* Ajouter une description
* Ajouter une date de dépense
* Ajouter une catégorie de dépense

### Application `balances` 

* Calculer le solde de chaque membre
* Calculer qui doit de l'argent
* Calculer qui doit recevoir de l'argent
* Proposer des remboursements optimisés
* Isoler toute la logique de calcul dans `services.py` 
* Ajouter des tests unitaires sur les calculs

---

## 5. Modèles Django à prévoir

### User

* username
* email
* password

### Group

* name
* description
* created_by
* created_at
* updated_at

### GroupMember

* group
* user
* display_name
* joined_at
* role : owner / member

### Expense

* group
* title
* amount
* paid_by
* date
* category
* created_by
* created_at
* updated_at

### ExpenseParticipant

* expense
* member
* share_amount
* is_included

### Settlement

* group
* from_member
* to_member
* amount
* status : pending / paid
* created_at

---

## 6. API Backend à créer

### Auth

* POST `/api/auth/register/` 
* POST `/api/auth/login/` 
* POST `/api/auth/logout/` 
* GET `/api/auth/me/` 

### Groups

* GET `/api/groups/` 
* POST `/api/groups/` 
* GET `/api/groups/:id/` 
* PUT `/api/groups/:id/` 
* DELETE `/api/groups/:id/` 

### Members

* GET `/api/groups/:id/members/` 
* POST `/api/groups/:id/members/` 
* DELETE `/api/groups/:id/members/:memberId/` 

### Expenses

* GET `/api/groups/:id/expenses/` 
* POST `/api/groups/:id/expenses/` 
* GET `/api/expenses/:id/` 
* PUT `/api/expenses/:id/` 
* DELETE `/api/expenses/:id/` 

### Balances

* GET `/api/groups/:id/balances/` 
* GET `/api/groups/:id/settlements/` 

---

## 7. Fonctionnalités Frontend

### Pages principales

* Page d'accueil
* Page inscription
* Page connexion
* Dashboard utilisateur
* Liste des groupes
* Création d'un groupe
* Détail d'un groupe
* Liste des membres
* Liste des dépenses
* Ajout d'une dépense
* Modification d'une dépense
* Page des soldes
* Page des remboursements suggérés

### Composants frontend

* Header
* Sidebar ou navigation
* Card groupe
* Formulaire groupe
* Formulaire dépense
* Tableau des dépenses
* Liste des membres
* Résumé des soldes
* Composant remboursement
* Loader
* Message d'erreur
* Modal de confirmation
* Badge positif/négatif pour les soldes

---

## 8. UX/UI attendue

* Interface propre et moderne
* Design responsive mobile et desktop
* Dashboard clair
* Couleurs différentes pour :

  * montant payé
  * montant dû
  * solde positif
  * solde négatif
* Messages de succès après action
* Messages d'erreur clairs
* Confirmation avant suppression
* Empty states quand il n'y a pas encore de groupe ou dépense

---

## 9. Règles métier importantes

* Un utilisateur ne peut voir que les groupes dont il est membre
* Seul le créateur du groupe peut supprimer le groupe
* Une dépense appartient toujours à un groupe
* Le payeur doit être membre du groupe
* Les participants doivent être membres du groupe
* Le total des parts doit correspondre au montant de la dépense
* Les soldes doivent être recalculés après chaque ajout, modification ou suppression de dépense
* Les remboursements doivent minimiser le nombre de transactions

---

## 10. Calcul des soldes

La logique de calcul doit être dans un fichier `services.py`.

Exemple :

Si Ali paie 90 € pour Ali, Sara et Omar :

* Chaque personne doit payer 30 €
* Ali a payé 90 €
* Ali devait seulement 30 €
* Ali doit recevoir 60 €
* Sara doit 30 €
* Omar doit 30 €

Résultat :

* Sara rembourse 30 € à Ali
* Omar rembourse 30 € à Ali

---

## 11. Étapes de développement

### Étape 1 : Initialisation du projet

* Créer le projet Django
* Créer les apps Django
* Installer Django REST Framework
* Configurer settings dev/base/prod
* Configurer les routes API
* Initialiser le frontend
* Créer la structure globale du projet

### Étape 2 : Authentification

* Créer l'inscription
* Créer la connexion
* Créer la déconnexion
* Protéger les routes privées
* Tester l'authentification côté backend et frontend

### Étape 3 : Gestion des groupes

* Créer les modèles Group et GroupMember
* Créer les serializers
* Créer les vues API
* Créer la liste des groupes côté frontend
* Créer le formulaire de création de groupe
* Créer la page détail d'un groupe

### Étape 4 : Gestion des membres

* Ajouter des membres à un groupe
* Supprimer des membres
* Afficher les membres
* Gérer les permissions

### Étape 5 : Gestion des dépenses

* Créer les modèles Expense et ExpenseParticipant
* Créer les serializers
* Créer les endpoints API
* Créer le formulaire d'ajout de dépense
* Afficher les dépenses dans le groupe
* Ajouter modification et suppression

### Étape 6 : Calcul des soldes

* Créer `services.py` 
* Calculer les soldes par membre
* Calculer les remboursements suggérés
* Ajouter les endpoints API balances
* Afficher les soldes côté frontend

### Étape 7 : Amélioration UI/UX

* Ajouter loaders
* Ajouter messages d'erreur
* Ajouter confirmations
* Améliorer responsive
* Ajouter dashboard avec statistiques simples

### Étape 8 : Bonus

* Ajouter export CSV ou PDF
* Ajouter invitation par lien
* Ajouter devises multiples
* Ajouter répartition inégale
* Ajouter Swagger
* Ajouter Docker et docker-compose

### Étape 9 : README et préparation soutenance

* Écrire README complet
* Ajouter instructions d'installation
* Ajouter architecture du projet
* Ajouter captures d'écran
* Préparer schéma d'architecture
* Préparer démo live
* Préparer explication technique du calcul des soldes

---

## 12. Critères de réussite

Le projet est réussi si :

* L'utilisateur peut créer un compte
* L'utilisateur peut créer un groupe
* L'utilisateur peut ajouter des membres
* L'utilisateur peut ajouter des dépenses
* L'application calcule correctement les soldes
* L'application propose les remboursements
* L'interface est claire et responsive
* Le backend respecte Django REST Framework
* Les permissions sont bien gérées
* Le README est complet
* Le code est propre et organisé
