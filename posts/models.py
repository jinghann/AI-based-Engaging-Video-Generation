# To use MongoDB
from djongo import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length= 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #date created
    is_private = models.BooleanField() #private/public post
    video = models.FileField(upload_to="postVideos/")
    AI_algo = models.TextField(default="None")
    AI_seq = models.TextField(default="None")
    cust_seq = models.TextField(default="None")
    cust_dur = models.TextField(default="None")
    cust_speed = models.TextField(default="None")
    author = models.ForeignKey(User, on_delete =  models.CASCADE) #if the user who created the post is deleted, the post is then deleted.

    def __str__(self):
        return self.title+' by '+self.author.username

class PostFile(models.Model):
    file = models.FileField(upload_to='postFiles/')
    post = models.ForeignKey(Post,on_delete=models.CASCADE) # post files will be deleted when a post is deleted

    def __str__(self):
        return self.file.url


class Comment(models.Model):
    content = models.TextField(max_length= 200)
    date_commented = models.DateTimeField(default=timezone.now) #date created
    post = models.ForeignKey(Post,on_delete =  models.CASCADE) # if post is deleted, comments will be deleted
    author = models.ForeignKey(User, on_delete =  models.CASCADE) #if the user who created the post is deleted, the post is then deleted.

    def __str__(self):
        return 'To post '+self.post.title+' by '+self.author.username
