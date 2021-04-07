import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class BlogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # many users can many blogs
    likes = models.ManyToManyField(User, related_name='blog_user', blank=True, through=BlogLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_repost(self):
        return self.parent != None

    def serialize(self):
        '''
        Feel free to delete!
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
