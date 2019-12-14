from importlib import import_module
from functools import wraps


# from django.utils.module_loading import import_string
def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


def never_cache(view_func):
    """
    Decorator that adds headers to a response so that it will never be cached.
    """
    @wraps(view_func)
    def _wrapped_view_func(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response.headers['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        return response
    return _wrapped_view_func
