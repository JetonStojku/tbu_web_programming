# Lesson 06: Authentication and User Flows

## Lesson Goal

Implement and understand end-to-end user authentication flow in Django.

## What Students Will Build/Learn

- Register new users with a custom registration form.
- Use Django auth views for login, logout, and password reset.
- Protect views using `login_required` and `LoginRequiredMixin`.
- Configure password reset email backend for development.

## Project Files Covered

- `blog/forms.py` (`UserRegisterForm`)
- `blog/views.py` (`register`, protected views)
- `blog/urls.py` (auth routes)
- `blog_project/settings.py` (`LOGIN_REDIRECT_URL`, `LOGIN_URL`, `LOGOUT_REDIRECT_URL`)
- `blog/templates/user/*.html`

## Step-by-Step Explanation

1. Registration flow:
   - `register` function in `blog/views.py`
   - `UserRegisterForm` in `blog/forms.py`
   - `register.html` template.
2. Login/logout flow:
   - built-in auth views in `blog/urls.py`
   - templates `user/login.html` and `user/logout.html`.
3. Password reset flow:
   - `PasswordResetView`
   - `PasswordResetDoneView`
   - `PasswordResetConfirmView`
   - `PasswordResetCompleteView`
4. Access control:
   - `@login_required` for function views
   - `LoginRequiredMixin` for class-based views.
5. Redirect behavior:
   - controlled by settings in `blog_project/settings.py`.

Development email backend setup (for local testing only):

```powershell
# Add this line in blog_project/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Run and test auth flow:

```powershell
python manage.py runserver
```

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/auth/default/>
- <https://docs.djangoproject.com/en/5.1/topics/auth/default/#using-the-views>
- <https://docs.djangoproject.com/en/5.1/topics/auth/default/#the-login-required-decorator>
- <https://docs.djangoproject.com/en/5.1/topics/email/>

## Common Mistakes

- Assuming password reset works without email backend configuration.
- Forgetting to protect write operations with login checks.
- Not handling redirect paths after login/logout.
- Re-implementing built-in auth behavior that Django already provides.

## Exercise

1. Configure console email backend in `blog_project/settings.py`.
2. Create two users and test:
   - register
   - login/logout
   - password reset request.
3. Confirm reset email appears in the server console output.

## Expected Result

- Students can describe and demonstrate the full authentication lifecycle.
- Protected routes require login and redirect correctly.

### Quick Recap

Django auth gives a complete user system quickly. Your job is to wire routes, templates, and access control cleanly.
