from django.http import HttpResponse
from django.shortcuts import redirect

# Decorator for views that checks that the user is logged in, redirecting

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

