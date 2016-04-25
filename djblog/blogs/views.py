
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import (login as django_login,
                                 authenticate,
                                 logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from .forms import UserRegistrationForm, AuthenticationForm
from .models import Blog, Comment


def index(request):

    #blog_list = Blog.objects.all()

    context = {
        #'blog_list': blog_list,
        'user': request.user.username,
    }

    return render_to_response('blogs/index.html', context)


def signup(request):

    if request.method == 'POST':
        signup_form = UserRegistrationForm(request.POST)

        if signup_form.is_valid():
        	try:
        		user = User.objects.create_user(username=signup_form.cleaned_data['username'],
	                                            email=signup_form.cleaned_data[
	                                                'email'],
	                                            password=signup_form.cleaned_data[
	                                                'password'],
	                                            first_name=signup_form.cleaned_data[
	                                                'first_name'],
	                                            last_name=signup_form.cleaned_data['last_name'])
        		user.save()

        		# Login User
        		django_login(request, user)
        		return HttpResponseRedirect('/')	
        	except :
        		return HttpResponse("Form data invalid.")
		else:
			pass
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
