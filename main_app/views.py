from django.shortcuts import render
from .models import Post

def register(request):
    """This just displays the register page."""
    return render(request, 'register.html')


def login(request):
    """This just displays the register page."""
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')

def timeline(request):
    all_posts = Post.objects.all()
    context = {'forloop' : range(100), 'all_posts' : all_posts}
    return render(request, 'timeline.html', context=context)