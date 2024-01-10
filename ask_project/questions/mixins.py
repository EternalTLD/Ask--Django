from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpRequest, HttpResponseForbidden
from django.http.response import HttpResponse


class AuthorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        obj = self.get_object()
        if not request.user == obj.author:
            return HttpResponseForbidden(f"You must be an author of {obj}")
        return super().dispatch(request, *args, **kwargs)
