from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view( template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/new/', views.MovieCreateView.as_view(), name='movie-create'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),
    path('movies/<int:pk>/review/', views.add_or_update_movie_review, name='movie-review'),
    path('reviews/<int:pk>/delete/', views.delete_movie_review, name='movie-review-delete'),
    path('movies/<int:pk>/comment/', views.add_movie_comment, name='movie-comment-add'),
    path('movie-comments/<int:pk>/edit/', views.edit_movie_comment, name='movie-comment-edit'),
    path('movie-comments/<int:pk>/delete/', views.delete_movie_comment, name='movie-comment-delete'),
    path('movies/<int:pk>/gallery/add/', views.add_movie_image, name='movie-image-add'),
    path('movie-images/<int:pk>/delete/', views.delete_movie_image, name='movie-image-delete'),
]
