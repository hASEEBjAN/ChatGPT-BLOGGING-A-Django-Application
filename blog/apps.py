"""Module for configuring the blog app."""
from django.apps import AppConfig

class BlogConfig(AppConfig):
    """Configuration class for the blog app."""
    name = 'blog'

    def ready(self):
        """Method to import signals when the app is ready."""
        import blog.signals  # pylint: disable=unused-import
