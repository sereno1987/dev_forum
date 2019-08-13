from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

class Boards(models.Model):
    name=models.CharField(max_length=40,unique=True)
    description=models.CharField(max_length=200)


class Topics(models.Model):
    subject=models.CharField(max_length=225)
    last_update=models.DateTimeField()
    board=models.ForeignKey(Boards,related_name="topics",on_delete='cascade')
    creator=models.ForeignKey(User,related_name="topics", on_delete='cascade')



class Posts(models.Model):
    message=models.TextField(max_length=2000)
    topic=models.ForeignKey(Topics,related_name="posts",on_delete='cascade')
    Created_at=models.DateTimeField(auto_now_add=True)
    last_update=models.DateTimeField(null=True)
    creator=models.ForeignKey(User,related_name="posts",on_delete='cascade')
    updated_by=models.ForeignKey(User,related_name="posts_update",on_delete='cascade')