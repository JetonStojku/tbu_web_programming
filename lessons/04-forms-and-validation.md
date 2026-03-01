# Lesson 04: Forms and Validation

## Lesson Goal

Use Django forms to handle user input safely, validate data, and render clear error messages.

## What Students Will Build/Learn

- Understand `ModelForm` usage for posts, movies, reviews, comments, and gallery images.
- Extend `UserCreationForm` for registration.
- Implement custom validation with `clean_<field>()` methods.
- Connect form errors to templates.

## Project Files Covered

- `blog/forms.py`
- `blog/views.py` (form usage in create/register/review/comment/gallery flows)
- `blog/templates/blog/post_form.html`
- `blog/templates/blog/movie_form.html`
- `blog/templates/blog/movie_detail.html`
- `blog/templates/user/register.html`

## Step-by-Step Explanation

1. In `blog/forms.py`, inspect `PostForm` and `CommentForm`:
   - `Meta.model`
   - `Meta.fields`
   - custom widgets for Bootstrap styling.
2. Inspect movie-related forms:
   - `MovieForm`
   - `MovieImageForm`
   - `MovieReviewForm`
   - `MovieCommentForm`
3. Review custom validators:
   - `clean_title` enforces minimum title length.
   - `clean_content` enforces comment length.
   - `clean_stars` enforces `1..5` movie ratings.
4. Study `UserRegisterForm(UserCreationForm)`:
   - added `email` field
   - `clean_email` uniqueness check.
5. In `blog/views.py`, identify form lifecycle:
   - instantiate form with `request.POST`
   - include `request.FILES` for image uploads
   - call `is_valid()`
   - save object and handle errors/messages.
6. In templates, show field errors near inputs.

```powershell
python manage.py runserver
```

Try invalid data examples:

- Post title shorter than 5 chars.
- Comment shorter than 10 chars.
- Registration with an existing email.
- Movie review stars outside `1..5`.
- Movie comment shorter than 5 chars.

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

1. Add one extra validation rule in `MovieForm`:
   - Example: reject years before `1888`.
2. Ensure the error appears in `blog/templates/blog/movie_form.html` below the year field.
3. Test with both valid and invalid submissions.

## Expected Result

- Students can explain where validation should live and why.
- Form errors are shown in the UI and invalid data is not saved.

### Quick Recap

Django forms centralize input parsing, validation, and error handling. This keeps views cleaner and protects data quality.
