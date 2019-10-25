from django.db import models

from users.models import CustomUser


class CommercialPage(models.Model):
    page_name = models.CharField(default="", max_length=100)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(default="", max_length=200)


class CommercialPagePosts(models.Model):
    page = models.ForeignKey(CommercialPage, on_delete=models.CASCADE)
    post_text = models.CharField(default="", max_length=100)
    date = models.DateTimeField(auto_now_add=True)


def getAllPages(user):
    pages = CommercialPage.objects.filter(admin=user)
    return pages


def getAllPosts(page):
    posts = CommercialPagePosts.objects.filter(page=page)
    return posts

