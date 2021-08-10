from django.contrib.auth import authenticate
from django.core.checks import messages
from django.http import request
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from blog.forms import SignupForm, ImageForm
from blog.forms import LoginForm
from blog.forms import PostForm
from django.contrib.auth import authenticate, login, logout
from blog.models import Post, Image
from django.contrib.auth.models import Group
from django.core.cache import cache


# Create your views here.


# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


# About
def about(request):
    return render(request, 'blog/about.html')


# Contact
def contact(request):
    return render(request, 'blog/contact.html')


# Dashboard
def dashboard(request):
    if request.user.is_authenticated:

        posts = Post.objects.all()
        user = request.user
        fullname = user.get_full_name()
        grps = user.groups.all()
        count = cache.get('count', version=user.pk)

        return render(request, 'blog/dashboard.html', {'posts': posts, 'fullname': fullname, 'groups': grps, 'ct': count})
    else:
        return HttpResponseRedirect('/login/')


# Signup
def user_signup(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            messages.success(
                request, 'Congratulations!! You have successfully created your account')
            user = fm.save()
            grp = Group.objects.get(name='Auther')
            user.groups.add(grp)
    else:
        fm = SignupForm()
    return render(request, 'blog/signup.html', {"form": fm})


# Login
def user_login(request):
    if not request.user.is_authenticated:
        # print('before post')
        if request.method == 'POST':
            fm = LoginForm(request=request, data=request.POST)
            # print('after post')
            c = cache.get(
                'fail_count', version=request.POST.get('username'))
            # print(f'count from view: {c}')
            if c == None:
                if fm.is_valid():
                    uname = fm.cleaned_data['username']
                    upass = fm.cleaned_data['password']
                    # print('after is valid')
                    user = authenticate(username=uname, password=upass)
                    print(user)
                    if user is not None:
                        login(request, user)
                        messages.success(
                            request, 'You are successfully logged in')
                        return HttpResponseRedirect('/dashboard/')
            else:
                messages.info(
                    request, 'You account has been locked. Please login after 60 sec...')
                return render(request, 'blog/login.html', {"form": fm})
        else:
            fm = LoginForm()
        return render(request, 'blog/login.html', {"form": fm})
    else:
        return HttpResponseRedirect('/dashboard/')


# Add post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PostForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                fm = PostForm()
        else:
            fm = PostForm()
        return render(request, 'blog/addpost.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# Update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            fm = PostForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            fm = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


# delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                pi = Post.objects.get(pk=id)
                pi.delete()
                return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
