from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest, HttpResponseForbidden


class IsAuthor:
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: Any, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
            obj = self.get_object()
            if not request.user == obj.author:
                return HttpResponseForbidden()
            return func(self, request, *args, **kwargs)

        return wrapper
