# Lesson 08: Testing and Deployment Basics

## Lesson Goal

Establish a practical baseline for automated testing and safe deployment configuration.

## What Students Will Build/Learn

- Understand current test status and what is missing.
- Plan and start writing useful Django tests.
- Apply a deployment safety checklist for settings and secrets.
- Separate development defaults from production requirements.

## Project Files Covered

- `blog/tests.py`
- `blog/models.py`
- `blog/forms.py`
- `blog/views.py`
- `blog_project/settings.py`

## Step-by-Step Explanation

1. Confirm dependencies are installed from the pinned `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

2. Current state:
   - `blog/tests.py` only contains the default placeholder.
3. Practical test plan for this project:
   - Model tests (`Post`, `Comment`, `__str__`, relationships).
   - Form tests (`clean_title`, `clean_content`, `clean_email`).
   - View/auth tests (login required for create/comment/delete, ownership restrictions).
4. Run tests:

```powershell
python manage.py test
```

5. Deployment baseline checklist (must be reviewed before production):
   - `DEBUG = False`
   - `ALLOWED_HOSTS` configured
   - secure `SECRET_KEY` from environment variable
   - production email backend and credentials
   - static files strategy
   - run `check --deploy` before release.

```powershell
python manage.py check --deploy
```

6. Environment variable direction (conceptual starter):
   - avoid hardcoding secrets in `settings.py`
   - load secret values from OS environment in production.

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/testing/overview/>
- <https://docs.djangoproject.com/en/5.1/topics/testing/tools/>
- <https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/>
- <https://docs.djangoproject.com/en/5.1/howto/static-files/>

## Common Mistakes

- Teaching only manual testing and skipping automated checks.
- Deploying with `DEBUG=True`.
- Keeping `SECRET_KEY` committed in public repositories.
- Ignoring `check --deploy` warnings.

## Exercise

1. Add two tests in `blog/tests.py`:
   - one form validation test (invalid short title/comment)
   - one auth/permission test (anonymous user cannot create post)
2. Run tests and capture output.

```powershell
python manage.py test blog
```

## Expected Result

- Students can run tests and understand what each test protects.
- Students can explain the minimum safe settings changes needed for deployment.

### Quick Recap

Production readiness starts early. Basic tests plus deployment-safe settings prevent common failures and security mistakes.
