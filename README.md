# Django Blog Application

A simple blog application built with Django for the Web Programming course.

## Features

- User authentication (Login/Logout)
- Create, Read, Update, Delete (CRUD) blog posts
- Comment system for posts
- Responsive design with Bootstrap
- Form validation
- Admin interface for content management
- CSRF protection
- SQLite database (default)

## Create a new django project and application

- new django project
  - django-admin startproject profiles_project .
- new django application
  - python manage.py startapp profiles_api

## Prerequisites

- Python 3.8+
- pip package manager
- Basic understanding of Python and web concepts

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/JetonStojku/tbu_web_programming.git
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create superuser (admin account)

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

## Project Structure

```bash
blog_project/
├── blog/
│   ├── migrations/       # Database migration files
│   ├── templates/        # HTML templates
│   │   └── blog/
│   ├── forms.py          # Form definitions
│   ├── models.py         # Database models
│   ├── urls.py           # App URL configuration
│   └── views.py          # View functions/classes
├── blog_project/
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
└── manage.py             # Django command-line utility
```

## Key Components

### Models

- `Post`: Blog posts with title, content, author, and timestamps
- `Comment`: Comments associated with posts

### Views

- Class-based views for CRUD operations
- Authentication mixins for authorization
- Function-based view for post details with comments

### Templates

- Bootstrap-powered responsive design
- Reusable base template
- Form error handling
- Conditional rendering based on authentication status

## Accessing the Application

1. Development server: <http://localhost:8000>
2. Admin interface: <http://localhost:8000/admin>

## Development Practices

1. Always work in the virtual environment
2. Use `./manage.py runserver` for local development
3. Create new database migrations when changing models:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Use Git for version control
5. Follow Django's MTV (Model-Template-View) architecture
6. Validate forms on both client and server side

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
