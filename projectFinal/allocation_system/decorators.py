from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

def role_required(user_types):
    def decorator(func):
        @wraps(func)
        def wrap(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated == True and user.user_type in user_types:
                return func(request, *args, **kwargs)
            else:
                return render(request, '403_Not_Authorized.html')
        return wrap
    return decorator