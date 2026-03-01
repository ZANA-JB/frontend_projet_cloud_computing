# FileShare Frontend

Ce dépôt contient uniquement le frontend de l'application de partage de fichiers, développé avec **Flask** (templates Jinja2) et **TailwindCSS** via CDN. Aucune logique métier ou base de données n'est implémentée ici ; il s'agit d'une interface prête à recevoir des endpoints REST (Supabase, Cloudinary, etc.).

## Structure du projet

```
frontend/
├── app.py                 # serveur Flask principal
├── templates/             # templates Jinja2
│   ├── base.html          # layout principal
│   ├── home.html          # page publique d'accueil
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html     # tableau de bord utilisateur
│   ├── upload.html        # formulaire d'upload
│   └── components/        # morceaux réutilisables
│       ├── _header.html
│       ├── _footer.html
│       └── _sidebar.html
└── static/
    └── js/
        └── main.js       # helpers partagés
```

## Pages/créées

Toutes les pages demandées ont été installées sous forme de templates : 

1. **Accueil public** (`/`) — liste dynamique de fichiers publics; comportant barre de recherche et pagination.
2. **Connexion** (`/login`) — formulaire d'authentification.
3. **Inscription** (`/signup`) — formulaire de création de compte.
4. **Tableau de bord** (`/dashboard`) — affiche fichiers privés + accès aux publics, avec sidebar et actions de modification.
5. **Upload** (`/upload`) — formulaire d'envoi de documents vers le backend (multipart/form-data, avec statut public/privé).

Les composants UI (`header`, `footer`, `sidebar`) sont extraits en fragments réutilisables.

## Routes Flask (frontend)

| URL              | Méthodes     | Description                                             | Protection   |
|------------------|--------------|---------------------------------------------------------|--------------|
| `/`              | GET          | Page d'accueil publique                                 | publique     |
| `/login`         | GET, POST    | Formulaire de connexion                                 | publique     |
| `/signup`        | GET, POST    | Formulaire d'inscription                                | publique     |
| `/logout`        | GET          | Déconnecte l'utilisateur (vide la session)              | publique     |
| `/dashboard`     | GET          | Tableau de bord (requiert session)                      | login requis |
| `/upload`        | GET, POST    | Formulaire d'upload (requiert session)                 | login requis |

Les appels REST sont désormais dirigés vers l’API de production (ou celle indiquée via
`CLOUD_API_URL`). Le module `api.py` centralise toutes les requêtes avec gestion du token,
ce qui garantit une intégration parfaite avec les endpoints du backend.

## Points d'intégration backend restants

- **Authentification** : remplacer la logique de `session[...]` par des appels à Supabase Auth (ou autre), traiter tokens.
- **Données** : remplacer les mocks `/api/public-files` et `/api/private-files` par des requêtes vers Supabase.
- **Upload** : remplacer le bloc `alert('Upload logic …')` dans `upload.html` par l'appel réel à Cloudinary + `POST` metadata vers Supabase. Le formulaire inclut désormais un champ caché `user_id` (utile pour les diagnostics) et une limite client de 10 Mo est vérifiée en JavaScript.
- **Gestion des erreurs et états de chargement** sont déjà préparés dans les fichiers JS (indicateurs disabled/loading). Le script `static/js/main.js` comporte également des logs détaillés (`console.log`) destinés à suivre les étapes d'upload et faciliter le debug.
- **Pages additionnelles** : déjà prévues dans la navigation (starred, trash) mais sans templates — à créer si nécessaire.

## Démarrage local

Voici les étapes pour lancer le projet sur votre machine et pouvoir l'envoyer à un ami :

1. **Prérequis**
   - Python 3.9+ installé (03/2026). Sur Windows, téléchargez depuis python.org et cochez "Add to PATH".
   - Un environnement virtuel est fortement conseillé (`python -m venv .venv`).
   - Depuis la racine du dépôt, activez‑le :
     - PowerShell : `& .\.venv\Scripts\Activate.ps1`
     - CMD : `.\.venv\Scripts\activate.bat`
     - Bash (WSL) : `source .venv/bin/activate`

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**
   - `CLOUD_API_URL` (optionnel) : URL de l’API backend. Par défaut `https://cloud-backend-80wx.onrender.com`.
   - `FLASK_SECRET_KEY` (requis) : une chaîne aléatoire pour sécuriser la session Flask.

   Exemple PowerShell :
   ```powershell
   $env:CLOUD_API_URL = 'https://cloud-backend-80wx.onrender.com'
   $env:FLASK_SECRET_KEY = 'une-cle-secrete'
   ```

4. **Lancer le serveur**
   ```bash
   # soit avec Flask CLI (reloader activé par défaut)
   set FLASK_APP=app.py         # sur Windows
   flask run

   # soit directement (le fichier `app.py` désactive le reloader pour éviter les
   # redémarrages multipliés et les codes de sortie 1 qui inquiètent certains)
   py app.py
   ```
   Le serveur démarrera en mode debug sur `http://127.0.0.1:5000`. Si vous voyez un
   code de sortie `1` ou des messages de "restarting with watchdog", c'est normal
   avec la CLI; utilisez `py app.py` pour un démarrage plus propre.

5. **Ouvrir le navigateur** et accéder à la page d'accueil.

> ⚠️ Ne vous inquiétez pas des messages « Restarting with watchdog » ou « Debugger PIN » : ce sont des notifications normales générées lors de l'autoreload en mode debug. Le code se relance chaque fois qu'un fichier Python est modifié.

### Partager le projet

Pour envoyer le frontend à un ami, il suffit de transmettre le répertoire (`zip`/Git). Il devra :

1. Créer et activer un environnement virtuel.
2. Installer les dépendances (`pip install -r requirements.txt`).
3. Définir les variables d'environnement ci-dessus.
4. Lancer `py app.py` et accéder à `http://localhost:5000`.

Le README contient désormais tout ce qu'il faut pour démarrer rapidement (y compris la configuration de l'URL du backend). Le backend reste inchangé ; il doit être accessible à l'adresse indiquée ou à celle que vous fournirez via `CLOUD_API_URL`.

Le frontend est entièrement connecté : authentification, upload, affichage des fichiers, modifications de statut et suppression fonctionnent avec les endpoints fournis.

---

**Tous les fichiers HTML requis sont en place** ; il ne reste que l’implémentation des endpoints métier côté serveur pour une intégration parfaite. Bonne continuation !