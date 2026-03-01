import shutil
from io import BytesIO
from tempfile import mkdtemp

from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Movie, MovieComment, MovieImage, MovieReview


def build_test_image(name='test.jpg', color=(200, 50, 50)):
    buffer = BytesIO()
    image = Image.new('RGB', (20, 20), color)
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type='image/jpeg')


class MovieBaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._temp_media = mkdtemp()
        cls._media_override = override_settings(MEDIA_ROOT=cls._temp_media)
        cls._media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._media_override.disable()
        shutil.rmtree(cls._temp_media, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff',
            password='Pass12345!',
            is_staff=True,
        )
        self.user = User.objects.create_user(username='user1', password='Pass12345!')
        self.other_user = User.objects.create_user(username='user2', password='Pass12345!')
        self.movie = Movie.objects.create(
            title='Inception',
            description='Sci-fi thriller',
            year=2010,
            genre='Sci-Fi',
            duration_minutes=148,
            director='Christopher Nolan',
            cover=build_test_image('cover.jpg'),
        )


class MovieModelTests(MovieBaseTestCase):
    def test_movie_get_absolute_url(self):
        self.assertEqual(
            self.movie.get_absolute_url(),
            reverse('movie-detail', kwargs={'pk': self.movie.pk}),
        )

    def test_review_unique_constraint_per_user_and_movie(self):
        MovieReview.objects.create(movie=self.movie, user=self.user, stars=4)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                MovieReview.objects.create(movie=self.movie, user=self.user, stars=5)

    def test_review_stars_validation_range(self):
        review = MovieReview(movie=self.movie, user=self.user, stars=6)
        with self.assertRaises(ValidationError):
            review.full_clean()


class MoviePermissionTests(MovieBaseTestCase):
    def test_anonymous_can_view_movie_list_and_detail(self):
        response_list = self.client.get(reverse('movie-list'))
        response_detail = self.client.get(reverse('movie-detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response_list.status_code, 200)
        self.assertEqual(response_detail.status_code, 200)

    def test_anonymous_cannot_post_review_or_comment(self):
        review_response = self.client.post(
            reverse('movie-review', kwargs={'pk': self.movie.pk}),
            {'stars': 5},
        )
        comment_response = self.client.post(
            reverse('movie-comment-add', kwargs={'pk': self.movie.pk}),
            {'content': 'Great movie!'},
        )
        self.assertEqual(review_response.status_code, 302)
        self.assertEqual(comment_response.status_code, 302)

    def test_non_staff_cannot_access_movie_management_pages(self):
        self.client.login(username='user1', password='Pass12345!')
        response_create = self.client.get(reverse('movie-create'))
        response_update = self.client.get(reverse('movie-update', kwargs={'pk': self.movie.pk}))
        response_delete = self.client.get(reverse('movie-delete', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response_create.status_code, 403)
        self.assertEqual(response_update.status_code, 403)
        self.assertEqual(response_delete.status_code, 403)

    def test_owner_can_edit_and_delete_own_comment_and_review(self):
        self.client.login(username='user1', password='Pass12345!')
        self.client.post(reverse('movie-review', kwargs={'pk': self.movie.pk}), {'stars': 4})
        self.client.post(
            reverse('movie-comment-add', kwargs={'pk': self.movie.pk}),
            {'content': 'Very nice film.'},
        )
        review = MovieReview.objects.get(movie=self.movie, user=self.user)
        comment = MovieComment.objects.get(movie=self.movie, user=self.user)

        edit_response = self.client.post(
            reverse('movie-comment-edit', kwargs={'pk': comment.pk}),
            {'content': 'Updated comment content.'},
        )
        self.assertEqual(edit_response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment content.')

        delete_review_response = self.client.post(
            reverse('movie-review-delete', kwargs={'pk': review.pk}),
        )
        delete_comment_response = self.client.post(
            reverse('movie-comment-delete', kwargs={'pk': comment.pk}),
        )
        self.assertEqual(delete_review_response.status_code, 302)
        self.assertEqual(delete_comment_response.status_code, 302)
        self.assertFalse(MovieReview.objects.filter(pk=review.pk).exists())
        self.assertFalse(MovieComment.objects.filter(pk=comment.pk).exists())

    def test_non_owner_cannot_modify_other_user_review_or_comment(self):
        review = MovieReview.objects.create(movie=self.movie, user=self.user, stars=5)
        comment = MovieComment.objects.create(movie=self.movie, user=self.user, content='Owner comment')

        self.client.login(username='user2', password='Pass12345!')
        review_delete_response = self.client.post(
            reverse('movie-review-delete', kwargs={'pk': review.pk}),
        )
        comment_edit_response = self.client.post(
            reverse('movie-comment-edit', kwargs={'pk': comment.pk}),
            {'content': 'Trying to edit'},
        )
        comment_delete_response = self.client.post(
            reverse('movie-comment-delete', kwargs={'pk': comment.pk}),
        )

        self.assertEqual(review_delete_response.status_code, 403)
        self.assertEqual(comment_edit_response.status_code, 403)
        self.assertEqual(comment_delete_response.status_code, 403)
        self.assertTrue(MovieReview.objects.filter(pk=review.pk).exists())
        self.assertTrue(MovieComment.objects.filter(pk=comment.pk).exists())

    def test_staff_can_moderate_review_and_comment(self):
        review = MovieReview.objects.create(movie=self.movie, user=self.user, stars=2)
        comment = MovieComment.objects.create(movie=self.movie, user=self.user, content='Needs improvement')

        self.client.login(username='staff', password='Pass12345!')
        review_delete_response = self.client.post(
            reverse('movie-review-delete', kwargs={'pk': review.pk}),
        )
        comment_delete_response = self.client.post(
            reverse('movie-comment-delete', kwargs={'pk': comment.pk}),
        )

        self.assertEqual(review_delete_response.status_code, 302)
        self.assertEqual(comment_delete_response.status_code, 302)
        self.assertFalse(MovieReview.objects.filter(pk=review.pk).exists())
        self.assertFalse(MovieComment.objects.filter(pk=comment.pk).exists())


class MovieFeatureFlowTests(MovieBaseTestCase):
    def test_staff_can_create_movie_with_cover(self):
        self.client.login(username='staff', password='Pass12345!')
        response = self.client.post(
            reverse('movie-create'),
            {
                'title': 'Interstellar',
                'description': 'Space exploration story',
                'year': 2014,
                'genre': 'Sci-Fi',
                'duration_minutes': 169,
                'director': 'Christopher Nolan',
                'cover': build_test_image('interstellar.jpg', color=(30, 60, 90)),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(title='Interstellar').exists())

    def test_staff_can_add_gallery_image(self):
        self.client.login(username='staff', password='Pass12345!')
        response = self.client.post(
            reverse('movie-image-add', kwargs={'pk': self.movie.pk}),
            {'image': build_test_image('gallery.jpg', color=(10, 120, 10)), 'caption': 'Scene image'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MovieImage.objects.filter(movie=self.movie).count(), 1)

    def test_review_upsert_creates_single_row_per_user(self):
        self.client.login(username='user1', password='Pass12345!')
        self.client.post(reverse('movie-review', kwargs={'pk': self.movie.pk}), {'stars': 3})
        self.client.post(reverse('movie-review', kwargs={'pk': self.movie.pk}), {'stars': 5})

        self.assertEqual(MovieReview.objects.filter(movie=self.movie, user=self.user).count(), 1)
        self.assertEqual(
            MovieReview.objects.get(movie=self.movie, user=self.user).stars,
            5,
        )

    def test_comment_add_edit_delete_flow(self):
        self.client.login(username='user1', password='Pass12345!')
        add_response = self.client.post(
            reverse('movie-comment-add', kwargs={'pk': self.movie.pk}),
            {'content': 'Initial comment'},
        )
        self.assertEqual(add_response.status_code, 302)
        comment = MovieComment.objects.get(movie=self.movie, user=self.user)

        edit_response = self.client.post(
            reverse('movie-comment-edit', kwargs={'pk': comment.pk}),
            {'content': 'Edited comment text'},
        )
        self.assertEqual(edit_response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Edited comment text')

        delete_response = self.client.post(
            reverse('movie-comment-delete', kwargs={'pk': comment.pk}),
        )
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(MovieComment.objects.filter(pk=comment.pk).exists())

    def test_movie_list_and_detail_render_rating_info(self):
        MovieReview.objects.create(movie=self.movie, user=self.user, stars=4)
        MovieReview.objects.create(movie=self.movie, user=self.other_user, stars=2)

        list_response = self.client.get(reverse('movie-list'))
        detail_response = self.client.get(reverse('movie-detail', kwargs={'pk': self.movie.pk}))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(list_response, 'Average Rating')
        self.assertContains(list_response, '(2 ratings)')
        self.assertContains(detail_response, 'Gallery')
        self.assertContains(detail_response, 'Comments')
