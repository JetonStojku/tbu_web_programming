from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Prefetch
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import (CommentForm, MovieCommentForm, MovieForm, MovieImageForm,
                        MovieReviewForm, PostForm, UserRegisterForm)

from .models import Comment, Movie, MovieComment, MovieImage, MovieReview, Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        if not hasattr(self, 'object') or not self.object.pk:
            return reverse('home')  # fallback if something went wrong
        return reverse('post-detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    
    def get_success_url(self):
        messages.success(self.request, 'Post has been deleted successfully!')
        return reverse('home')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class MovieListView(ListView):
    model = Movie
    template_name = 'blog/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return (
            Movie.objects.annotate(
                avg_rating=Avg('reviews__stars'),
                rating_count=Count('reviews', distinct=True),
            )
            .order_by('-created_at')
        )


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'blog/movie_detail.html'
    context_object_name = 'movie'

    def get_queryset(self):
        return (
            Movie.objects.annotate(
                avg_rating=Avg('reviews__stars'),
                rating_count=Count('reviews', distinct=True),
            )
            .prefetch_related(
                'gallery_images',
                Prefetch(
                    'movie_comments',
                    queryset=MovieComment.objects.select_related('user').order_by('-created_at'),
                ),
                Prefetch(
                    'reviews',
                    queryset=MovieReview.objects.select_related('user').order_by('-updated_at'),
                ),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.object
        user_review = None

        if self.request.user.is_authenticated:
            user_review = movie.reviews.filter(user=self.request.user).first()

        context['user_review'] = user_review
        context['review_form'] = MovieReviewForm(instance=user_review)
        context['comment_form'] = MovieCommentForm()
        context['image_form'] = MovieImageForm() if self.request.user.is_staff else None
        return context


class MovieCreateView(StaffRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'blog/movie_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Movie created successfully.')
        return response


class MovieUpdateView(StaffRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'blog/movie_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Movie updated successfully.')
        return response


class MovieDeleteView(StaffRequiredMixin, DeleteView):
    model = Movie
    template_name = 'blog/movie_confirm_delete.html'

    def get_success_url(self):
        return reverse('movie-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Movie deleted successfully.')
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def add_or_update_movie_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    existing_review = MovieReview.objects.filter(movie=movie, user=request.user).first()
    form = MovieReviewForm(request.POST, instance=existing_review)

    if form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.user = request.user
        review.save()
        if existing_review:
            messages.success(request, 'Your rating has been updated.')
        else:
            messages.success(request, 'Your rating has been added.')
    else:
        messages.error(request, 'Please submit a valid rating between 1 and 5.')

    return redirect('movie-detail', pk=movie.pk)


@login_required
@require_POST
def delete_movie_review(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    movie_pk = review.movie.pk

    if request.user != review.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return redirect('movie-detail', pk=movie_pk)


@login_required
@require_POST
def add_movie_comment(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        messages.success(request, 'Your comment has been added.')
    else:
        messages.error(request, 'Please provide a valid comment.')

    return redirect('movie-detail', pk=movie.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def edit_movie_comment(request, pk):
    comment = get_object_or_404(MovieComment, pk=pk)

    if request.user != comment.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == 'POST':
        form = MovieCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('movie-detail', pk=comment.movie.pk)
    else:
        form = MovieCommentForm(instance=comment)

    return render(
        request,
        'blog/movie_comment_form.html',
        {
            'form': form,
            'movie': comment.movie,
            'comment': comment,
        },
    )


@login_required
@require_POST
def delete_movie_comment(request, pk):
    comment = get_object_or_404(MovieComment, pk=pk)
    movie_pk = comment.movie.pk

    if request.user != comment.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    comment.delete()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('movie-detail', pk=movie_pk)


@login_required
@require_POST
def add_movie_image(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to manage movie images.")

    form = MovieImageForm(request.POST, request.FILES)
    if form.is_valid():
        movie_image = form.save(commit=False)
        movie_image.movie = movie
        movie_image.save()
        messages.success(request, 'Gallery image added successfully.')
    else:
        messages.error(request, 'Please provide a valid image.')

    return redirect('movie-detail', pk=movie.pk)


@login_required
@require_POST
def delete_movie_image(request, pk):
    movie_image = get_object_or_404(MovieImage, pk=pk)
    movie_pk = movie_image.movie.pk

    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete movie images.")

    movie_image.delete()
    messages.success(request, 'Gallery image deleted successfully.')
    return redirect('movie-detail', pk=movie_pk)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
        else:
            messages.error(request, 'Error adding your comment!')
    return redirect('post-detail', pk=post.pk)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
    else:
        messages.error(request, "You can't delete this comment!")
    return redirect('post-detail', pk=post_pk)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})
