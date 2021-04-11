import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import BlogForm
from .models import Blog
from .serializers import (
    BlogSerializer,
    BlogActionSerializer,
    BlogCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "pages/home.html", context={"username": username}, status=200)


@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
def blog_create_view(request, *args, **kwargs):
    serializer = BlogCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def blog_detail_view(request, blog_id, *args, **kwargs):
    qs = Blog.objects.filter(id=blog_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = BlogSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def blog_delete_view(request, blog_id, *args, **kwargs):
    qs = Blog.objects.filter(id=blog_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this blog"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Blog removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blog_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, repost
    '''
    serializer = BlogActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        blog_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Blog.objects.filter(id=blog_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = BlogSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = BlogSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "repost":
            new_blog = Blog.objects.create(
                    user=request.user,
                    parent=obj,
                    content=content,
                    )
            serializer = BlogSerializer(new_blog)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


@api_view(['GET'])
def blog_list_view(request, *args, **kwargs):
    qs = Blog.objects.all()
    username = request.GET.get('username') # ?username=Justin
    if username != None:
        qs = qs.filter(user__username__iexact=username)
    serializer = BlogSerializer(qs, many=True)
    return Response( serializer.data, status=200)



def blog_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API Create View -> DRF
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = BlogForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = BlogForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def blog_list_view_pure_django(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    qs = Blog.objects.all()
    blogs_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": blogs_list
    }
    return JsonResponse(data)


def blog_detail_view_pure_django(request, blog_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": blog_id,
    }
    status = 200
    try:
        obj = Blog.objects.get(id=blog_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json'
