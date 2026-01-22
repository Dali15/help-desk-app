# Helpdesk Support - Tunisair

Une application Django de gestion de tickets de support avec pièces jointes, commentaires et authentification utilisateur.

## Caractéristiques

- 🎫 **Gestion de tickets** : créer, modifier, supprimer des tickets
- 📎 **Pièces jointes** : upload d'images et PDFs
- 💬 **Commentaires** : ajouter des commentaires aux tickets
- 👤 **Authentification** : inscription, connexion, gestion d'utilisateurs
- 🔐 **Permissions** : différents rôles (admin, agent, user)
- 📊 **Dashboard** : statistiques et vue d'ensemble
- 🎨 **Branding Tunisair** : logo et thème personnalisé
- 📱 **Responsive** : adapté mobile et desktop

## Stack technique

- **Backend** : Django 6.0.1
- **Frontend** : Bootstrap 5, Font Awesome
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Stockage fichiers** : système de fichiers (dev) / S3 (prod)

## Installation locale

### Prérequis
- Python 3.11+
- pip / virtualenv

### Étapes

1. **Cloner le repo**
```bash
git clone https://github.com/Dali15/help-desk-app.git
cd help-desk-app
```

2. **Créer un virtualenv**
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Migrations**
```bash
python manage.py migrate
```

5. **Créer un super utilisateur (admin)**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000 dans le navigateur.

## Déploiement

### Sur Render

1. Crée un compte [Render.com](https://render.com)
2. Crée un "Web Service"
3. Connecte ton repo GitHub
4. Configure :
   - **Build Command** : `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn hd.wsgi`
5. Ajoute des variables d'environnement :
   - `DJANGO_SETTINGS_MODULE` = `hd.settings`
   - `SECRET_KEY` = (génère une clé)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*.render.com`

### Sur Railway

1. Crée un compte [Railway.app](https://railway.app)
2. Connecte GitHub
3. Sélectionne le repo `help-desk-app`
4. Railway détecte Django automatiquement
5. Ajoute des variables d'environnement (même que Render)
6. Déploie en un clic

## Structure du projet

```
helpdesk/
├── hd/                          # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tickets/                      # Application principale
│   ├── models.py               # Ticket, Comment, Attachment
│   ├── views.py                # Logique métier
│   ├── forms.py                # Formulaires
│   ├── urls.py                 # Routes
│   ├── templates/              # Templates HTML
│   │   ├── base.html
│   │   ├── auth/
│   │   └── tickets/
│   └── static/                 # Assets (CSS, JS, images)
│       └── tickets/
│           └── img/logo.png    # Logo Tunisair
├── media/                       # Fichiers uploadés
├── db.sqlite3                   # Base de données
├── manage.py
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Variables d'environnement (.env)

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=sqlite:///db.sqlite3
```

## Utilisation

### Pour les utilisateurs
1. Inscris-toi
2. Crée des tickets
3. Ajoute des commentaires et pièces jointes
4. Suivi l'état du ticket

### Pour les admins
1. Gère tous les tickets
2. Assigne les tickets
3. Marque comme résolu/fermé
4. Accès à l'admin Django : `/admin/`

## Sécurité en production

- ✓ Utilise `DEBUG=False`
- ✓ Génère une `SECRET_KEY` forte
- ✓ Utilise HTTPS
- ✓ Configure `ALLOWED_HOSTS`
- ✓ Utilise une BD PostgreSQL ou MySQL
- ✓ Utilise S3 ou équivalent pour les uploads
- ✓ Configure un WAF (Web Application Firewall)
- ✓ Ajoute une authentification 2FA

## Développement futur

- [ ] Notifications email
- [ ] Recherche avancée
- [ ] Rapports PDF
- [ ] API REST
- [ ] Applications mobiles
- [ ] Intégration chatbot

## Support

Pour les problèmes ou suggestions, ouvre une issue sur GitHub.

## Licence

MIT License - voir LICENSE pour plus de détails.

---

Fait avec ❤️ pour Tunisair
