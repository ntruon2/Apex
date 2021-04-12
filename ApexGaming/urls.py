from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include # url()
from django.views.generic import TemplateView

from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

from blogs.views import (
    blogs_list_view,
    blogs_detail_view,
    blogs_profile_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blogs_list_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('<int:blog_id>', blogs_detail_view),
    path('profile/<str:username>', blogs_profile_view),
    path('api/blogs/', include('blogs.api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                document_root=settings.STATIC_ROOT)
