
from functools import wraps
from django.utils.decorators import available_attrs
from utils import statusCode


def user_check_test(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            return statusCode.NRK_INVALID_PARAM_USR_PWD_ERR

        return _wrapped_view

    return decorator


def auth_login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_check_test(
        lambda r: r.user.is_authenticated,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def auth_administrator_required(view_func):
    def check_perms(request):
        if request.method == "GET":
            return request.user.is_authenticated
        else:
            return request.user.is_active and request.user.is_superuser

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if check_perms(request):
            return view_func(request, *args, **kwargs)
        else:
            return statusCode.NRK_INVALID_OPERA_LOW_PRIVILEGE
    return _wrapped_view


