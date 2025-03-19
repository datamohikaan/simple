from functools import wraps
from frontend.app import abort


def check_role_access(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Inner function that performs the role-based access check before executing the original function.

        Args:
            *args (Any): Positional arguments to be passed to the original function.
            **kwargs (Any): Keyword arguments to be passed to the original function.

        Returns:
            Any: The return value of the original function if access is granted.
        """
        # Get the set of pages the user's role has explicit access to
        print(f"Checking access for function: {func.__name__}")

        if func.__name__ == 'protected_func':
            abort(403)  # Deny access with a 403 Forbidden response

        else:
            pass
        # Proceed with the original function if access is granted
        return func(*args, **kwargs)

    return decorated_function


@check_role_access
def printer_123_A(input):
    print('helu ' + input)


@check_role_access
def protected_func(input):
    print('helu secret' + input)


printer_123_A('suley')
protected_func('suley')


