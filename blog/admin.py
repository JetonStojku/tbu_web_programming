from django.contrib import admin

from .models import Comment, Movie, MovieComment, MovieImage, MovieReview, Post

admin.site.register(Post)
admin.site.register(Comment)


class MovieImageInline(admin.TabularInline):
    model = MovieImage
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'director', 'created_at')
    list_filter = ('genre', 'year', 'created_at')
    search_fields = ('title', 'director', 'description')
    inlines = [MovieImageInline]


@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'stars', 'updated_at')
    list_filter = ('stars', 'updated_at')
    search_fields = ('movie__title', 'user__username')


@admin.register(MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'created_at')
    search_fields = ('movie__title', 'user__username', 'content')
