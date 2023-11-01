from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
# Decorator for views that checks that the user is logged in, redirecting

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            #print('Working allowed User Decorator: ', allowed_roles)
            group = None
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # if group == 'admin':
            #     print('redirect to admin page')
            #     return redirect('admin_home')
            
            if group in allowed_roles:
                #print('Working allowed User Decorator: ', allowed_roles)
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

# 
# 
# @login_required(login_url='login_user')
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group != 'admin':
            #print('Not an Admin, redirect to home')
            return redirect('home')
        
        if group == 'admin':
            #print('Admin, redirect to admin page')
            return view_func(request, *args, **kwargs)

        else:
            messages.error(request, 'You are not authorized to view this page. This is for Admin only')
            return HttpResponse('You are not authorized to view this page. This is for Admin only')

    return wrapper_function