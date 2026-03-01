# Lesson 07: CRUD, Reviews, Comments, Permissions, and Messages

## Lesson Goal

Understand end-to-end movie CRUD and user interaction flows (ratings/comments) with correct permission checks.

## What Students Will Build/Learn

- Trace movie CRUD behavior with class-based views.
- Trace review and comment actions with function-based views.
- Understand staff-only vs owner-only authorization rules.
- Understand how Django messages are generated and rendered globally.

## Project Files Covered

- `blog/views.py`
- `blog/urls.py`
- `blog/templates/blog/movie_list.html`
- `blog/templates/blog/movie_detail.html`
- `blog/templates/blog/movie_form.html`
- `blog/templates/blog/movie_confirm_delete.html`
- `blog/templates/blog/base.html`

## Step-by-Step Explanation

1. Movie CRUD mapping (staff-only):
   - list: `MovieListView` (public read)
   - detail: `MovieDetailView` (public read)
   - create: `MovieCreateView` (`StaffRequiredMixin`)
   - update: `MovieUpdateView` (`StaffRequiredMixin`)
   - delete: `MovieDeleteView` (`StaffRequiredMixin`).
2. Review flow:
   - add/update review: `add_or_update_movie_review` (one review per user per movie)
   - delete review: `delete_movie_review` (owner or staff).
3. Comment flow:
   - add comment: `add_movie_comment`
   - edit comment: `edit_movie_comment` (owner or staff)
   - delete comment: `delete_movie_comment` (owner or staff).
4. Gallery flow (staff-only):
   - add image: `add_movie_image`
   - delete image: `delete_movie_image`.
5. Messages flow:
   - success/error messages created in views.
   - messages rendered in `blog/templates/blog/base.html`.
6. Aggregation on movie pages:
   - average rating and rating count shown on list/detail pages.

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-editing/>
- <https://docs.djangoproject.com/en/5.1/topics/auth/default/#limiting-access-to-logged-in-users>
- <https://docs.djangoproject.com/en/5.1/ref/contrib/messages/>
- <https://docs.djangoproject.com/en/5.1/topics/http/shortcuts/>

## Common Mistakes

- Using only login checks when a staff/owner check is also required.
- Forgetting to use POST for delete actions.
- Allowing duplicate review rows instead of update-on-resubmit.
- Not showing message feedback after create/update/delete actions.

## Exercise

1. Add a staff-only genre filter page for movies.
2. Add a minimum-rating filter (`>=4`) and show filtered results.
3. Keep all permission checks unchanged (non-staff cannot manage movies).

## Expected Result

- Students can explain the permission matrix:
  - public read
  - authenticated write for own content
  - staff moderation and movie management
- Students can trace one complete interaction from URL -> view -> DB -> message -> template output.

### Quick Recap

Secure CRUD is not only about create/update/delete. It also requires role checks, ownership rules, and clear user feedback on every action.
