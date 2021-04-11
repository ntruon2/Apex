from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include # url()
from django.views.generic import TemplateView

from blogs.views import (
    home_view,
    blog_action_view,
    blog_delete_view,
    blog_detail_view,
    blog_list_view,
    blog_create_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('react/', TemplateView.as_view(template_name='react_via_dj.html')),
    path('create-blog', blog_create_view),
    path('blogs', blog_list_view),
    path('blogs/<int:blog_id>', blog_detail_view),
    path('api/blogs/', include('blogs.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                document_root=settings.STATIC_ROOT)
