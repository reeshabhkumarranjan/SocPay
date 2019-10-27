from django.shortcuts import render, redirect

# Create your views here.
from main_app import utils
from main_app.models import Post


def timeline(request):
    all_posts = Post.objects.filter(recipient_name=request.user.username).order_by('-post_date')
    context = {'forloop' : range(100), 'all_posts' : all_posts}
    return render(request, 'timeline.html', context=context)

def friends(request):
    if request.method == 'POST':
        pass # TODO complete this
    # all_friends = Friend.objects.all(creator__id=)
    all_friends = utils.get_friends(request.user)
    all_strangers = utils.get_not_friends(request.user)
    all_requests_sent = utils.get_sent_requests(request.user)
    all_requests_received = utils.get_received_requests(request.user)
    context = {'all_friends' : all_friends, 'all_strangers' : all_strangers, 'all_requests_sent' : all_requests_sent, 'all_requests_received' : all_requests_received}
    return render(request, 'friends.html', context=context)

def add_post(request):
    # TODO add checks
    author_name = request.user.username
    recipient_name = request.user.username
    post_text = request.POST.get('post_text', "N/A")

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('friends:timeline')

def add_post_friend(request, friend_username):
    # TODO add checks
    author_name = request.user.username
    recipient_name = friend_username
    post_text = request.POST.get('post_text', "N/A")

    Post.objects.create(author_name=author_name, recipient_name=recipient_name, post_text=post_text)
    return redirect('friends:friend_timeline', friend_username=friend_username)
    # return redirect('https://google.com')

def friend_timeline(request, friend_username):
    all_posts = Post.objects.filter(recipient_name=friend_username).order_by('-post_date')
    context = {'friend_username' : friend_username, 'all_posts' : all_posts}
    return render(request, '../friends/templates/friend_timeline.html', context=context)
