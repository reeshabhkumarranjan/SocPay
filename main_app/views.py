from django.shortcuts import render

def register(request):
    """This just displays the register page."""
    return render(request, 'register.html')


def login(request):
    """This just displays the register page."""
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')

def timeline(request):
    context = {'forloop' : range(100)}
    return render(request, 'timeline.html', context=context)