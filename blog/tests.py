"""Module for testing blog functionalities."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Tag

User = get_user_model()

class BlogTests(TestCase):
    """TestCase class for blog operations."""

    def setUp(self):
        """Set up data for the blog tests."""
        # Create users
        self.user1 = User.objects.create_user(username='testuser1', password='abc123')
        self.user2 = User.objects.create_user(username='testuser2', password='abc123')

        # Create tags
        self.tag1 = Tag.objects.create(name='Django')
        self.tag2 = Tag.objects.create(name='Testing')

        # Create a blog post with tags
        self.post = Post.objects.create(
            author=self.user1, title='Blog title', content='Body content...'
        )
        self.post.tags.add(self.tag1, self.tag2)

    def test_signup(self):
        """Test user signup."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        """Test user login."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser1',
            'password': 'abc123'
        })
        self.assertEqual(response.status_code, 200)  # OK status
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout(self):
        """Test user logout."""
        self.client.login(username='testuser1', password='abc123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertTrue('_auth_user_id' not in self.client.session)

    def test_like_post_authenticated(self):
        """Test liking a post as an authenticated user."""
        self.client.login(username='testuser2', password='abc123')
        response = self.client.post(reverse('like-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.liked_by.filter(id=self.user2.id).exists())

    def test_like_post_unauthenticated(self):
        """Test liking a post as an unauthenticated user."""
        response = self.client.post(reverse('like-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_post_owner(self):
        """Test editing a post by the owner."""
        self.client.login(username='testuser1', password='abc123')
        response = self.client.post(reverse('edit-post', args=[self.post.id]), {
            'title': 'Updated title',
            'content': 'Updated content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to post detail
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated title')
        self.assertEqual(self.post.content, 'Updated content')

    def test_delete_post_owner(self):
        """Test deleting a post by the owner."""
        self.client.login(username='testuser1', password='abc123')
        response = self.client.post(reverse('delete-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_user_settings_update_profile(self):
        """Test updating user settings and profile."""
        self.client.login(username='testuser1', password='abc123')
        response = self.client.post(reverse('handle-profile-update'), {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@example.com',
            'phone': '1234567890',
            'address': 'New Address'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'NewFirstName')
        self.assertEqual(self.user1.last_name, 'NewLastName')
        self.assertEqual(self.user1.email, 'newemail@example.com')
