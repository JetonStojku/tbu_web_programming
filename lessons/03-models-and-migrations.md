# Lesson 03: Models and Migrations

## Lesson Goal

Understand how Django models define database structure and how migrations apply schema changes safely.

## What Students Will Build/Learn

- Read and explain `Post`, `Comment`, `Movie`, `MovieImage`, `MovieReview`, and `MovieComment` models.
- Understand foreign keys to `User` and reverse relationships.
- Use `makemigrations` and `migrate` correctly.
- Interpret migration files such as `0001_initial.py` and `0002_...`.

## Project Files Covered

- `blog/models.py`
- `blog/migrations/0001_initial.py`
- `blog/migrations/0002_movie_alter_comment_post_moviecomment_movieimage_and_more.py`
- `blog/admin.py`
- `blog/templates/blog/post_detail.html` (uses `post.comments.all`)
- `blog/templates/blog/movie_detail.html` (uses gallery/reviews/comments relations)

## Step-by-Step Explanation

1. Review `Post` model fields:
   - `title` (`CharField`)
   - `content` (`TextField`)
   - `author` (`ForeignKey` to `User`)
   - `date_posted` (`DateTimeField(auto_now_add=True)`)
2. Review `Comment` model fields and relation to `Post`.
3. Review movie models:
   - `Movie` (basic metadata + `cover`)
   - `MovieImage` (`movie` relation + gallery image file)
   - `MovieReview` (`movie`, `user`, `stars`)
   - `MovieComment` (`movie`, `user`, `content`)
4. Explain reverse relation access in templates:
   - `post.comments.all` (enabled by `related_name='comments'`).
   - `movie.gallery_images.all`, `movie.reviews.all`, `movie.movie_comments.all`.
5. Explain model helper methods:
   - `__str__` for readable display in admin/shell.
   - `get_absolute_url` for redirect after create/update (`Post` and `Movie`).
6. Inspect `blog/migrations/0001_initial.py` and `0002_...`:
   - dependencies
   - `CreateModel` operations
   - constraints:
     - unique review per `(movie, user)`
     - stars check between `1` and `5`
   - field definitions translated to migration operations.

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

Optional migration SQL inspection:

```powershell
python manage.py sqlmigrate blog 0002
```

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/db/models/>
- <https://docs.djangoproject.com/en/5.1/topics/db/examples/many_to_one/>
- <https://docs.djangoproject.com/en/5.1/topics/migrations/>
- <https://docs.djangoproject.com/en/5.1/ref/models/instances/#get-absolute-url>

## Common Mistakes

- Editing old migration files manually after they were applied.
- Forgetting to run migrations after model changes.
- Using `null=True`/`blank=True` incorrectly.
- Not defining a readable `__str__` method.

## Exercise

1. Add a new field to `Movie`, for example:
   - `language = models.CharField(max_length=50, default='English')`
2. Run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

3. Confirm schema change in Django shell or admin.

## Expected Result

- Students can map model code to database schema changes.
- Students can explain what migration files represent and when they are created.

### Quick Recap

Models are the source of truth for data structure. Migrations are the safe mechanism that converts model changes into database operations.
