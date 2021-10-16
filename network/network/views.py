import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
    "posts":page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create(request):
    if request.method == "POST":
        body = request.POST["body"]
        if body == '':
            return render(request, "network/index.html", {
            "posts":Post.objects.all().order_by('-timestamp'),
            "message":"You must type in something."
            })
        # create new posting
        post = Post.objects.create(owner=request.user, body=body)
        post.save()
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def profile(request,profile):
    bool = True
    try:
        f = Follow.objects.get(follower=request.user, followed__username=profile)
        bool = False
    except ObjectDoesNotExist:
        pass
    posts = Post.objects.filter(owner__username=profile).order_by('-timestamp')
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
    "current_user":User.objects.get(username=profile),
    "posts":page_obj,
    "follower":Follow.objects.filter(followed__username=profile).count(),
    "followed":Follow.objects.filter(follower__username=profile).count(),
    "bool":bool
    })

@login_required
def follow(request, profile):
    if request.method == "POST":
        #wenn es noch keinen Follow gibt, erstelle einen neuen, ansonsten lösche den bestehenden
        u = User.objects.get(username=profile)
        try:
            f = Follow.objects.get(follower=request.user, followed=u)
            f.delete()
        except ObjectDoesNotExist:
            f = Follow.objects.create(follower=request.user, followed=u)
            f.save()
        return redirect('profile', profile=profile)
    else:
        # display posts of Follows
        posts = []
        users = []
        follow_list = Follow.objects.filter(follower=request.user)
        for follow in follow_list:
            users.append(follow.followed)
        for user in users:
            posts.extend(Post.objects.filter(owner=user))
        posts.sort(key=lambda post: post.timestamp, reverse=True)
        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
        "posts":page_obj
        })


@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(owner=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "PUT required."
        }, status=400)

@csrf_exempt
@login_required
def like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "GET":
        #existiert der Like schon?
        try:
            like = Like.objects.get(liker=request.user, post=post)
            post.likes -= 1
            like.delete()
            post.save()
        except Like.DoesNotExist:
            like = Like.objects.create(liker=request.user, post=post)
            post.likes += 1
            like.save()
            post.save()
        return JsonResponse(post.serialize())
