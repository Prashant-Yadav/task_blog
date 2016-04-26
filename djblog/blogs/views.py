
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import (login as django_login,
                                 authenticate,
                                 logout as django_logout)
from django.contrib.auth.decorators import login_required

from .forms import (UserRegistrationForm,
                    AuthenticationForm,
                    BlogAdditionForm,
                    CommentAdditionForm,
                    BlogUpdateForm)
from .models import Blog, Comment


def index(request):

    blog_list = Blog.objects.all().order_by('-created')

    context = {
        'blog_list': blog_list,
        'user': request.user.username,
    }

    return render_to_response('blogs/index.html', context)


@csrf_protect
def signup(request):

    if request.method == 'POST':
        signup_form = UserRegistrationForm(request.POST)

        if signup_form.is_valid():

            user = User.objects.create_user(username=signup_form.cleaned_data['username'],
                                            password=signup_form.cleaned_data[
                                                'password'],
                                            email=signup_form.cleaned_data['email'])

            user = authenticate(username=signup_form.cleaned_data['username'],
                                password=signup_form.cleaned_data['password'])

            if user is not None:
                if user.is_active:
                    # Login User
                    django_login(request, user)
                    return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/invalid_data/')
    else:
        signup_form = UserRegistrationForm()

    return render_to_response('blogs/signup.html', {
        'signup_form': signup_form
    }, context_instance=RequestContext(request))


def login(request):

    if request.method == 'POST':
        auth_form = AuthenticationForm(request.POST)

        if auth_form.is_valid():
            username = request.POST['username']
            try:
                user = authenticate(username=username,
                                    password=request.POST['password'])

                if user is not None:
                    if user.is_active:
                        django_login(request, user)
                        return HttpResponseRedirect('/')
            except:
                return HttpResponse("invalid Login.")
    else:
        auth_form = AuthenticationForm()

    return render_to_response('blogs/login.html', {
        'login_form': auth_form
    }, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def logout(request):
    '''
    Log out view
    '''
    django_logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def add_blog(request):

    if request.method == 'POST':
        blog_form = BlogAdditionForm(request.POST)

        if blog_form.is_valid():
            user = User.objects.get(username=request.user)
            try:
                blog = Blog(title=blog_form.cleaned_data['title'],
                            blog_text=blog_form.cleaned_data['blog_text'])
                blog.user = user
                blog.save()

                blog_id = blog.id

                return HttpResponseRedirect('/')

            except Exception, e:
                return HttpResponse('Blog addition failed.' + str(e))
        else:
            return HttpResponseRedirect('/invalid_data/')
    else:
        blog_form = BlogAdditionForm()

    return render_to_response('blogs/add_blog.html', {
        'form': blog_form
    }, context_instance=RequestContext(request))


@csrf_protect
def blog_view(request, blog_id):

    is_blog_owner = False
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog)
    if request.method == 'POST':
        comment_form = CommentAdditionForm(request.POST)

        if comment_form.is_valid():
            user = User.objects.get(username=request.user)
            try:
                comment = Comment(comment_text=comment_form.cleaned_data[
                                  'comment_text'], user=user, blog=blog)
                comment.save()

                return HttpResponseRedirect('/blog_view/' + blog_id)
            except Exception, e:
                return HttpResponse('Comment addition failed: ' + str(e))
        else:
            return HttpResponseRedirect('/invalid_data/')
    else:
        comment_form = CommentAdditionForm()

    if blog.user == request.user:
        is_blog_owner = True

    context = {
        'comment_form': comment_form,
        'blog': blog,
        'comments': comments,
        'user': request.user.username,
        'blog_owner': is_blog_owner,
    }

    return render(request, 'blogs/blog_view.html', context)


@login_required(login_url='/login/')
def edit_blog(request, blog_id):

    blog = Blog.objects.get(id=blog_id)

    if request.method == 'POST':
        form = BlogUpdateForm(request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user)
            try:
                blog.title = form.cleaned_data['title']
                blog.blog_text = form.cleaned_data['blog_text']
                blog.save()

                blog_id = blog.id

                return HttpResponseRedirect('/blog_view/' + blog_id)

            except Exception, e:
                return HttpResponse('Blog updation failed: ' + str(e))
        else:
            return HttpResponseRedirect('/invalid_data/')
    else:
        form = BlogUpdateForm(instance=blog)

    context = {
        'form': form,
        'blog': blog,
        'user': request.user.username,
    }

    return render(request, 'blogs/edit_blog.html', context)


@login_required(login_url='/login/')
def delete_blog(request, blog_id):

    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog)

    for comment in comments:
        comment.delete()

    blog.delete()

    context = {}

    return render(request, 'blogs/delete_blog.html', context)


def invalid_data(request):

    context = {}

    return render(request, 'blogs/invalid_data.html', context)
