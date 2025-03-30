from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def user_is_not_authenticated(function=None, login_url='/'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated, 
        login_url=login_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator