
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import (login as django_login,
                                 authenticate,
                                 logout as django_logout,
                                 get_user_model)
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, AuthenticationForm, BlogAdditionForm
from .models import Blog, Comment


def index(request):

    blog_list = Blog.objects.all()

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
            return HttpResponse("form data invalid.")
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
                        user = User.objects.get(username=username)
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
			#user = get_user_model()
			try:
				blog = Blog(title=blog_form.cleaned_data['title'],
                            blog_text=blog_form.cleaned_data['blog_text'])
				blog.user = user
				blog.save()

				return HttpResponse('Blog Addition successful.')
			except Exception, e:
				return HttpResponse('Blog addition failed.'+str(e))
		else:
			return HttpResponse('invalid form data.')
	else:
		blog_form = BlogAdditionForm()

	return render_to_response('blogs/add_blog.html', {
		'form': blog_form
	}, context_instance=RequestContext(request))
