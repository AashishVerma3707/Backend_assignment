from django.shortcuts import render, HttpResponse
import requests
from django.http import JsonResponse
from .models import Profile, Comments, Userpost
from rest_framework.decorators import api_view
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User

@api_view(('GET','POST'))

def authenticate(request):
    if request.method=='POST':
        user_email=request.POST['User_email']
        user_password=request.POST['User_password']
        user = auth.authenticate(username=user_email, password=user_password)


        if user is not None:
            auth.login(request, user)

        else:
            new_user = get_user_model().objects.create_user(username=user_email,password=user_password)
            new_user.save()
            auth.login(request, new_user)
            Profile.objects.create(user=new_user)
            print(new_user.id)

        url="http://127.0.0.1:8000/api/token/"
        refresh_url="http://127.0.0.1:8000/api/token/refresh/"
        response = requests.post(url, data={'username': user_email,'password': user_password})
        refresh_response=requests.post(refresh_url, data={'refresh':response.json()['refresh']})
        return JsonResponse({"JWT Token: ":refresh_response.json()['access']})
        # we will get refreshed Token in every time interval

    print("rrr", request.user.username,request.user.id)
    return render(request, 'index1.html')


@api_view(('GET',))
@permission_classes((IsAuthenticated, ))
def follow(request,pk):

    user=User.objects.get(id=pk)
    req_user=Profile.objects.get(user=user)
    req_user.followers.add(request.user)
    concurrent_profile=Profile.objects.get(user=request.user)
    concurrent_profile.followings.add(user)

    return HttpResponse(f"You've now started following {user.username}")


@api_view(('GET',))
@permission_classes((IsAuthenticated, ))
def unfollow(request,pk):

    user=User.objects.get(id=pk)
    req_user=Profile.objects.get(user=user)
    req_user.followers.remove(request.user)
    concurrent_profile=Profile.objects.get(user=request.user)
    concurrent_profile.followings.remove(user)

    return HttpResponse(f"You've now unfollowed {user.username}")


@api_view(("GET","POST"))
def get_user(request):
    if request.user.is_authenticated:
        req_user=Profile.objects.get(user=request.user)
        len_followers=len(req_user.followers.all())
        len_following=len(req_user.followings.all())
        return JsonResponse({"Username":req_user.user.username,
        "Number of followings":len_following,"Number of followers":len_followers})
    else:
        if request.method=='POST':
            user_email = request.POST['User_email']
            user_password = request.POST['User_password']
            user = auth.authenticate(username=user_email, password=user_password)

            if user is not None:
                auth.login(request, user)
                req_user = Profile.objects.get(user=user)
                len_followers = len(req_user.followers.all())
                len_following = len(req_user.followings.all())
                return JsonResponse({"Username": req_user.user.username,
                                     "Number of followings": len_following, "Number of followers": len_followers})
            else:
                return HttpResponse("user not found")

        return render(request,"index2.html")

@api_view(('GET','POST'))
@permission_classes((IsAuthenticated, ))
def create_post(request):
    if request.method=="POST":
        title=request.POST["title"]
        desc=request.POST['description']
        req_post=Userpost.objects.create(title=title,desc=desc,post_user=request.user)
        req_post.save()
        return JsonResponse({"Post Id":req_post.id,"Title":req_post.title,
                             "Description":req_post.desc,"Created time":req_post.created_at})

    return render(request,"index3.html")


@api_view(('DELETE',"GET",))
@permission_classes((IsAuthenticated, ))
def delete_post(request,pk):

    # Since there are different method for same the url.

    if request.method == "DELETE":
        req_post=Userpost.objects.get(id=pk)
        if req_post.post_user == request.user:
            req_post.delete()
            return HttpResponse("your post has been deleted")

    elif request.method == "GET":
        comment_list = []
        req_post = Userpost.objects.get(id=pk)
        number_likes = len(req_post.likes.all())
        req_comments = Comments.objects.filter(comment_post=req_post)
        for i in req_comments:
            comment_list.append(i.body)
        return JsonResponse({"Number of likes": number_likes, "comments": comment_list})


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def like(request,pk):
    req_post=Userpost.objects.get(id=pk)
    req_post.likes.add(request.user)
    print(req_post.likes.all())
    return HttpResponse(f"You've liked the post with id {pk} successfully")


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def unlike(request,pk):
    req_post = Userpost.objects.get(id=pk)
    req_post.likes.remove(request.user)
    print(req_post.likes.all())
    return HttpResponse(f"You've unliked the post with id {pk} successfully")


@api_view(("GET","POST"))
@permission_classes((IsAuthenticated,))
def add_comment(request , pk):
    if request.method == "POST":
        comment_body=request.POST["body"]
        req_userpost = Userpost.objects.get(id=pk)
        req_comment=Comments.objects.create(body=comment_body,comment_post=req_userpost)
        req_comment.save()
        return HttpResponse(req_comment.id)

    return render(request,"index4.html",{"pk":pk})


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def all_posts(request):
    post_list=[]
    req_post=Userpost.objects.filter(post_user=request.user).order_by('-created_at')
    for i in req_post:
        comment_list = []
        post_dict = {}
        post_dict["id"]=i.id
        post_dict["Title"]=i.title
        post_dict["desc"]=i.desc
        post_dict["created_at"]=i.created_at
        req_comments = Comments.objects.filter(comment_post=i)
        for comment in req_comments:
            comment_list.append(comment.body)
        post_dict["comments"]=comment_list
        post_dict["likes"]=len(i.likes.all())
        post_list.append(post_dict)
    return JsonResponse({"All post values":post_list})