from django.shortcuts import render

# Create your views here.

def exception(request):
    return render(request, 'exception_html', name='exception')