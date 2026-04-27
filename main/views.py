from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post
from django.contrib.auth.models import Group

def home(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
            post.delete()
    return render(request, 'main/home.html', {"posts" : posts})

@login_required(login_url="/login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, "main/post.html", {"form" : form})

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            default_group = Group.objects.get_or_create(name='defalt')
            user.groups.add(default_group)
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "registration/sign-up.html", {"form" : form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login")