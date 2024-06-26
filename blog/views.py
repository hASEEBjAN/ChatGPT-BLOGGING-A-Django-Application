"""Module for handling views in the blog application."""
import re
from urllib.parse import unquote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction, IntegrityError
from .models import Post, Profile, Tag, User
from .gpt_blog_generator.openai_integration import BlogContentGenerator

def home(request):
    """Render the home page with a list of posts."""
    posts = Post.objects.all()
    for post in posts:
        post.author_display = (
            f"{post.author.first_name} {post.author.last_name}"
            if post.author.first_name and post.author.last_name
            else post.author.username
        )
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)


def about(request):
    """Render the about page."""
    return render(request, 'blog/about.html', {'title': 'About'})

def signup(request):
    """Handle user signup via a form."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                return redirect('additional-details')  # Redirect to additional details or home
            except IntegrityError:
                return render(request, 'blog/signup.html', {'error': 'Username already exists'})
        else:
            return render(request, 'blog/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'blog/signup.html')

@login_required
def additional_details(request):
    """Handle additional profile detail of user on signup via a form."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.profile_picture = request.FILES.get('profile_picture')
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.save()

        tags = request.POST.get('tags', '')
        tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
        profile.liked_tags.clear()  # Clear existing tags before adding new ones
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            profile.liked_tags.add(tag)

        return redirect('blog-home')

    return render(request, 'blog/additional_details.html')

def login_view(request):
    """Handle user login and generate a blog post on successful login."""
    if request.method != 'POST':
        return render(request, 'blog/login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, 'blog/login.html', {'error': 'Invalid username or password'})

    login(request, user)
    # Extract tags from the user's liked tags
    blog_content = BlogContentGenerator().generate_blog_content(
        ','.join(tag.name for tag in user.profile.liked_tags.all())
    )
    # Use regex to extract title, tags, and content
    title_match = re.search(r"Title: (.+)", blog_content)
    tags_match = re.search(r"Tags: (.+)", blog_content)
    content_match = re.search(r"\n\n([\s\S]+)", blog_content)

    if not (title_match and tags_match and content_match):
        return render(request, 'blog/login.html', {'error': 'Error generating post content'})

    # Create a new post with the extracted title and content
    post = Post.objects.create(author=user,
                               title=title_match.group(1),
                               content=content_match.group(1))

    for tag_name in tags_match.group(1).split(', '):
        tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
        post.tags.add(tag)

    return redirect('blog-home')

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('blog-home')

@login_required
def like_post(request, post_id):
    """Allow users to like or unlike a post."""
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
        liked = False
    else:
        post.liked_by.add(request.user)
        liked = True
    post.save()
    return JsonResponse({'liked': liked, 'like_count': post.liked_by.count()})

def post_detail(request, post_id):
    """Render the detail view of a post."""
    post = get_object_or_404(Post, id=post_id)
    post.author_display = (
        f"{post.author.first_name} {post.author.last_name}"
        if post.author.first_name and post.author.last_name
        else post.author.username
    )
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)

def user_posts(request, user_id):
    """Display all posts by a specific user."""
    posts = Post.objects.filter(author_id=user_id)
    for post in posts:
        post.author_display = (
            f"{post.author.first_name} {post.author.last_name}"
            if post.author.first_name and post.author.last_name
            else post.author.username
        )
    context = {'posts': posts}
    return render(request, 'blog/user_posts.html', context)

def tagged_posts(request, tag_name):
    """Display all posts associated with a specific tag."""
    # Decode the URL-encoded tag name
    tag_name = unquote(tag_name)
    posts = Post.objects.filter(tags__name=tag_name)
    context = {'posts': posts, 'tag_name': tag_name}
    return render(request, 'blog/tagged_posts.html', context)

@login_required
def publish_post(request):
    """Allow users to publish a new post."""
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        tag_names = request.POST.get('tags', '').split(',')
        with transaction.atomic():
            post = Post.objects.create(title=title, content=content, author=request.user)
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                post.tags.add(tag)
        return redirect('post-detail', post_id=post.id)
    return render(request, 'blog/publish_post.html')

@login_required
def edit_post(request, post_id):
    """Allow users to edit their post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.tags.clear()
        tag_names = request.POST.get('tags', '').split(',')
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
            post.tags.add(tag)
        post.save()
        return redirect('post-detail', post_id=post.id)
    existing_tags = ', '.join(tag.name for tag in post.tags.all())
    context = {'post': post, 'existing_tags': existing_tags}
    return render(request, 'blog/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """Allow users to delete their post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog-home')
    post.author_display = (
        f"{post.author.first_name} {post.author.last_name}"
        if post.author.first_name and post.author.last_name
        else post.author.username
    )
    context = {'post': post}
    return render(request, 'blog/confirm_delete.html', context)

@login_required
def settings(request):
    """Handle user settings based on the action specified."""
    action = request.GET.get('action', 'update_profile')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if action == 'update_profile':
            return render(request, 'blog/partials/update_profile.html', {'user': request.user})
        if action == 'change_password':
            return render(request, 'blog/partials/change_password.html', {'user': request.user})
        if action == 'update_email':
            return render(request, 'blog/partials/update_email.html', {'user': request.user})
        if action == 'delete_account':
            return render(request, 'blog/partials/delete_account.html', {'user': request.user})
    return render(request, 'blog/setting.html', {'user': request.user, 'action': action})

@login_required
def handle_password_change(request):
    """Allow users to change their password."""
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if password == password_confirm:
            user.set_password(password)
            user.save()
            return redirect('blog-home')
    return render(request, 'blog/setting.html', {
        'user': request.user,
        'action': 'change_password'
    })

@login_required
def handle_email_update(request):
    """Allow users to update their email address."""
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        user.email = email
        user.save()
        return redirect('blog-home')
    return render(request, 'blog/setting.html', {
        'user': request.user,
        'action': 'update_email'
    })

@login_required
def handle_account_delete(request):
    """Allow users to delete their account."""
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('blog-home')
    return render(request, 'blog/setting.html', {
        'user': request.user,
        'action': 'delete_account'
    })

@login_required
def handle_profile_update(request):
    """Allow users to update their profile information including liked tags."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Handling tag updates
        tags = request.POST.get('tags', '')
        tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
        profile.liked_tags.clear()  # Clear existing tags before adding new ones
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            profile.liked_tags.add(tag)

        user.save()
        profile.save()
        return redirect('blog-home')
    return render(request, 'blog/setting.html', {
        'user': request.user,
        'action': 'update_profile'
    })
