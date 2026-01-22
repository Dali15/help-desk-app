# 🎫 Helpdesk Support System - Tunisair

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.2.10-green?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Dali15/help--desk--app-black?style=flat-square&logo=github)](https://github.com/Dali15/help-desk-app)
[![Live](https://img.shields.io/badge/Live-Render-46E3B7?style=flat-square&logo=render)](https://help-desk-tunisiar.onrender.com)

**Production-ready ticket management system for Tunisair** 🌍

[🚀 Live Demo](#-live-demo) • [📦 Installation](#-installation) • [🔧 Features](#-features) • [📚 Docs](#-documentation)

</div>

---

## 🚀 Live Demo

🌐 **URL**: [https://help-desk-tunisiar.onrender.com](https://help-desk-tunisiar.onrender.com)

### Test Credentials
```
Username: demo@tunisair.com
Password: demo123
```

---

## ✨ Features

### 🎫 Ticket Management
- ✅ Create, read, update, delete tickets
- ✅ Real-time status tracking (Open → In Progress → Resolved → Closed)
- ✅ Priority levels (Low, Medium, High)
- ✅ Category classification (Bug, Feature, Support, Other)
- ✅ Urgent flag for critical issues

### 📎 File Attachments
- ✅ Upload images (PNG, JPG, GIF) and PDFs
- ✅ Image preview in ticket details
- ✅ Direct download links
- ✅ Secure file storage with date-based organization

### 💬 Collaboration
- ✅ Add comments to tickets
- ✅ Track comment history
- ✅ Delete comments (admin/owner)
- ✅ Real-time updates

### 👤 User Management
- ✅ User registration & authentication
- ✅ Role-based access (Admin, User)
- ✅ Profile management
- ✅ Password security

### 📊 Dashboard & Analytics
- ✅ Real-time ticket statistics
- ✅ Open/In Progress/Resolved/Closed counts
- ✅ Priority distribution
- ✅ Urgent ticket alerts
- ✅ Recent activity feed

### 🎨 UI/UX
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Tunisair branding with logo & watermark
- ✅ Modern Bootstrap 5 interface
- ✅ Dark/light theme support
- ✅ Intuitive navigation

### 🔒 Security
- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ Permission-based access control
- ✅ Secure password hashing
- ✅ Admin panel access control

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Bootstrap 5, Vanilla JavaScript |
| **Backend** | Django 5.2, Python 3.11+ |
| **Database** | SQLite (dev) / PostgreSQL (production) |
| **Storage** | Local filesystem (dev) / S3 (production) |
| **Server** | Gunicorn + WhiteNoise |
| **Deployment** | Render.com |
| **Version Control** | Git + GitHub |

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip
- Git

### Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/Dali15/help-desk-app.git
cd help-desk-app

# 2. Create virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (admin account)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser 🎉

---

## 🚀 Deployment

### Deploy on Render (Recommended)

1. Fork this repository
2. Sign up on [Render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub account
5. Configure build & start commands
6. Set environment variables:
   ```
   DEBUG=False
   SECRET_KEY=<generate-from-djecrety.ir>
   ALLOWED_HOSTS=*.render.com
   ```
7. Deploy! 🚀

### Deploy on Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

---

## 📁 Project Structure

```
helpdesk/
├── hd/                              # Django project config
│   ├── settings.py                  # App settings
│   ├── urls.py                      # URL routing
│   ├── wsgi.py                      # WSGI config
│   └── asgi.py                      # ASGI config
│
├── tickets/                         # Main app
│   ├── models.py                    # Ticket, Comment, Attachment
│   ├── views.py                     # Business logic
│   ├── forms.py                     # Django forms
│   ├── urls.py                      # Routes
│   ├── admin.py                     # Admin interface
│   │
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Base template
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── tickets/
│   │       ├── dashboard.html
│   │       ├── ticket_list.html
│   │       ├── ticket_detail.html
│   │       └── ticket_form.html
│   │
│   └── static/                      # CSS, JS, images
│       └── tickets/
│           └── img/logo.png         # Tunisair logo
│
├── media/                           # User uploads
├── db.sqlite3                       # SQLite database
├── requirements.txt                 # Dependencies
├── Procfile                         # Deployment config
├── runtime.txt                      # Python version
├── README.md                        # This file
└── manage.py                        # Django CLI
```

---

## 📖 Usage

### For Users
1. **Register** → Create account
2. **Create Ticket** → Describe your issue
3. **Upload Files** → Add screenshots/documents
4. **Track Status** → Monitor progress
5. **Comment** → Communicate with support team

### For Admins
1. **View All Tickets** → Dashboard overview
2. **Assign** → Assign to team members
3. **Update Status** → Move through workflow
4. **Add Comments** → Communicate resolutions
5. **Manage Users** → `/admin/` panel

---

## 🔐 Environment Variables

Create `.env` file:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=sqlite:///db.sqlite3
DJANGO_SETTINGS_MODULE=hd.settings
```

Generate SECRET_KEY: [djecrety.ir](https://djecrety.ir/)

---

## 🗂 Database Models

### Ticket
```python
- id (Primary Key)
- title (CharField)
- description (TextField)
- priority (Choices: LOW, MED, HIGH)
- status (Choices: OPEN, IN_PROGRESS, RESOLVED, CLOSED)
- category (Choices: BUG, FEATURE, SUPPORT, OTHER)
- requester_name (CharField)
- requester_email (EmailField)
- assigned_to (CharField)
- is_urgent (BooleanField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- resolved_at (DateTimeField)
```

### Comment
```python
- id (Primary Key)
- ticket (ForeignKey → Ticket)
- author_name (CharField)
- content (TextField)
- created_at (DateTimeField)
```

### Attachment
```python
- id (Primary Key)
- ticket (ForeignKey → Ticket)
- file (FileField)
- uploaded_at (DateTimeField)
```

---

## 🧪 Testing

```bash
# Run tests
python manage.py test

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🔄 API Endpoints (Future)

- `GET /api/tickets/` - List all tickets
- `POST /api/tickets/` - Create ticket
- `GET /api/tickets/<id>/` - Get ticket details
- `PUT /api/tickets/<id>/` - Update ticket
- `DELETE /api/tickets/<id>/` - Delete ticket

---

## 🚧 Roadmap

- [ ] REST API (Django Rest Framework)
- [ ] Email notifications
- [ ] Advanced search & filters
- [ ] PDF report generation
- [ ] Mobile app (React Native)
- [ ] WebSocket notifications
- [ ] SLA tracking
- [ ] Knowledge base integration
- [ ] Multi-language support
- [ ] Audit logs

---

## 🤝 Contributing

Contributions welcome! 

```bash
# Fork the repo
# Create feature branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add amazing feature'

# Push to branch
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**Dali15** - [GitHub](https://github.com/Dali15) | [LinkedIn](https://linkedin.com)

---

## 💬 Support

- 📧 Email: support@tunisair.com
- 🐛 Report Issues: [GitHub Issues](https://github.com/Dali15/help-desk-app/issues)
- 💡 Feature Requests: [Discussions](https://github.com/Dali15/help-desk-app/discussions)

---

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Render Deployment Guide](https://render.com/docs)
- [Git Cheatsheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf)

---

<div align="center">

**Made with ❤️ for Tunisair**

⭐ If you find this useful, please star the repository!

</div>

