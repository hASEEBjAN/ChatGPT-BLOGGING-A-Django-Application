"""URL configurations for the blog application."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'),
    path('post/new/', views.publish_post, name='publish-post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit-post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete-post'),
    path('settings/', views.settings, name='settings'),
    path('user/<int:user_id>/posts/', views.user_posts, name='user-posts'),
    path('settings/update_profile/', views.handle_profile_update, name='handle-profile-update'),
    path('settings/change_password/', views.handle_password_change, name='handle-password-change'),
    path('settings/update_email/', views.handle_email_update, name='handle-email-update'),
    path('settings/delete_account/', views.handle_account_delete, name='handle-account-delete'),
    path('tags/<str:tag_name>/', views.tagged_posts, name='tagged-posts'),
    path('additional-details/', views.additional_details, name='additional-details')
]
