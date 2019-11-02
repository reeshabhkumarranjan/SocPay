from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests

# Create your views here.
from django.urls import reverse

from commercial_page.models import getAllPages, CommercialPage, getAllPosts, CommercialPagePosts, getAllPagesGlobal, \
    isPageAdmin
from cse_345_fcs_course_project import settings
from main_app import utils


def page_list(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user.user_type != 5:
        raise PermissionDenied
    pages = getAllPages(request.user)
    context = {'pages' : pages}
    return render(request, 'page_list.html', context=context)

def page_timeline(request, page_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    # if request.user.user_type != 5:
    #     raise PermissionDenied
    # page_id = request.POST.get("page_id", "null")
    page = CommercialPage.objects.get(id=page_id)
    context = {}
    context['page'] = page
    context['posts'] = getAllPosts(page).order_by('-date')
    is_admin = isPageAdmin(request.user, page)
    context['is_admin'] = is_admin
    return render(request, 'page_timeline.html', context=context)

def page_list_global(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    pages = getAllPagesGlobal()
    context = {'pages':pages}
    return render(request, 'page_list_global.html', context=context)

def add_post(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user.user_type != 5:
        raise PermissionDenied
    page_id = request.POST.get("page_id", "null")
    page = CommercialPage.objects.get(id=page_id)
    if not isPageAdmin(request.user, page):
        raise PermissionDenied
    utils.check_captcha(request)
    post_text = request.POST.get("post_text", "null")
    CommercialPagePosts.objects.create(page=page, post_text=post_text)
    return HttpResponseRedirect(reverse('commercial_page:page_timeline', kwargs={'page_id' : page_id}))

def add_page(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user.user_type != 5:
        raise PermissionDenied
    # if request.method == 'POST':
    #     recaptcha_response = request.POST.get('g-recaptcha-response')
    #     data = {
    #         'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
    #         'response': recaptcha_response
    #     }
    #     result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data).json()
    #     if not result['success']:
    #         raise PermissionDenied
    utils.check_captcha(request)
    page_name = request.POST.get("page_name", "null")
    admin = request.user
    description = request.POST.get("description", "null")
    CommercialPage.objects.create(page_name=page_name, admin=admin, description=description)
    return HttpResponseRedirect(reverse('commercial_page:page_list'))

def add_page_form(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user.user_type != 5:
        raise PermissionDenied
    return render(request, 'add_page_form.html')
