from django.shortcuts import render

def register(request):
    """This just displays the register page."""
    return render(request, 'register.html')


def login(request):
    """This just displays the register page."""
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')
