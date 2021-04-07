from django.contrib import admin

# Register your models here.
from .models import Blog, BlogLike


class BlogLikeAdmin(admin.TabularInline):
    model = BlogLike

class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Blog

admin.site.register(Blog, BlogAdmin)
