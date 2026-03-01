# Lesson 04: Forms and Validation

## Lesson Goal

Use Django forms to handle user input safely, validate data, and render clear error messages.

## What Students Will Build/Learn

- Understand `ModelForm` usage for `Post` and `Comment`.
- Extend `UserCreationForm` for registration.
- Implement custom validation with `clean_<field>()` methods.
- Connect form errors to templates.

## Project Files Covered

- `blog/forms.py`
- `blog/views.py` (form usage in create/register/comment flows)
- `blog/templates/blog/post_form.html`
- `blog/templates/user/register.html`

## Step-by-Step Explanation

1. In `blog/forms.py`, inspect `PostForm` and `CommentForm`:
   - `Meta.model`
   - `Meta.fields`
   - custom widgets for Bootstrap styling.
2. Review custom validators:
   - `clean_title` enforces minimum title length.
   - `clean_content` enforces comment length.
3. Study `UserRegisterForm(UserCreationForm)`:
   - added `email` field
   - `clean_email` uniqueness check.
4. In `blog/views.py`, identify form lifecycle:
   - instantiate form with `request.POST`
   - call `is_valid()`
   - save object and handle errors/messages.
5. In templates, show field errors near inputs.

```powershell
python manage.py runserver
```

Try invalid data examples:

- Post title shorter than 5 chars.
- Comment shorter than 10 chars.
- Registration with an existing email.

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/forms/>
- <https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/>
- <https://docs.djangoproject.com/en/5.1/ref/forms/validation/>
- <https://docs.djangoproject.com/en/5.1/topics/auth/default/#django.contrib.auth.forms.UserCreationForm>

## Common Mistakes

- Trusting only browser-side `required` checks.
- Forgetting `is_valid()` before saving.
- Returning raw form errors without user-friendly placement in templates.
- Performing duplicate business rules in many views instead of centralizing in form clean methods.

## Exercise

1. Add one extra validation rule in `PostForm`:
   - Example: reject banned words in title.
2. Ensure the error appears in `blog/templates/blog/post_form.html` below the title field.
3. Test with both valid and invalid submissions.

## Expected Result

- Students can explain where validation should live and why.
- Form errors are shown in the UI and invalid data is not saved.

### Quick Recap

Django forms centralize input parsing, validation, and error handling. This keeps views cleaner and protects data quality.
