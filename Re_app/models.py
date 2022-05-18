from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Userpost(models.Model):
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    post_user=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,blank=True,related_name='like')


class Comments(models.Model):
    body=models.CharField(max_length=100)
    comment_post=models.ForeignKey(Userpost,on_delete=models.CASCADE)


class Profile(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    followers=models.ManyToManyField(User,blank=True,related_name="follower")
    followings=models.ManyToManyField(User,blank=True,related_name='following')

    def __str__(self):
        return f"{self.user.username} {self.user.id}"
