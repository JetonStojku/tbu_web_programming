# Lesson 08: Testing and Deployment Basics

## Lesson Goal

Establish a practical baseline for automated testing and safe deployment configuration.

## What Students Will Build/Learn

- Understand the current automated test coverage in this project.
- Extend existing Django tests for new movie features.
- Apply a deployment safety checklist for settings and secrets.
- Separate development defaults from production requirements, including media files.

## Project Files Covered

- `blog/tests.py`
- `blog/models.py`
- `blog/forms.py`
- `blog/views.py`
- `blog_project/settings.py`
- `blog_project/urls.py`

## Step-by-Step Explanation

1. Confirm dependencies are installed from the pinned `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

2. Current state:
   - `blog/tests.py` contains a movie-focused test suite (model, permission, flow, and render checks).
   - Test database is created automatically during `manage.py test`.
3. Covered scenarios include:
   - `MovieReview` uniqueness and stars validation.
   - anonymous vs authenticated behavior on movie actions.
   - non-staff blocked from movie management routes.
   - owner/staff moderation rules for reviews/comments.
   - review upsert behavior (single row per user/movie).
   - list/detail rendering with rating aggregate output.
4. Run tests:

```powershell
python manage.py test
```

5. Run checks before deployment:

```powershell
python manage.py check
python manage.py check --deploy
```

6. Deployment baseline checklist (must be reviewed before production):
   - `DEBUG = False`
   - `ALLOWED_HOSTS` configured
   - secure `SECRET_KEY` from environment variable
   - production email backend and credentials
   - static files strategy
   - media files strategy (`MEDIA_URL` / `MEDIA_ROOT` in development; cloud/static server in production)
7. Environment variable direction (conceptual starter):
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

1. Add two extra tests in `blog/tests.py`:
   - invalid gallery image upload handling
   - staff-only access assertion for `movie-image-add`
2. Run tests and capture output.

```powershell
python manage.py test blog
```

## Expected Result

- Students can run tests and understand what each test protects.
- Students can explain the minimum safe settings changes needed for deployment, including media file handling.

### Quick Recap

Production readiness starts early. Basic tests plus deployment-safe settings prevent common failures and security mistakes.
