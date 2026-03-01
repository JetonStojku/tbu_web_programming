from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (Comment, Movie, MovieComment, MovieImage, MovieReview, Post)

MOVIE_STAR_CHOICES = [(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': 'min-height: 200px;',
                'placeholder': 'Write your post content here'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your comment...'}),
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters.")
        return content
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'description',
            'year',
            'genre',
            'duration_minutes',
            'director',
            'cover',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1888}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drama, Action, ...'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director name'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class MovieImageForm(forms.ModelForm):
    class Meta:
        model = MovieImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional caption'}),
        }


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['stars']
        widgets = {
            'stars': forms.Select(
                choices=MOVIE_STAR_CHOICES,
                attrs={'class': 'form-select'},
            ),
        }

    def clean_stars(self):
        stars = self.cleaned_data.get('stars')
        if stars is None or stars < 1 or stars > 5:
            raise forms.ValidationError('Stars must be between 1 and 5.')
        return stars


class MovieCommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Write your comment...',
                }
            ),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content
