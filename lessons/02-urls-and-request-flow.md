# Lesson 02: URLs and Request Flow

## Lesson Goal

Learn how Django maps incoming URLs to views and returns responses.

## What Students Will Build/Learn

- Understand project-level and app-level URL configuration.
- Use path converters like `<int:pk>`.
- Use named routes and reverse URL lookup.
- Compare class-based and function-based views in this project.

## Project Files Covered

- `blog_project/urls.py`
- `blog/urls.py`
- `blog/views.py`
- `blog/models.py` (for `get_absolute_url`)

## Step-by-Step Explanation

1. Start at `blog_project/urls.py`:
   - `path('admin/', admin.site.urls)` routes admin.
   - `path('', include('blog.urls'))` delegates all other paths to the app.
2. Open `blog/urls.py` and identify route patterns:
   - list page (`''`)
   - detail/update/delete with `<int:pk>`
   - auth routes (`login`, `logout`, `password_reset`)
3. Explain route names (`name='post-detail'`) and why template links use names, not hardcoded URLs.
4. Show reverse lookup in code:
   - `reverse('post-detail', kwargs={'pk': self.object.pk})` in `PostCreateView`
   - `get_absolute_url` in `Post` model.
5. Compare view styles used here:
   - Class-based views for core CRUD (`ListView`, `DetailView`, etc.)
   - Function-based views for comment actions and registration.

```powershell
python manage.py runserver
```

Test route examples in browser:

- `http://localhost:8000/`
- `http://localhost:8000/post/1/`
- `http://localhost:8000/login/`

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/http/urls/>
- <https://docs.djangoproject.com/en/5.1/topics/http/views/>
- <https://docs.djangoproject.com/en/5.1/topics/class-based-views/>
- <https://docs.djangoproject.com/en/5.1/ref/urlresolvers/>

## Common Mistakes

- Forgetting to include app URLs in project URLs.
- Hardcoding URLs in templates instead of `{% url %}`.
- Mismatch between URL converter type and view expectations.
- Renaming route names without updating template links.

## Exercise

1. Add a simple `about/` route in `blog/urls.py`.
2. Implement a minimal view in `blog/views.py` that returns plain text or a simple template.
3. Add a link to the new route in `blog/templates/blog/base.html`.
4. Verify route lookup by name using `{% url 'about' %}`.

## Expected Result

- Students can trace a request from URL pattern to view to response.
- Students can explain why named routes are safer than hardcoded URL strings.

### Quick Recap

Routing is the entry gate of every feature. Understanding URL include + named route patterns will simplify all later Django work.
