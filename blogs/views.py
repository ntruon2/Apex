import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "pages/home.html", context={"username": username}, status=200)

def blogs_list_view(request, *args, **kwargs):
    return render(request, "blogs/list.html")

def blogs_detail_view(request, blog_id, *args, **kwargs):
    return render(request, "blogs/detail.html", context={"blog_id": blog_id})

def blogs_profile_view(request, username, *args, **kwargs):
    return render(request, "blogs/profile.html", context={"profile_username": username})
