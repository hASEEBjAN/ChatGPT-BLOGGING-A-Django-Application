"""Module for handling signals related to the User model."""

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
    """
    Create a profile for each new user.
    
    Args:
        instance (User): The user instance.
        created (bool): Flag that indicates if the user was created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(instance, **kwargs):
    """
    Save the profile associated with the user.
    
    Args:
        instance (User): The user instance.
    """
    instance.profile.save()
