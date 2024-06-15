from srvmedicals.models import User
from django.shortcuts import redirect
from django.contrib.sessions.backends.db import SessionStore



def authenticate(request, username=None, password=None):
    user = User.objects.filter(email=username).values()
    try:
        dbPass = user[0]["password"]
        if dbPass == password:
            return user
        else:
            return None
    except:
        return None




def login(request, user):
    session = SessionStore()
    session['emai'] = user[0]["email"]
    session["mobile"] = user[0]["mboile_no"]
    session.save()
    request.session = session


def logout(request):
    request.session.flush()


def login_required(login_url='login'):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
                # return redirect('view_fuc')
            else:
                # Redirect to the specified login URL
                return redirect(login_url)
        return wrapper
    return decorator
