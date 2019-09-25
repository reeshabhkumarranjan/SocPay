from django.shortcuts import render


# Create your views here.


def login(request):
    """This is only to display login page."""
    return render(request, 'login.html')


def login_form(request):
    """This handles a login request."""
    # TODO complete this method
    username = request.POST["username"]
    password = request.POST["password"]
    context = {'test_string' : username + " " + password}

    return render(request, 'dummy.html', context=context)


def register(request):
    """This just displays the register page."""
    return render(request, 'register.html')


def register_form(request):
    """This handles the register request."""
    # TODO complete this method
    name = request.POST["name"]
    email = request.POST["email"]
    dob = request.POST["dob"]
    username = request.POST["username"]

    context = {'test_string' : name + " " + email + " " + dob + " " + username}

    return render(request, 'dummy.html', context = context)


def index(request):
    return render(request, 'index.html')
