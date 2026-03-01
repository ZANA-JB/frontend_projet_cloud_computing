# Objectif du projet

Une interface Flask/TailwindCSS servant de frontend à une API de partage de fichiers. Le but est de fournir un panneau utilisateur léger permettant de s'authentifier, téléverser, lister, modifier le statut et supprimer des documents, ainsi qu'une page publique présentant les fichiers partagés.

## Fonctionnalités développées

* Authentification (connexion / inscription / déconnexion)
* Téléversement de fichiers via formulaire multipart avec statut public/privé
* Affichage de la liste des fichiers privés pour l'utilisateur
* Actions sur chaque fichier : changer le statut, supprimer
* Page d'accueil listant les fichiers publics
* Sidebar et footer réutilisables
* Validation client et logs d'upload
* Limite de taille 10Mo sur le formulaire

## Structure du projet

`
frontend/
├── app.py                 # serveur Flask principal
├── api.py                 # wrapper HTTP vers l'API backend
├── templates/             # templates Jinja2
│   ├── base.html          # layout principal
│   ├── home.html          # page publique
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html     # tableau de bord utilisateur
│   ├── upload.html        # formulaire d'upload
│   └── components/        # fragments (header, footer, sidebar)
└── static/
    └── js/
        └── main.js       # scripts client (auto-fill, debug)
`

## Comment lancer le projet

1. **Préparer l'environnement** : Python?3.9+ et un virtuel (python -m venv .venv).
2. **Activer le virtuel** (PowerShell : & .\\.venv\\Scripts\\Activate.ps1).
3. **Installer les dépendances** :
   `
   pip install -r requirements.txt
   `
4. **Définir les variables** : CLOUD_API_URL (optionnel) et FLASK_SECRET_KEY.
5. **Démarrer le serveur** :
   `
   set FLASK_APP=app.py  # Windows
   flask run
   # ou
   py app.py
   `
6. **Ouvrir un navigateur** à http://127.0.0.1:5000.


