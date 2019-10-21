from django.shortcuts import render, redirect

from main_app.models import Post
from users.models import Friend


def register(request):
    """This just displays the register page."""
    return render(request, 'signup.html')


def login(request):
    """This just displays the register page."""
    return render(request, 'registration/login.html')


def index(request):
    return render(request, 'index.html')

def timeline(request):
    all_posts = Post.objects.filter(author_name=request.user.username, recipient_name=request.user.username).order_by('-post_date')
    context = {'forloop' : range(100), 'all_posts' : all_posts}
    return render(request, 'timeline.html', context=context)

def friends(request):
    # all_friends = Friend.objects.all(creator__id=)
    all_friends = Friend.objects.filter(creator=request.user) | Friend.objects.filter(follower=request.user) & Friend.objects.filter(confirmed=True)
    context = {'all_friends' : all_friends}
    return render(request, 'friends.html', context=context)

def add_post(request):
    # TODO add checks
    author_name = request.user.username
    recipient_name = request.user.username
    post_text = request.POST.get('post_text', "N/A")

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('main_app:timeline')