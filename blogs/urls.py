from django.urls import path

from .views import (
    home_view,
    blog_action_view,
    blog_delete_view,
    blog_detail_view,
    blog_list_view,
    blog_create_view,
)
'''
CLIENT
Base ENDPOINT /api/blogs/
'''
urlpatterns = [
    path('', blog_list_view),
    path('action/', blog_action_view),
    path('create/', blog_create_view),
    path('<int:blog_id>/', blog_detail_view),
    path('<int:blog_id>/delete/', blog_delete_view),
]
