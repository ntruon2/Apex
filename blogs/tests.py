from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Blog
# Create your tests here.
User = get_user_model()

class BlogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jnt', password='somepassword')
        self.userb = User.objects.create_user(username='jnt-2', password='somepassword2')
        Blog.objects.create(content="my first post",
            user=self.user)
        Blog.objects.create(content="my first post",
            user=self.user)
        Blog.objects.create(content="my first post",
            user=self.userb)
        self.currentCount = Blog.objects.all().count()

    def test_blog_created(self):
        blog_obj = Blog.objects.create(content="my second post",
            user=self.user)
        self.assertEqual(blog_obj.id, 4)
        self.assertEqual(blog_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_blog_list(self):
        client = self.get_client()
        response = client.get("/api/blogs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_blog_list(self):
        client = self.get_client()
        response = client.get("/api/blogs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/blogs/action/",
            {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/blogs/action/",
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/blogs/action/",
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)

    def test_action_repost(self):
        client = self.get_client()
        response = client.post("/api/blogs/action/",
            {"id": 2, "action": "repost"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_blog_id = data.get("id")
        self.assertNotEqual(2, new_blog_id)
        self.assertEqual(self.currentCount + 1, new_blog_id)

    def test_blog_create_api_view(self):
        request_data = {"content": "This is my test post"}
        client = self.get_client()
        response = client.post("/api/blogs/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_blog_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_blog_id)

    def test_blog_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/blogs/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_blog_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/blogs/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/blogs/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/blogs/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)
