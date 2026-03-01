# Lesson 01: Project Setup and Architecture

## Lesson Goal

Understand how this Django project is organized and run it locally from scratch.

## What Students Will Build/Learn

- Set up the project environment on Windows PowerShell.
- Run the Django development server.
- Understand the role of `manage.py`, `blog_project`, and `blog`.
- Read key settings for apps, middleware, templates, and database.

## Project Files Covered

- `manage.py`
- `requirements.txt`
- `blog_project/settings.py`
- `blog_project/urls.py`
- `blog/apps.py`

## Step-by-Step Explanation

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run initial migrations to create the SQLite schema.
4. Create a superuser for admin access.
5. Start the development server and verify both app and admin routes.
6. Open `blog_project/settings.py` and identify:
   - `INSTALLED_APPS`
   - `MIDDLEWARE`
   - `TEMPLATES`
   - `DATABASES`

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Architecture map (current project):

- `manage.py`: entry point for Django management commands.
- `blog_project/`: project-level config (`settings.py`, `urls.py`, ASGI/WSGI files).
- `blog/`: application logic (models, forms, views, templates, urls).
- `db.sqlite3`: local database file used in development.

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/intro/install/>
- <https://docs.djangoproject.com/en/5.1/intro/tutorial01/>
- <https://docs.djangoproject.com/en/5.1/topics/settings/>
- <https://docs.djangoproject.com/en/5.1/ref/django-admin/>

## Common Mistakes

- Running commands without activating the virtual environment.
- Forgetting `python manage.py migrate` before `runserver`.
- Editing the wrong settings file.
- Not adding new apps to `INSTALLED_APPS`.

## Exercise

1. Run the setup commands on your machine.
2. Open `blog_project/settings.py` and explain the purpose of:
   - `INSTALLED_APPS`
   - `MIDDLEWARE`
   - `DATABASES`
3. Start the server and open:
   - `http://localhost:8000/`
   - `http://localhost:8000/admin/`

## Expected Result

- The app and admin page load without errors.
- Students can describe what each top-level folder/file does.

### Quick Recap

This lesson established the runtime environment and the architectural map students will use in every next lesson.
