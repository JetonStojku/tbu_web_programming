# Lesson 07: CRUD, Comments, Permissions, and Messages

## Lesson Goal

Understand CRUD flow implementation and identify permission/message gaps that should be improved.

## What Students Will Build/Learn

- Trace complete post CRUD behavior in class-based views.
- Trace comment create/delete behavior in function-based views.
- Understand ownership checks and where they are missing.
- Understand Django messages lifecycle and template rendering requirement.

## Project Files Covered

- `blog/views.py`
- `blog/urls.py`
- `blog/templates/blog/post_detail.html`
- `blog/templates/blog/post_confirm_delete.html`
- `blog/templates/blog/base.html`

## Step-by-Step Explanation

1. Post CRUD mapping:
   - list: `PostListView`
   - detail: `PostDetailView`
   - create: `PostCreateView`
   - update: `PostUpdateView`
   - delete: `PostDeleteView`.
2. Comment flow mapping:
   - add comment: `add_comment`
   - delete comment: `comment_delete`.
3. Ownership and authorization currently implemented:
   - `PostDeleteView.get_queryset()` filters by current author.
   - `comment_delete` checks `request.user == comment.author`.
4. Messages usage in views:
   - success/error messages created via `django.contrib.messages`.
5. Essential gaps in the current codebase (must be addressed in future improvement):
   1. `PostUpdateView` is missing author restriction.
   2. `blog/templates/blog/post_confirm_delete.html` is empty.
   3. Messages are created in views but not rendered in `blog/templates/blog/base.html`.
   4. `post_detail.html` checks `comment_form.content.errors`, but `PostDetailView` does not provide `comment_form` context.

## Django Docs Used (5.1 links)

- <https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-editing/>
- <https://docs.djangoproject.com/en/5.1/ref/contrib/messages/>
- <https://docs.djangoproject.com/en/5.1/topics/http/shortcuts/>
- <https://docs.djangoproject.com/en/5.1/topics/auth/default/>

## Common Mistakes

- Assuming login checks are enough without object ownership checks.
- Forgetting to render messages in a base template.
- Using detail templates with context variables never provided by the view.
- Leaving default/empty templates for critical operations like delete confirmation.

## Exercise

Choose one fix and implement it as homework:

- Option A: Restrict `PostUpdateView` to posts owned by the logged-in user.
- Option B: Render flash messages in `blog/templates/blog/base.html`.
- Option C: Add a proper delete confirmation template in `post_confirm_delete.html`.

## Expected Result

- Students can explain where permissions are enforced and where they are missing.
- Students can propose a clear fix for at least one identified gap.

### Quick Recap

CRUD works functionally, but secure and maintainable Django apps require consistent ownership checks, complete templates, and visible feedback messages.
