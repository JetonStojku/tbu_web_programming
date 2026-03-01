# Django Blog Application

A teaching project for introducing Django through a practical blog application.

## Course Lessons (Start Here)

Version note: all lesson examples and documentation links are pinned to **Django 5.1.x**.

1. [Lesson 01 - Project Setup and Architecture](lessons/01-project-setup-and-architecture.md)
2. [Lesson 02 - URLs and Request Flow](lessons/02-urls-and-request-flow.md)
3. [Lesson 03 - Models and Migrations](lessons/03-models-and-migrations.md)
4. [Lesson 04 - Forms and Validation](lessons/04-forms-and-validation.md)
5. [Lesson 05 - Templates and Bootstrap UI](lessons/05-templates-and-bootstrap-ui.md)
6. [Lesson 06 - Authentication and User Flows](lessons/06-authentication-and-user-flows.md)
7. [Lesson 07 - CRUD, Comments, Permissions, Messages](lessons/07-crud-comments-and-messages.md)
8. [Lesson 08 - Testing and Deployment Basics](lessons/08-testing-and-deployment-basics.md)

## Course Roadmap

- Lessons 01-02: project setup, architecture, URL routing, and request flow.
- Lessons 03-04: models, migrations, forms, and validation for posts and movies.
- Lessons 05-06: templates, UI rendering, authentication, and role-based access.
- Lessons 07-08: CRUD permissions, reviews/comments, testing, and deployment checklist.

## How to Use These Lessons in Class

- Suggested pacing: 8 sessions, 75-90 minutes per lesson.
- Classroom pattern per lesson:
  1. 15-20 min concept explanation
  2. 30-40 min live coding walkthrough in this repo
  3. 15-20 min student exercise and recap
- Keep students focused on project files listed in each lesson before introducing extra theory.

## Features in This Project

- User authentication (register, login, logout)
- Password reset flow (template-based)
- Create, Read, Update, Delete (CRUD) for blog posts
- Comment system on posts
- Movie manager with staff-only CRUD
- Movie reviews (1-5 stars, one review per user per movie)
- Movie comments with ownership and staff moderation rules
- Movie cover uploads and gallery image uploads
- Bootstrap-based UI templates
- Form validation with custom rules
- Admin interface for content management
- CSRF-protected POST forms
- SQLite database (default)

## Prerequisites

- Python 3.10+
- pip package manager
- Basic understanding of Python and web concepts

## Version Lock

To keep student environments consistent, this course is pinned to:

- `Django==5.1.7`
- `Pillow==11.1.0`
- `Bootstrap 5.3.0` via CDN (`blog/templates/blog/base.html`, CSS + JS bundle)

## Setup Instructions

### 1. Clone the repository

```powershell
git clone https://github.com/JetonStojku/tbu_web_programming.git
cd tbu_web_programming
```

### 2. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run migrations

```powershell
python manage.py migrate
```

### 5. Create superuser (admin account)

```powershell
python manage.py createsuperuser
```

### 6. Run development server

```powershell
python manage.py runserver
```

## Accessing the Application

1. Main app: <http://localhost:8000>
2. Admin interface: <http://localhost:8000/admin>

## Project Structure

```text
blog_project/
blog/
lessons/
manage.py
requirements.txt
db.sqlite3
README.md
```

## Development Workflow

1. Always work inside the virtual environment.
2. After changing models, run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

3. Run tests before class demos:

```powershell
python manage.py test
```

4. Follow Django MTV architecture and keep business logic in views/forms/models, not templates.

## Core Learning Resources

- [Django 5.1 Documentation](https://docs.djangoproject.com/en/5.1/)
- [Django 5.1 Tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
- [Django Settings Reference (5.1)](https://docs.djangoproject.com/en/5.1/ref/settings/)
- [Bootstrap 5.3 Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
