"""Module for defining models related to the blog app."""

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    """Model representing a tag used in blog posts."""
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        """Return the name of the tag as its string representation."""
        return self.name
class Post(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        """Return the title of the post as its string representation."""
        return self.title

    def like_count(self):
        """Return the number of likes for the post."""
        return self.liked_by.count()

class Profile(models.Model):
    """Model representing a user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    liked_tags = models.ManyToManyField('Tag', related_name='liked_by')

    def __str__(self):
        """Return the username + profile."""
        return f'{self.user.username} Profile'
