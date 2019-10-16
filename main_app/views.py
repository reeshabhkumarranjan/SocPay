from django.shortcuts import render

from main_app.models import Post


def register(request):
    """This just displays the register page."""
    return render(request, 'signup.html')


def login(request):
    """This just displays the register page."""
    return render(request, 'registration/login.html')


def index(request):
    return render(request, 'index.html')

def timeline(request):
    all_posts = Post.objects.all()
    context = {'forloop' : range(100), 'all_posts' : all_posts}
    return render(request, 'timeline.html', context=context)