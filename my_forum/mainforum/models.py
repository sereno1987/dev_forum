from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

class Boards(models.Model):
    name=models.CharField(max_length=40,unique=True)
    description=models.CharField(max_length=200)
    def __str__(self):
        return self.name

    def get_post_count(self):
        return Posts.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Posts.objects.filter(topic__board=self).order_by('-Created_at').first()


class Topics(models.Model):
    subject=models.CharField(max_length=225)
    last_update=models.DateTimeField(auto_now_add=True)
    board=models.ForeignKey(Boards,related_name="topics",on_delete='cascade')
    creator=models.ForeignKey(User,related_name="topics", on_delete='cascade')
    # as we call the string it will print the name
    def __str__(self):
        return self.subject

class Posts(models.Model):
    message=models.TextField(max_length=2000)
    topic=models.ForeignKey(Topics,related_name="posts",on_delete='cascade')
    Created_at=models.DateTimeField(auto_now_add=True)
    last_update=models.DateTimeField(auto_now_add=True)
    creator=models.ForeignKey(User,related_name="posts",on_delete='cascade')
    updated_by=models.ForeignKey(User,related_name="posts_update",on_delete='cascade')
    def __str__(self):
        truncated_message=Truncator(self.message)
        return truncated_message.chars(30)